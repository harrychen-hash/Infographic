#!/usr/bin/env python3
"""
[INPUT]: 文章文件路径或文本
[OUTPUT]: 完整 pipeline 测试结果
[POS]: agentic/scripts 的完整流程测试脚本

[PROTOCOL]:
1. 一旦本文件逻辑变更，必须同步更新此 Header。
2. 更新后必须上浮检查 scripts/.folder.md 的描述是否仍然准确。

使用方法:
    cd site/src/lib/agentic
    .venv/bin/python -m scripts.test_pipeline /path/to/article.md
"""

from __future__ import annotations

import asyncio
import json
import sys
import time
from pathlib import Path
from datetime import datetime

# 获取路径
SCRIPT_DIR = Path(__file__).parent
AGENTIC_ROOT = SCRIPT_DIR.parent
LIB_ROOT = AGENTIC_ROOT.parent  # site/src/lib
PROJECT_ROOT = AGENTIC_ROOT.parent.parent.parent.parent

# ========== 解决 agents 包名冲突 ==========
# openai-agents 包使用 "agents" 作为模块名，与本地 agents 目录冲突
# 必须在添加本地路径之前先导入 openai-agents

# 1. 移除可能包含本地 agents 目录的路径
paths_to_remove = [str(AGENTIC_ROOT), str(AGENTIC_ROOT.resolve()), ""]
original_paths = sys.path.copy()
for p in paths_to_remove:
    while p in sys.path:
        sys.path.remove(p)

# 2. 先导入 openai-agents 的 agents 包
import agents as openai_agents_sdk
Agent = openai_agents_sdk.Agent
Runner = openai_agents_sdk.Runner
function_tool = openai_agents_sdk.function_tool

# 3. 恢复路径并添加 lib 路径
sys.path = original_paths
sys.path.insert(0, str(LIB_ROOT))

# 4. 确保 'agents' 在 sys.modules 中指向 openai-agents，防止被本地 agents 覆盖
# 这样当 agentic.tools 中的文件 import agents 时，会得到正确的模块
sys.modules["agents"] = openai_agents_sdk

# 现在导入本地模块 (使用 agentic 作为包名)
from agentic.models import ArticleSegmentation, TemplateSelection, Intent


class PipelineLogger:
    """简单的 pipeline 日志记录器"""

    def log(self, level: str, msg: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{timestamp} │ {level:7} │ {msg}")

    def info(self, msg: str):
        self.log("INFO", msg)

    def error(self, msg: str):
        self.log("ERROR", msg)

    def start_pipeline(self, article_length: int):
        self.info(f"🚀 Pipeline started | Article length: {article_length} chars")

    def end_pipeline(self, intent_count: int, success_count: int, duration: float):
        self.info(f"✅ Pipeline completed | Intents: {intent_count} | Success: {success_count} | Duration: {duration:.2f}s")

    def segmentation_start(self):
        self.info("📝 Segmentation started")

    def segmentation_complete(self, intent_count: int, duration: float):
        self.info(f"📝 Segmentation complete | Intents: {intent_count} | Duration: {duration:.2f}s")

    def intent_processing_start(self, index: int, intent: str):
        short = intent[:50] + "..." if len(intent) > 50 else intent
        self.info(f"🔄 [{index}] Processing intent: {short}")

    def intent_processing_complete(self, index: int, category: str, template: str, duration: float):
        self.info(f"✓  [{index}] Selected: {category}/{template} | Duration: {duration:.2f}s")

    def intent_skipped(self, index: int, reason: str):
        self.info(f"⏭  [{index}] Skipped: {reason[:80]}")

    def intent_error(self, index: int, error: str):
        self.error(f"❌ [{index}] Error: {error}")


logger = PipelineLogger()


# 导入本地 utils
from agentic.utils import get_default_model, get_model_settings


# ========== 内联定义 agents 以避免导入冲突 ==========

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

segmentation_agent = Agent(
    name="Article Segmenter",
    instructions=SEGMENTATION_INSTRUCTIONS,
    output_type=ArticleSegmentation,
    model=get_default_model(),
    model_settings=get_model_settings(),
)


async def segment_article(article_text: str) -> ArticleSegmentation:
    """将文章按意图切分"""
    result = await Runner.run(segmentation_agent, article_text)
    return result.final_output_as(ArticleSegmentation)


# ========== Template Selector (简化版，用于测试) ==========

from agentic.tools.chart_tools import chart_pie, chart_bar, chart_line, chart_column, chart_wordcloud
from agentic.tools.list_tools import list_column, list_grid, list_pyramid, list_row, list_sector, list_zigzag
from agentic.tools.sequence_tools import (
    sequence_stairs, sequence_timeline, sequence_steps, sequence_snake,
    sequence_circular, sequence_funnel, sequence_roadmap, sequence_zigzag
)
from agentic.tools.comparison_tools import compare_binary, compare_hierarchy, compare_swot, compare_quadrant
from agentic.tools.hierarchy_tools import hierarchy_tree, hierarchy_mindmap, hierarchy_structure
from agentic.tools.relation_tools import relation_dagre_flow, relation_circle
from agentic.tools.quadrant_tools import quadrant_quarter, quadrant_simple
from agentic.tools.common import (
    skip_chart, skip_list, skip_sequence, skip_comparison,
    skip_hierarchy, skip_relation, skip_quadrant
)

# Category Agents Instructions
CHART_AGENT_INSTRUCTIONS = """你是图表数据提取专家。从段落内容中提取结构化数据并选择合适的图表模板。

## 任务
1. 分析段落内容，识别可视化的数据
2. 选择最合适的图表类型（饼图、柱状图等）
3. 从文本中提取具体的数据项
4. 调用对应的工具，传入正确的 data_json

## data_json 格式
必须是 JSON 字符串格式：{"values": [{"label": "项目名", "value": 数值}]}

## 示例
输入段落: "2023年市场份额：产品A占35%，产品B占25%，产品C占20%，其他占20%"
提取数据: {"values": [{"label": "产品A", "value": 35}, {"label": "产品B", "value": 25}, {"label": "产品C", "value": 20}, {"label": "其他", "value": 20}]}

如果段落中没有明确的数值数据，使用 skip_chart 跳过。
"""

chart_agent = Agent(
    name="Chart Agent",
    handoff_description="处理数据图表类内容",
    instructions=CHART_AGENT_INSTRUCTIONS,
    tools=[chart_pie, chart_bar, chart_line, chart_column, chart_wordcloud, skip_chart],
    tool_use_behavior="stop_on_first_tool",
    model=get_default_model(),
    model_settings=get_model_settings(),
)

LIST_AGENT_INSTRUCTIONS = """你是列表数据提取专家。从段落内容中提取结构化列表并选择合适的模板。

## 任务
1. 分析段落内容，识别列表项
2. 选择最合适的列表类型
3. 从文本中提取具体的列表项
4. 调用对应的工具，传入正确的 data_json

## data_json 格式
必须是 JSON 字符串格式：{"lists": [{"label": "列表项1"}, {"label": "列表项2"}]}

## 示例
输入段落: "主要功能包括：实时监控、数据分析、报告生成、用户管理"
提取数据: {"lists": [{"label": "实时监控"}, {"label": "数据分析"}, {"label": "报告生成"}, {"label": "用户管理"}]}

如果段落中没有明确的列表结构，使用 skip_list 跳过。
"""

list_agent = Agent(
    name="List Agent",
    handoff_description="处理列表类内容",
    instructions=LIST_AGENT_INSTRUCTIONS,
    tools=[list_column, list_grid, list_pyramid, list_row, list_sector, list_zigzag, skip_list],
    tool_use_behavior="stop_on_first_tool",
    model=get_default_model(),
    model_settings=get_model_settings(),
)

SEQUENCE_AGENT_INSTRUCTIONS = """你是流程数据提取专家。从段落内容中提取步骤/流程并选择合适的模板。

## 任务
1. 分析段落内容，识别流程步骤
2. 选择最合适的流程类型（时间线、漏斗、路线图等）
3. 从文本中提取具体的步骤
4. 调用对应的工具，传入正确的 data_json

## data_json 格式
必须是 JSON 字符串格式：{"sequences": [{"label": "步骤1"}, {"label": "步骤2"}]}

## 示例
输入段落: "项目开发分为四个阶段：需求分析、系统设计、编码实现、测试上线"
提取数据: {"sequences": [{"label": "需求分析"}, {"label": "系统设计"}, {"label": "编码实现"}, {"label": "测试上线"}]}

如果段落中没有明确的流程/步骤，使用 skip_sequence 跳过。
"""

sequence_agent = Agent(
    name="Sequence Agent",
    handoff_description="处理时序流程类内容",
    instructions=SEQUENCE_AGENT_INSTRUCTIONS,
    tools=[sequence_stairs, sequence_timeline, sequence_steps, sequence_snake,
           sequence_circular, sequence_funnel, sequence_roadmap, sequence_zigzag, skip_sequence],
    tool_use_behavior="stop_on_first_tool",
    model=get_default_model(),
    model_settings=get_model_settings(),
)

COMPARISON_AGENT_INSTRUCTIONS = """你是对比数据提取专家。从段落内容中提取对比关系并选择合适的模板。

## 任务
1. 分析段落内容，识别对比关系
2. 选择最合适的对比类型（二元对比、SWOT、象限等）
3. 从文本中提取具体的对比数据
4. 调用对应的工具，传入正确的 data_json

## data_json 格式
- compare_binary: {"compares": [{"label": "左侧标题", "children": ["特性1", "特性2"]}, {"label": "右侧标题", "children": ["特性A", "特性B"]}]}
- compare_hierarchy: {"compares": [{"label": "分类名", "children": ["特性1", "特性2"]}]}
- compare_swot: {"compares": [{"label": "优势", "children": [...]}, {"label": "劣势", "children": [...]}, {"label": "机会", "children": [...]}, {"label": "威胁", "children": [...]}]}

## 示例
输入段落: "传统方法依赖人工处理，效率低，成本高；AI方法实现自动化，效率高，成本低"
提取数据: {"compares": [{"label": "传统方法", "children": ["人工处理", "效率低", "成本高"]}, {"label": "AI方法", "children": ["自动化", "效率高", "成本低"]}]}

如果段落中没有明确的对比关系，使用 skip_comparison 跳过。
"""

comparison_agent = Agent(
    name="Comparison Agent",
    handoff_description="处理对比分析类内容",
    instructions=COMPARISON_AGENT_INSTRUCTIONS,
    tools=[compare_binary, compare_hierarchy, compare_swot, compare_quadrant, skip_comparison],
    tool_use_behavior="stop_on_first_tool",
    model=get_default_model(),
    model_settings=get_model_settings(),
)

HIERARCHY_AGENT_INSTRUCTIONS = """你是层级结构提取专家。从段落内容中提取层级关系并选择合适的模板。

## 任务
1. 分析段落内容，识别层级结构
2. 选择最合适的层级类型（树状图、思维导图、组织架构）
3. 从文本中提取层级数据
4. 调用对应的工具，传入正确的 data_json

## data_json 格式
必须是 JSON 字符串格式：{"root": {"label": "根节点", "children": [{"label": "子节点1", "children": [...]}, {"label": "子节点2"}]}}

## 示例
输入段落: "技术栈分为前端和后端。前端包括React和Vue，后端包括Python和Go"
提取数据: {"root": {"label": "技术栈", "children": [{"label": "前端", "children": [{"label": "React"}, {"label": "Vue"}]}, {"label": "后端", "children": [{"label": "Python"}, {"label": "Go"}]}]}}

如果段落中没有明确的层级关系，使用 skip_hierarchy 跳过。
"""

hierarchy_agent = Agent(
    name="Hierarchy Agent",
    handoff_description="处理层级结构类内容",
    instructions=HIERARCHY_AGENT_INSTRUCTIONS,
    tools=[hierarchy_tree, hierarchy_mindmap, hierarchy_structure, skip_hierarchy],
    tool_use_behavior="stop_on_first_tool",
    model=get_default_model(),
    model_settings=get_model_settings(),
)

RELATION_AGENT_INSTRUCTIONS = """你是关系图提取专家。从段落内容中提取节点和连接关系并选择合适的模板。

## 任务
1. 分析段落内容，识别实体及其关系
2. 选择最合适的关系图类型（有向流程图、环形图）
3. 从文本中提取节点和边
4. 调用对应的工具，传入正确的 data_json

## data_json 格式
必须是 JSON 字符串格式：{"nodes": [{"id": "A", "label": "节点A"}], "relations": [{"from": "A", "to": "B"}]}

## 示例
输入段落: "数据采集后进入数据处理，处理后存入数据库，最后展示给用户"
提取数据: {"nodes": [{"id": "A", "label": "数据采集"}, {"id": "B", "label": "数据处理"}, {"id": "C", "label": "数据存储"}, {"id": "D", "label": "数据展示"}], "relations": [{"from": "A", "to": "B"}, {"from": "B", "to": "C"}, {"from": "C", "to": "D"}]}

如果段落中没有明确的关系/流向，使用 skip_relation 跳过。
"""

relation_agent = Agent(
    name="Relation Agent",
    handoff_description="处理关系图类内容",
    instructions=RELATION_AGENT_INSTRUCTIONS,
    tools=[relation_dagre_flow, relation_circle, skip_relation],
    tool_use_behavior="stop_on_first_tool",
    model=get_default_model(),
    model_settings=get_model_settings(),
)

QUADRANT_AGENT_INSTRUCTIONS = """你是象限图提取专家。从段落内容中提取四象限分类并选择合适的模板。

## 任务
1. 分析段落内容，识别四象限分类
2. 选择最合适的象限类型
3. 从文本中提取每个象限的内容
4. 调用对应的工具，传入正确的 data_json

## data_json 格式
必须是 JSON 字符串格式：{"compares": [{"label": "象限1标题", "children": ["项目1", "项目2"]}, {"label": "象限2标题", "children": ["项目A"]}]}

## 示例
输入段落: "高价值高成本的有策略A和B，高价值低成本的有策略C，低价值高成本的有策略D，低价值低成本的有策略E和F"
提取数据: {"compares": [{"label": "高价值/高成本", "children": ["策略A", "策略B"]}, {"label": "高价值/低成本", "children": ["策略C"]}, {"label": "低价值/高成本", "children": ["策略D"]}, {"label": "低价值/低成本", "children": ["策略E", "策略F"]}]}

如果段落中没有明确的四象限结构，使用 skip_quadrant 跳过。
"""

quadrant_agent = Agent(
    name="Quadrant Agent",
    handoff_description="处理象限图类内容",
    instructions=QUADRANT_AGENT_INSTRUCTIONS,
    tools=[quadrant_quarter, quadrant_simple, skip_quadrant],
    tool_use_behavior="stop_on_first_tool",
    model=get_default_model(),
    model_settings=get_model_settings(),
)


@function_tool
def skip_visualization(reason: str) -> str:
    """跳过当前意图块，不生成可视化"""
    return f"category='skip' sub_category=None template=None data=None rationale='{reason}'"


skip_agent = Agent(
    name="Skip Agent",
    handoff_description="当内容不适合任何可视化方案时使用",
    instructions="判断内容确实不适合可视化后，调用 skip_visualization 工具",
    tools=[skip_visualization],
    tool_use_behavior="stop_on_first_tool",
    model=get_default_model(),
    model_settings=get_model_settings(),
)

TEMPLATE_SELECTOR_INSTRUCTIONS = """你是图表类型选择专家。根据用户提供的意图和段落内容，决定应该使用哪种类型的图表。

## 可用的图表类型

1. **Chart Agent** - 数据图表（占比、趋势、数值对比）
2. **Comparison Agent** - 对比分析（两方对比、SWOT）
3. **Hierarchy Agent** - 层级结构（组织架构、树状图）
4. **List Agent** - 列表展示（步骤清单、特征列表）
5. **Quadrant Agent** - 象限图（二维分类）
6. **Relation Agent** - 关系图（流程依赖、网络关系）
7. **Sequence Agent** - 时序流程（步骤、时间线、漏斗）
8. **Skip Agent** - 跳过可视化（纯叙述性内容）

转交给最合适的 Agent 处理。
"""

template_selector = Agent(
    name="Template Selector",
    instructions=TEMPLATE_SELECTOR_INSTRUCTIONS,
    handoffs=[
        chart_agent, comparison_agent, hierarchy_agent, list_agent,
        quadrant_agent, relation_agent, sequence_agent, skip_agent,
    ],
    model=get_default_model(),
    model_settings=get_model_settings(),
)


async def select_template_for_intent(intent: Intent, index: int) -> TemplateSelection | None:
    """为单个 intent 选择模板"""
    start_time = time.time()
    logger.intent_processing_start(index, intent.intent)

    input_text = f"""## 意图
{intent.intent}

## 段落内容
{chr(10).join(intent.paragraphs)}
"""

    try:
        result = await Runner.run(template_selector, input_text)
        final_output = result.final_output
        duration = time.time() - start_time

        if isinstance(final_output, TemplateSelection):
            if final_output.template is None:
                logger.intent_skipped(index, final_output.rationale)
            else:
                logger.intent_processing_complete(
                    index, final_output.category, final_output.template, duration
                )
            return final_output
        elif isinstance(final_output, dict):
            selection = TemplateSelection(**final_output)
            if selection.template is None:
                logger.intent_skipped(index, selection.rationale)
            else:
                logger.intent_processing_complete(
                    index, selection.category, selection.template or "N/A", duration
                )
            return selection
        elif isinstance(final_output, str):
            # 尝试解析字符串格式的输出
            import ast

            # Debug: 打印原始输出
            print(f"[RAW OUTPUT] [{index}] {final_output[:300]}...")

            parsed_data = None

            # 方法1: 尝试 ast.literal_eval (处理 Python dict 字符串格式)
            if final_output.strip().startswith("{"):
                try:
                    parsed_data = ast.literal_eval(final_output)
                except Exception as e:
                    logger.info(f"[{index}] ast.literal_eval failed: {e}")

            # 方法2: 回退到正则解析 (处理 Pydantic str() 格式)
            if parsed_data is None and "category=" in final_output:
                import re
                def extract_value(s: str, key: str) -> str | None:
                    pattern = rf"{key}='([^']*)'|{key}=None"
                    match = re.search(pattern, s)
                    if match:
                        return match.group(1) if match.group(1) else None
                    return None

                # 提取 data - 从 "data=" 到 " rationale=" 之间的内容
                data = None
                data_start = final_output.find("data=")
                if data_start != -1:
                    # 检查是否是 data=None
                    if final_output[data_start:data_start+9] == "data=None":
                        data = None
                    else:
                        # 找到 data={ 后面匹配的闭合大括号
                        brace_start = final_output.find("{", data_start)
                        if brace_start != -1:
                            brace_count = 0
                            data_end = brace_start
                            for i, c in enumerate(final_output[brace_start:], start=brace_start):
                                if c == '{':
                                    brace_count += 1
                                elif c == '}':
                                    brace_count -= 1
                                    if brace_count == 0:
                                        data_end = i + 1
                                        break
                            data_str = final_output[brace_start:data_end]
                            try:
                                data = ast.literal_eval(data_str)
                            except Exception as e:
                                print(f"[PARSE ERROR] [{index}] Failed to parse data: {e}")
                                print(f"[PARSE ERROR] data_str: {data_str[:100]}...")

                parsed_data = {
                    "category": extract_value(final_output, "category") or "skip",
                    "sub_category": extract_value(final_output, "sub_category"),
                    "template": extract_value(final_output, "template"),
                    "data": data,
                    "rationale": extract_value(final_output, "rationale") or final_output[:200],
                }

            if parsed_data and isinstance(parsed_data, dict):
                # Debug: 打印解析后的数据
                data_preview = str(parsed_data.get('data', {}))[:100]
                print(f"[DEBUG] [{index}] Parsed data: {data_preview}...")

                selection = TemplateSelection(**parsed_data)
                if selection.template:
                    logger.intent_processing_complete(
                        index, selection.category, selection.template, duration
                    )
                else:
                    logger.intent_skipped(index, (selection.rationale or "Unknown")[:80])
                return selection
            else:
                # 字符串输出但不是标准格式
                logger.intent_skipped(index, f"Unparseable output: {final_output[:60]}...")
                return TemplateSelection(
                    category="skip",
                    sub_category=None,
                    template=None,
                    data=None,
                    rationale=f"Unparseable: {final_output[:200]}",
                )

        # 打印更详细的错误信息以便调试
        output_preview = str(final_output)[:200] if final_output else "None"
        logger.intent_error(index, f"Unexpected output: {type(final_output)} - {output_preview}")
        return None
    except Exception as e:
        logger.intent_error(index, str(e))
        return None


async def process_article(article_text: str) -> tuple[ArticleSegmentation, list]:
    """完整流程：切分文章 -> 并发选择模板"""
    pipeline_start = time.time()
    logger.start_pipeline(len(article_text))

    # Step 1: 切分文章
    seg_start = time.time()
    logger.segmentation_start()
    segmentation = await segment_article(article_text)
    logger.segmentation_complete(len(segmentation.intents), time.time() - seg_start)

    # Step 2: 并发处理每个 intent
    tasks = [select_template_for_intent(intent, i) for i, intent in enumerate(segmentation.intents)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # 处理异常
    processed = []
    for i, r in enumerate(results):
        if isinstance(r, Exception):
            logger.intent_error(i, str(r))
            processed.append(None)
        else:
            processed.append(r)

    success_count = sum(1 for r in processed if r is not None)
    logger.end_pipeline(len(segmentation.intents), success_count, time.time() - pipeline_start)

    return segmentation, processed


async def render_selections(
    selections: list,
    output_dir: Path,
) -> list:
    """渲染选中的模板到 SVG

    Args:
        selections: TemplateSelection 列表
        output_dir: 输出目录

    Returns:
        输出文件路径列表
    """
    from agentic.renderers import generate_dsl, render_to_svg, save_svg

    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = []

    for i, selection in enumerate(selections):
        # Debug: 打印 selection 数据
        if selection:
            data_preview = str(selection.data)[:100] if selection.data else "EMPTY"
            print(f"[RENDER] [{i}] template={selection.template}, data={data_preview}")

        if selection is None or selection.template is None:
            logger.info(f"⏭  [{i}] Render skipped: No template selected")
            outputs.append(None)
            continue

        render_start = time.time()
        logger.info(f"🎨 [{i}] Rendering: {selection.template}")

        try:
            # 生成 DSL
            dsl = generate_dsl(
                template=selection.template,
                category=selection.category,
                data=selection.data or {},
            )

            # Debug: 打印 DSL 内容
            print(f"\n--- DSL for [{i}] ---")
            print(dsl[:800] if len(dsl) > 800 else dsl)
            print("--- End DSL ---\n")

            # 渲染到 SVG
            result = render_to_svg(dsl)

            if result["success"]:
                # 保存 SVG
                svg_path = output_dir / f"infographic-{i}.svg"
                save_svg(result["svg"], svg_path)
                outputs.append(svg_path)
                logger.info(
                    f"✅ [{i}] Saved: {svg_path} | Duration: {time.time() - render_start:.2f}s"
                )
            else:
                logger.error(f"❌ [{i}] Render failed: {result.get('error', 'Unknown error')}")
                outputs.append(None)

        except Exception as e:
            logger.error(f"❌ [{i}] Render exception: {e}")
            outputs.append(None)

    return outputs


async def main(article_path: str, render: bool = False, output_dir: str = None):
    """主函数

    Args:
        article_path: 文章路径
        render: 是否渲染 SVG
        output_dir: 输出目录 (默认 site/output)
    """
    # 读取文章
    article_file = Path(article_path)
    if not article_file.exists():
        article_file = PROJECT_ROOT / article_path
        if not article_file.exists():
            print(f"❌ Article file not found: {article_path}")
            return

    print(f"\n📄 Reading article: {article_file}")
    article_text = article_file.read_text(encoding="utf-8")
    print(f"   Length: {len(article_text)} characters")
    print("\n" + "=" * 60)

    # 运行 pipeline
    segmentation, results = await process_article(article_text)

    # 输出结果
    print("\n" + "=" * 60)
    print("📊 Results Summary")
    print("=" * 60)

    for i, (intent, selection) in enumerate(zip(segmentation.intents, results)):
        print(f"\n─── Intent {i} ───")
        print(f"  意图: {intent.intent[:80]}{'...' if len(intent.intent) > 80 else ''}")
        print(f"  段落数: {len(intent.paragraphs)}")

        if selection is None:
            print(f"  结果: ❌ Failed")
        elif selection.template is None:
            print(f"  结果: ⏭ Skipped")
        else:
            print(f"  结果: ✅ {selection.category}/{selection.sub_category}")
            print(f"  模板: {selection.template}")
            if selection.data:
                data_str = json.dumps(selection.data, ensure_ascii=False)
                print(f"  数据: {data_str[:100]}{'...' if len(data_str) > 100 else ''}")

    # 统计
    success = sum(1 for r in results if r is not None)
    skipped = sum(1 for r in results if r and r.template is None)
    templates = sum(1 for r in results if r and r.template)

    print("\n" + "=" * 60)
    print(f"📈 Statistics:")
    print(f"   Total: {len(results)} | Success: {success} | Templates: {templates} | Skipped: {skipped}")
    print("=" * 60)

    # Step 3: 渲染 (可选)
    if render and templates > 0:
        print("\n" + "=" * 60)
        print("🎨 Rendering Infographics")
        print("=" * 60)

        out_path = Path(output_dir) if output_dir else (AGENTIC_ROOT.parent.parent.parent / "output")
        svg_outputs = await render_selections(results, out_path)

        rendered = sum(1 for o in svg_outputs if o is not None)
        print("\n" + "=" * 60)
        print(f"🖼  Render Statistics:")
        print(f"   Rendered: {rendered} | Failed: {templates - rendered}")
        print(f"   Output: {out_path}")
        print("=" * 60)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test agentic pipeline")
    parser.add_argument("article", nargs="?", default="example2.md", help="Article file path")
    parser.add_argument("--render", "-r", action="store_true", help="Render to SVG")
    parser.add_argument("--output", "-o", help="Output directory for SVG files")

    args = parser.parse_args()
    asyncio.run(main(args.article, render=args.render, output_dir=args.output))
