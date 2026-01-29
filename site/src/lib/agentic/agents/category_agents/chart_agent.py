"""
[INPUT]: intent, paragraphs 从 Template Selector 传入
[OUTPUT]: TemplateSelection - 通过调用 chart tools 返回
[POS]: agents/category_agents 的 chart 分类 agent

[PROTOCOL]:
1. 一旦本文件逻辑变更，必须同步更新此 Header。
2. 更新后必须上浮检查 category_agents/.folder.md 的描述是否仍然准确。
"""

from agents import Agent

from ...tools.chart_tools import (
    chart_pie,
    chart_bar,
    chart_line,
    chart_column,
    chart_wordcloud,
)
from ...tools.common import skip_chart
from ...utils import get_default_model

CHART_AGENT_INSTRUCTIONS = """你是数据图表专家。根据用户提供的意图和段落内容，选择最合适的图表模板类型并提取数据。

## 你的工具

1. **chart_pie** - 饼图/环形图，适合展示占比、组成部分
2. **chart_bar** - 条形图，适合展示数值大小对比
3. **chart_line** - 折线图，适合展示趋势变化
4. **chart_column** - 柱状图，适合展示分类数据对比
5. **chart_wordcloud** - 词云图，适合展示关键词频率

## 选择原则

1. 占比数据 → pie
2. 大小对比 → bar/column
3. 时间趋势 → line
4. 关键词 → wordcloud

## 数据格式

- 饼图: {"values": [{"label": "...", "value": 数值}]}
- 条形图: {"values": [{"label": "...", "value": 数值}]}
- 词云: {"words": [{"text": "...", "weight": 数值}]}

## 输出

调用一个工具，传入 template、data、rationale。
"""

chart_agent = Agent(
    name="Chart Agent",
    handoff_description="处理数据图表类内容，如占比、趋势、数值对比、关键词统计等",
    instructions=CHART_AGENT_INSTRUCTIONS,
    tools=[chart_pie, chart_bar, chart_line, chart_column, chart_wordcloud, skip_chart],
    tool_use_behavior="stop_on_first_tool",
    model=get_default_model(),
)
