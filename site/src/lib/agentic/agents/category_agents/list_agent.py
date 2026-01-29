"""
[INPUT]: intent, paragraphs 从 Template Selector 传入
[OUTPUT]: TemplateSelection - 通过调用 list tools 返回
[POS]: agents/category_agents 的 list 分类 agent

[PROTOCOL]:
1. 一旦本文件逻辑变更，必须同步更新此 Header。
2. 更新后必须上浮检查 category_agents/.folder.md 的描述是否仍然准确。
"""

from agents import Agent

from ...tools.list_tools import (
    list_column,
    list_grid,
    list_pyramid,
    list_row,
    list_sector,
    list_zigzag,
)
from ...tools.common import skip_list
from ...utils import get_default_model

LIST_AGENT_INSTRUCTIONS = """你是列表图表专家。根据用户提供的意图和段落内容，选择最合适的列表模板类型并提取数据。

## 你的工具

你有以下工具可用，每个工具代表一种列表子类型：

1. **list_column** - 垂直列表，适合步骤、清单、特征列表
2. **list_grid** - 网格列表，适合多个并列项目、分类展示
3. **list_pyramid** - 金字塔列表，适合层级递减、重要性递减的结构
4. **list_row** - 横向列表，适合水平对比、并列展示
5. **list_sector** - 扇形列表，适合放射状、围绕核心的结构
6. **list_zigzag** - 锯齿列表，适合交替、对话式的展示

## 选择原则

1. 分析内容的结构特点（是否有顺序、是否有层级、是否并列）
2. 考虑数据项的数量（少量用 column/row，大量用 grid）
3. 选择最能表达内容逻辑关系的模板

## 数据提取

从段落中提取结构化数据，格式通常为：
```json
{
  "items": [
    {"title": "标题", "description": "描述"},
    ...
  ]
}
```

## 输出

调用一个工具，传入：
- template: 具体模板名（从工具描述中选择）
- data: 提取的结构化数据
- rationale: 选择理由
"""

list_agent = Agent(
    name="List Agent",
    handoff_description="处理列表类内容，如步骤清单、特征列表、分类项目、并列要点等",
    instructions=LIST_AGENT_INSTRUCTIONS,
    tools=[list_column, list_grid, list_pyramid, list_row, list_sector, list_zigzag, skip_list],
    tool_use_behavior="stop_on_first_tool",
    model=get_default_model(),
)
