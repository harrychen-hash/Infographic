"""
[INPUT]: intent, paragraphs 从 Template Selector 传入
[OUTPUT]: TemplateSelection - 通过调用 chart tools 返回（单次调用）
[POS]: agents/category_agents 的 chart 分类 agent

[PROTOCOL]:
1. 一旦本文件逻辑变更，必须同步更新此 Header。
2. 更新后必须上浮检查 category_agents/.folder.md 的描述是否仍然准确。
"""

from agents import Agent, AgentOutputSchema

from ...models import TemplateSelection
from ...tools.chart_tools import (
    chart_pie,
    chart_bar,
    chart_line,
    chart_column,
    chart_wordcloud,
    chart_combo,
)
from ...tools.common import skip_chart
from ...utils import get_default_model, load_prompt


CHART_AGENT_INSTRUCTIONS = load_prompt("chart_agent")

chart_agent = Agent(
    name="Chart Agent",
    handoff_description="处理数据图表类内容，如占比、趋势、数值对比、双指标组合等",
    instructions=CHART_AGENT_INSTRUCTIONS,
    tools=[chart_pie, chart_bar, chart_line, chart_column, chart_wordcloud, chart_combo, skip_chart],
    tool_use_behavior="stop_on_first_tool",
    output_type=AgentOutputSchema(TemplateSelection, strict_json_schema=False),
    model=get_default_model(),
)
