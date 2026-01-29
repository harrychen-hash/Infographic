"""
[INPUT]: intent, paragraphs 从 Template Selector 传入
[OUTPUT]: TemplateSelection - 通过调用 relation tools 返回
[POS]: agents/category_agents 的 relation 分类 agent

[PROTOCOL]:
1. 一旦本文件逻辑变更，必须同步更新此 Header。
2. 更新后必须上浮检查 category_agents/.folder.md 的描述是否仍然准确。
"""

from agents import Agent

from ...tools.relation_tools import (
    relation_dagre_flow,
    relation_circle,
)
from ...tools.common import skip_relation
from ...utils import get_default_model

RELATION_AGENT_INSTRUCTIONS = """你是关系图专家。根据用户提供的意图和段落内容，选择最合适的关系模板类型并提取数据。

## 你的工具

1. **relation_dagre_flow** - 流程关系图，适合展示有向流程和依赖关系
2. **relation_circle** - 环形关系图，适合展示循环或围绕关系

## 选择原则

1. 有向流程、依赖关系 → dagre_flow
2. 循环、围绕中心的关系 → circle

## 数据格式

流程图:
```json
{
  "nodes": [{"id": "1", "label": "节点1"}, ...],
  "edges": [{"source": "1", "target": "2", "label": "关系"}, ...]
}
```

## 输出

调用一个工具，传入 template、data、rationale。
"""

relation_agent = Agent(
    name="Relation Agent",
    handoff_description="处理关系图类内容，如流程依赖、网络关系、循环系统等",
    instructions=RELATION_AGENT_INSTRUCTIONS,
    tools=[relation_dagre_flow, relation_circle, skip_relation],
    tool_use_behavior="stop_on_first_tool",
    model=get_default_model(),
)
