"""
[INPUT]: ArticleSegmentation (从 segmentation_agent 输出)
[OUTPUT]: List[TemplateSelection] - 每个 intent 对应一个模板选择结果
[POS]: agents/ 的流水线入口，协调整个处理流程

[PROTOCOL]:
1. 一旦本文件逻辑变更，必须同步更新此 Header。
2. 更新后必须上浮检查 agents/.folder.md 的描述是否仍然准确。
"""

from __future__ import annotations

import asyncio
import time
from typing import List, Optional

from agents import Runner

from .template_selector import template_selector
from .segmentation_agent import segment_article, segment_article_sync
from ..models import ArticleSegmentation, Intent, TemplateSelection
from ..utils import pipeline_logger


async def select_template_for_intent(
    intent: Intent, index: int
) -> Optional[TemplateSelection]:
    """
    为单个 intent 选择模板

    Args:
        intent: 意图块
        index: 意图索引

    Returns:
        TemplateSelection 或 None（如果处理失败）
    """
    start_time = time.time()
    pipeline_logger.intent_processing_start(index, intent.intent)

    # 构造输入文本
    input_text = f"""## 意图
{intent.intent}

## 段落内容
{chr(10).join(intent.paragraphs)}
"""

    try:
        result = await Runner.run(template_selector, input_text)

        # 从结果中提取 TemplateSelection
        # 由于使用了 handoff + stop_on_first_tool，最终输出应该是 tool 的返回值
        final_output = result.final_output

        duration = time.time() - start_time

        if isinstance(final_output, TemplateSelection):
            if final_output.template is None:
                # skip 情况
                pipeline_logger.intent_skipped(index, final_output.rationale)
            else:
                pipeline_logger.intent_processing_complete(
                    index, final_output.category, final_output.template or "N/A", duration
                )
            return final_output
        elif isinstance(final_output, dict):
            selection = TemplateSelection(**final_output)
            if selection.template is None:
                pipeline_logger.intent_skipped(index, selection.rationale)
            else:
                pipeline_logger.intent_processing_complete(
                    index, selection.category, selection.template or "N/A", duration
                )
            return selection
        else:
            # 尝试从字符串解析
            import json

            if isinstance(final_output, str):
                # 检查是否是 skip 格式的字符串输出
                if "category='skip'" in final_output or "sub_category=None" in final_output:
                    # 解析 skip 输出
                    pipeline_logger.intent_skipped(index, str(final_output))
                    return TemplateSelection(
                        category="skip",
                        sub_category=None,
                        template=None,
                        data=None,
                        rationale=str(final_output),
                    )
                try:
                    data = json.loads(final_output)
                    selection = TemplateSelection(**data)
                    pipeline_logger.intent_processing_complete(
                        index, selection.category, selection.template or "N/A", duration
                    )
                    return selection
                except (json.JSONDecodeError, TypeError):
                    pass
            pipeline_logger.intent_error(index, f"Unexpected output type: {type(final_output)}")
            return None
    except Exception as e:
        duration = time.time() - start_time
        pipeline_logger.intent_error(index, str(e))
        return None


async def process_intents(
    segmentation: ArticleSegmentation,
) -> List[Optional[TemplateSelection]]:
    """
    并发处理所有 intent blocks

    Args:
        segmentation: 文章切分结果

    Returns:
        每个 intent 对应的 TemplateSelection 列表（失败的为 None）
    """
    tasks = [
        select_template_for_intent(intent, i)
        for i, intent in enumerate(segmentation.intents)
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # 处理异常
    processed_results: List[Optional[TemplateSelection]] = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            pipeline_logger.intent_error(i, str(result))
            processed_results.append(None)
        else:
            processed_results.append(result)

    return processed_results


async def process_article(article_text: str) -> List[Optional[TemplateSelection]]:
    """
    完整流程：切分文章 -> 并发选择模板

    Args:
        article_text: 文章原文

    Returns:
        每个 intent 对应的 TemplateSelection 列表
    """
    pipeline_start = time.time()
    pipeline_logger.start_pipeline(len(article_text))

    # Step 1: 切分文章
    seg_start = time.time()
    pipeline_logger.segmentation_start()
    segmentation = await segment_article(article_text)
    seg_duration = time.time() - seg_start
    pipeline_logger.segmentation_complete(len(segmentation.intents), seg_duration)

    # Step 2: 并发处理每个 intent
    results = await process_intents(segmentation)

    # 统计结果
    success_count = sum(1 for r in results if r is not None)
    pipeline_duration = time.time() - pipeline_start
    pipeline_logger.end_pipeline(len(segmentation.intents), success_count, pipeline_duration)

    return results


def process_article_sync(article_text: str) -> List[Optional[TemplateSelection]]:
    """
    同步版本：完整流程

    Args:
        article_text: 文章原文

    Returns:
        每个 intent 对应的 TemplateSelection 列表
    """
    return asyncio.run(process_article(article_text))


async def process_article_with_segmentation(
    article_text: str,
) -> tuple[ArticleSegmentation, List[Optional[TemplateSelection]]]:
    """
    完整流程，同时返回切分结果和模板选择结果

    Args:
        article_text: 文章原文

    Returns:
        (切分结果, 模板选择列表)
    """
    pipeline_start = time.time()
    pipeline_logger.start_pipeline(len(article_text))

    # Step 1: 切分文章
    seg_start = time.time()
    pipeline_logger.segmentation_start()
    segmentation = await segment_article(article_text)
    seg_duration = time.time() - seg_start
    pipeline_logger.segmentation_complete(len(segmentation.intents), seg_duration)

    # Step 2: 并发处理每个 intent
    results = await process_intents(segmentation)

    # 统计结果
    success_count = sum(1 for r in results if r is not None)
    pipeline_duration = time.time() - pipeline_start
    pipeline_logger.end_pipeline(len(segmentation.intents), success_count, pipeline_duration)

    return segmentation, results
