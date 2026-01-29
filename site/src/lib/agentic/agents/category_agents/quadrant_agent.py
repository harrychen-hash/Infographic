"""
[INPUT]: intent, paragraphs 从 Template Selector 传入
[OUTPUT]: TemplateSelection - 通过调用 quadrant tools 返回
[POS]: agents/category_agents 的 quadrant 分类 agent

[PROTOCOL]:
1. 一旦本文件逻辑变更，必须同步更新此 Header。
2. 更新后必须上浮检查 category_agents/.folder.md 的描述是否仍然准确。
"""

from agents import Agent

from ...tools.quadrant_tools import (
    quadrant_quarter,
    quadrant_simple,
)
from ...tools.common import skip_quadrant
from ...utils import get_default_model

QUADRANT_AGENT_INSTRUCTIONS = """你是象限图专家。根据用户提供的意图和段落内容，选择最合适的象限模板类型并提取数据。

## 你的工具

1. **quadrant_quarter** - 四象限图，适合按两个维度分成四个区域
2. **quadrant_simple** - 简单象限图，适合基础的象限展示

## 选择原则

1. 有明确的两个维度（如重要/紧急、风险/收益） → quarter
2. 简单的四分类 → simple

## 数据格式

```json
{
  "xAxis": "维度1名称",
  "yAxis": "维度2名称",
  "quadrants": [
    {"title": "象限1", "items": [...]},
    {"title": "象限2", "items": [...]},
    {"title": "象限3", "items": [...]},
    {"title": "象限4", "items": [...]}
  ]
}
```

## 输出

调用一个工具，传入 template、data、rationale。
"""

quadrant_agent = Agent(
    name="Quadrant Agent",
    handoff_description="处理象限图类内容，如四象限分析、二维分类、矩阵定位等",
    instructions=QUADRANT_AGENT_INSTRUCTIONS,
    tools=[quadrant_quarter, quadrant_simple, skip_quadrant],
    tool_use_behavior="stop_on_first_tool",
    model=get_default_model(),
)
