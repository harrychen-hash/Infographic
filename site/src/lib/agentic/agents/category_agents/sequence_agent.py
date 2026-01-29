"""
[INPUT]: intent, paragraphs 从 Template Selector 传入
[OUTPUT]: TemplateSelection - 通过调用 sequence tools 返回
[POS]: agents/category_agents 的 sequence 分类 agent

[PROTOCOL]:
1. 一旦本文件逻辑变更，必须同步更新此 Header。
2. 更新后必须上浮检查 category_agents/.folder.md 的描述是否仍然准确。
"""

from agents import Agent

from ...tools.sequence_tools import (
    sequence_stairs,
    sequence_timeline,
    sequence_steps,
    sequence_snake,
    sequence_circular,
    sequence_funnel,
    sequence_roadmap,
    sequence_zigzag,
)
from ...tools.common import skip_sequence
from ...utils import get_default_model

SEQUENCE_AGENT_INSTRUCTIONS = """你是时序流程专家。根据用户提供的意图和段落内容，选择最合适的时序模板类型并提取数据。

## 你的工具

1. **sequence_stairs** - 阶梯流程，适合逐步递进的过程
2. **sequence_timeline** - 时间线，适合按时间顺序展示事件
3. **sequence_steps** - 步骤流程，适合展示操作步骤
4. **sequence_snake** - 蛇形流程，适合弯曲的步骤展示
5. **sequence_circular** - 循环流程，适合展示循环往复的过程
6. **sequence_funnel** - 漏斗图，适合展示逐步筛选的过程
7. **sequence_roadmap** - 路线图，适合展示规划和里程碑
8. **sequence_zigzag** - 锯齿流程，适合交替排列的步骤

## 选择原则

1. 递进式过程 → stairs
2. 时间顺序 → timeline
3. 操作步骤 → steps
4. 多步骤需要省空间 → snake/zigzag
5. 循环过程 → circular
6. 筛选/转化 → funnel
7. 规划/里程碑 → roadmap

## 数据格式

```json
{
  "steps": [
    {"title": "步骤1", "description": "描述"},
    {"title": "步骤2", "description": "描述"}
  ]
}
```

## 输出

调用一个工具，传入 template、data、rationale。
"""

sequence_agent = Agent(
    name="Sequence Agent",
    handoff_description="处理时序流程类内容，如步骤、阶段、时间线、里程碑、漏斗等",
    instructions=SEQUENCE_AGENT_INSTRUCTIONS,
    tools=[
        sequence_stairs,
        sequence_timeline,
        sequence_steps,
        sequence_snake,
        sequence_circular,
        sequence_funnel,
        sequence_roadmap,
        sequence_zigzag,
        skip_sequence,
    ],
    tool_use_behavior="stop_on_first_tool",
    model=get_default_model(),
)
