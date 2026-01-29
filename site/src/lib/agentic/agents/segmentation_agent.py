"""
[INPUT]: 文章文本 (str)
[OUTPUT]: ArticleSegmentation - 按意图切分的文章结构
[POS]: agentic/agents 的核心 agent，负责将文章按意图切分

[PROTOCOL]:
1. 一旦本文件逻辑变更，必须同步更新此 Header。
2. 更新后必须上浮检查 agents/.folder.md 的描述是否仍然准确。
"""

from agents import Agent, Runner

from ..models import ArticleSegmentation
from ..utils import get_default_model

SEGMENTATION_INSTRUCTIONS = """你是一个文章分析专家。你的任务是将文章按照"意图"进行切分。

## 任务

分析输入的文章，识别其中的不同意图块。每个意图块代表文章中一个独立的论点、观点或信息单元。

## 切分规则

1. **按意图而非段落切分**：一个意图可能跨越多个自然段落，也可能一个段落包含多个意图
2. **意图的完整性**：每个意图块应该是自包含的，能够独立表达一个完整的观点
3. **动态数量**：根据文章实际内容决定意图数量，不要人为限制或扩充

## 意图识别标准

- 核心论点或观点
- 关键结论或发现
- 重要的数据分析
- 独立的案例或例证
- 明确的行动建议

## 输出要求

- `intent`: 用一句话概括该意图块的核心内容
- `paragraphs`: 属于该意图的所有段落原文（保持原文，不要修改、不要删减）

## 语言规则

**必须使用文章的原始语言输出**：
- 英文文章 → 英文的 intent
- 中文文章 → 中文的 intent
"""


# 创建 Agent 实例
segmentation_agent = Agent(
    name="Article Segmenter",
    instructions=SEGMENTATION_INSTRUCTIONS,
    output_type=ArticleSegmentation,
    model=get_default_model(),
)


async def segment_article(article_text: str) -> ArticleSegmentation:
    """
    将文章按意图切分

    Args:
        article_text: 文章原文

    Returns:
        ArticleSegmentation: 切分后的意图结构
    """
    result = await Runner.run(segmentation_agent, article_text)
    return result.final_output_as(ArticleSegmentation)


def segment_article_sync(article_text: str) -> ArticleSegmentation:
    """
    同步版本：将文章按意图切分

    Args:
        article_text: 文章原文

    Returns:
        ArticleSegmentation: 切分后的意图结构
    """
    result = Runner.run_sync(segmentation_agent, article_text)
    return result.final_output_as(ArticleSegmentation)
