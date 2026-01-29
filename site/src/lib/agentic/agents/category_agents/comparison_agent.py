"""
[INPUT]: intent, paragraphs 从 Template Selector 传入
[OUTPUT]: TemplateSelection - 通过调用 comparison tools 返回
[POS]: agents/category_agents 的 comparison 分类 agent

[PROTOCOL]:
1. 一旦本文件逻辑变更，必须同步更新此 Header。
2. 更新后必须上浮检查 category_agents/.folder.md 的描述是否仍然准确。
"""

from agents import Agent

from ...tools.comparison_tools import (
    compare_binary,
    compare_hierarchy,
    compare_swot,
    compare_quadrant,
)
from ...tools.common import skip_comparison
from ...utils import get_default_model

COMPARISON_AGENT_INSTRUCTIONS = """你是对比分析专家。根据用户提供的意图和段落内容，选择最合适的对比模板类型并提取数据。

## 你的工具

1. **compare_binary** - 二元对比，适合两方对比（优劣、前后、新旧）
2. **compare_hierarchy** - 层级对比，适合多层级或多分类的对比
3. **compare_swot** - SWOT 分析，适合优势、劣势、机会、威胁分析
4. **compare_quadrant** - 对比象限，适合按两个维度分类对比

## 选择原则

1. 两个事物对比 → binary
2. 多层级/多分类对比 → hierarchy
3. SWOT 分析 → swot
4. 两维度分类 → quadrant

## 数据格式

- 二元对比: {"left": {...}, "right": {...}}
- SWOT: {"strengths": [...], "weaknesses": [...], "opportunities": [...], "threats": [...]}

## 输出

调用一个工具，传入 template、data、rationale。
"""

comparison_agent = Agent(
    name="Comparison Agent",
    handoff_description="处理对比分析类内容，如两方对比、优劣分析、SWOT 分析等",
    instructions=COMPARISON_AGENT_INSTRUCTIONS,
    tools=[compare_binary, compare_hierarchy, compare_swot, compare_quadrant, skip_comparison],
    tool_use_behavior="stop_on_first_tool",
    model=get_default_model(),
)
