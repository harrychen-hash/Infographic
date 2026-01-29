"""
[INPUT]: Intent (意图和段落) 从 pipeline 传入
[OUTPUT]: 通过 handoff 转交给对应的 category sub-agent
[POS]: agents/ 的模板选择入口 agent，决定 handoff 到哪个 category

[PROTOCOL]:
1. 一旦本文件逻辑变更，必须同步更新此 Header。
2. 更新后必须上浮检查 agents/.folder.md 的描述是否仍然准确。
"""

from agents import Agent

from .category_agents import (
    chart_agent,
    comparison_agent,
    hierarchy_agent,
    list_agent,
    quadrant_agent,
    relation_agent,
    sequence_agent,
    skip_agent,
)
from ..utils import get_default_model

TEMPLATE_SELECTOR_INSTRUCTIONS = """你是图表类型选择专家。根据用户提供的意图和段落内容，决定应该使用哪种类型的图表。

## 你的任务

分析输入的意图（intent）和段落内容（paragraphs），判断最适合用哪种图表类型来可视化这些内容，然后转交给对应的专家处理。

## 可用的图表类型

1. **Chart Agent** - 数据图表
   - 适合：占比数据、趋势变化、数值对比、关键词统计
   - 例如：市场份额、销售趋势、各项指标对比

2. **Comparison Agent** - 对比分析
   - 适合：两方对比、优劣分析、SWOT 分析
   - 例如：新旧对比、方案对比、产品对比

3. **Hierarchy Agent** - 层级结构
   - 适合：组织架构、分类体系、树状关系、思维导图
   - 例如：公司架构、知识分类、概念拆解

4. **List Agent** - 列表展示
   - 适合：步骤清单、特征列表、分类项目、并列要点
   - 例如：功能特点、注意事项、优势列表

5. **Quadrant Agent** - 象限图
   - 适合：二维分类、矩阵定位、四象限分析
   - 例如：重要紧急矩阵、风险收益分析

6. **Relation Agent** - 关系图
   - 适合：流程依赖、网络关系、系统架构
   - 例如：数据流程、系统架构、因果关系

7. **Sequence Agent** - 时序流程
   - 适合：步骤流程、时间线、里程碑、漏斗
   - 例如：开发流程、历史时间线、转化漏斗

8. **Skip Agent** - 跳过可视化
   - 适合：纯叙述性内容、引言/结语、过渡段落、缺乏结构化数据
   - 例如：背景介绍、情感抒发、没有任何叙述逻辑或数据支撑

## 决策原则

1. **内容特征优先**：根据内容本身的结构特征选择
2. **意图匹配**：考虑原文想表达的意图
3. **可视化效果**：选择最能清晰表达信息的图表类型
4. **不强求可视化**：如果内容确实不适合任何图表类型，选择 Skip Agent

## 输出

转交给最合适的 Agent 处理。如果内容不适合可视化，转交给 Skip Agent。
"""

template_selector = Agent(
    name="Template Selector",
    instructions=TEMPLATE_SELECTOR_INSTRUCTIONS,
    handoffs=[
        chart_agent,
        comparison_agent,
        hierarchy_agent,
        list_agent,
        quadrant_agent,
        relation_agent,
        sequence_agent,
        skip_agent,
    ],
    model=get_default_model(),
)
