"""
[INPUT]: intent, paragraphs 从 Template Selector 传入
[OUTPUT]: TemplateSelection - 通过调用 hierarchy tools 返回
[POS]: agents/category_agents 的 hierarchy 分类 agent

[PROTOCOL]:
1. 一旦本文件逻辑变更，必须同步更新此 Header。
2. 更新后必须上浮检查 category_agents/.folder.md 的描述是否仍然准确。
"""

from agents import Agent

from ...tools.hierarchy_tools import (
    hierarchy_tree,
    hierarchy_mindmap,
    hierarchy_structure,
)
from ...tools.common import skip_hierarchy
from ...utils import get_default_model

HIERARCHY_AGENT_INSTRUCTIONS = """你是层级结构专家。根据用户提供的意图和段落内容，选择最合适的层级模板类型并提取数据。

## 你的工具

1. **hierarchy_tree** - 树状图，适合展示层级和分支关系
2. **hierarchy_mindmap** - 思维导图，适合展示发散性思维和关联
3. **hierarchy_structure** - 组织架构图，适合展示组织层级

## 选择原则

1. 有明确的父子层级关系 → tree
2. 中心发散、关联思维 → mindmap
3. 组织/机构架构 → structure

## 数据格式

```json
{
  "root": {
    "label": "根节点",
    "children": [
      {"label": "子节点1", "children": [...]},
      {"label": "子节点2"}
    ]
  }
}
```

## 输出

调用一个工具，传入 template、data、rationale。
"""

hierarchy_agent = Agent(
    name="Hierarchy Agent",
    handoff_description="处理层级结构类内容，如组织架构、分类体系、树状关系、思维导图等",
    instructions=HIERARCHY_AGENT_INSTRUCTIONS,
    tools=[hierarchy_tree, hierarchy_mindmap, hierarchy_structure, skip_hierarchy],
    tool_use_behavior="stop_on_first_tool",
    model=get_default_model(),
)
