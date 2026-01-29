"""
[INPUT]: intent, paragraphs 从 category agent 传入
[OUTPUT]: TemplateSelection - 选择的模板和数据
[POS]: agentic/tools 的 comparison 分类工具集

[PROTOCOL]:
1. 一旦本文件逻辑变更，必须同步更新此 Header。
2. 更新后必须上浮检查 tools/.folder.md 的描述是否仍然准确。
"""

from __future__ import annotations

import json
from typing import Any, Dict

from agents import function_tool

from ..models import TemplateSelection


@function_tool
def compare_binary(
    template: str,
    data_json: str,
    rationale: str,
) -> TemplateSelection:
    """选择 compare-binary 类型模板 - 二元对比，展示两方差异。

    ## 可用模板
    - compare-binary-horizontal-arrow-simple: 箭头分隔简洁对比 (maxItems=5)
    - compare-binary-horizontal-arrow-underline-text: 箭头分隔下划线文本 (maxItems=4)
    - compare-binary-horizontal-arrow-badge-card: 箭头分隔徽章卡片 (maxItems=4)
    - compare-binary-horizontal-arrow-compact-card: 箭头分隔紧凑卡片 (maxItems=4)
    - compare-binary-horizontal-fold-simple: 折叠分隔简洁对比 (maxItems=5)
    - compare-binary-horizontal-fold-underline-text: 折叠分隔下划线文本 (maxItems=4)
    - compare-binary-horizontal-fold-badge-card: 折叠分隔徽章卡片 (maxItems=4)
    - compare-binary-horizontal-fold-compact-card: 折叠分隔紧凑卡片 (maxItems=4)
    - compare-binary-horizontal-vs-simple: VS分隔简洁对比 (maxItems=5)
    - compare-binary-horizontal-vs-underline-text: VS分隔下划线文本 (maxItems=4)
    - compare-binary-horizontal-vs-badge-card: VS分隔徽章卡片 (maxItems=4)
    - compare-binary-horizontal-vs-compact-card: VS分隔紧凑卡片 (maxItems=4)

    ## 适用场景
    - 两方对比（优劣、前后、新旧）
    - A vs B 结构
    - 传统方法 vs 新方法
    - 产品对比、方案对比

    ## 不适用场景
    - 超过 2 方对比（用 compare-hierarchy）
    - SWOT 分析（用 compare-swot）
    - 四象限分析（用 quadrant）
    - 层级对比

    ## 与其他 comparison 类型的区别
    - compare-binary: 严格的两方对比，左右并列
    - compare-hierarchy: 多层级或多分类对比
    - compare-swot: 固定的四维分析（优势/劣势/机会/威胁）
    - compare-quadrant: 按两个维度的四象限分析

    ## 数据格式
    {"compares": [{"label": "左侧标题", "children": ["特性1", "特性2"]}, {"label": "右侧标题", "children": ["特性A", "特性B"]}]}

    注意: 必须恰好 2 个 compare 项，每项包含 label 和 children 数组

    Args:
        template: 模板名称，必须是: compare-binary-horizontal-arrow-simple | compare-binary-horizontal-arrow-underline-text | compare-binary-horizontal-arrow-badge-card | compare-binary-horizontal-arrow-compact-card | compare-binary-horizontal-fold-simple | compare-binary-horizontal-fold-underline-text | compare-binary-horizontal-fold-badge-card | compare-binary-horizontal-fold-compact-card | compare-binary-horizontal-vs-simple | compare-binary-horizontal-vs-underline-text | compare-binary-horizontal-vs-badge-card | compare-binary-horizontal-vs-compact-card
        data_json: JSON 字符串，格式为 {"compares": [{"label": "传统方法", "children": ["手动操作", "效率低"]}, {"label": "新方法", "children": ["自动化", "效率高"]}]}，必须恰好 2 个项，每项包含 label 和 children 数组
        rationale: 选择该模板的理由，简述为什么二元对比适合当前内容
    """
    return TemplateSelection(
        category="comparison",
        sub_category="compare-binary",
        template=template,
        data=json.loads(data_json),
        rationale=rationale,
    )


@function_tool
def compare_hierarchy(
    template: str,
    data_json: str,
    rationale: str,
) -> TemplateSelection:
    """选择 compare-hierarchy 类型模板 - 层级对比，展示多层级差异。

    ## 可用模板
    - compare-hierarchy-left-right-simple: 左右层级简洁对比 (maxItems=4)
    - compare-hierarchy-left-right-compact-card: 左右层级紧凑卡片 (maxItems=3)
    - compare-hierarchy-row-simple: 行式层级简洁对比 (maxItems=5)
    - compare-hierarchy-row-compact-card: 行式层级紧凑卡片 (maxItems=4)

    ## 适用场景
    - 多层级分类对比
    - 多个分类的并列对比
    - 复杂产品特性对比
    - 多方案对比

    ## 不适用场景
    - 简单的二元对比（用 compare-binary）
    - SWOT 分析（用 compare-swot）
    - 四象限分析（用 quadrant）

    ## 与其他 comparison 类型的区别
    - compare-hierarchy: 多层级、多分类，支持复杂结构
    - compare-binary: 严格两方对比，结构简单
    - compare-swot: 固定四维分析

    ## 数据格式
    {"compares": [{"label": "分类名", "children": ["特性1", "特性2"]}]}

    注意: children 是子项数组，可以是字符串或带 label 的对象

    Args:
        template: 模板名称，必须是: compare-hierarchy-left-right-simple | compare-hierarchy-left-right-compact-card | compare-hierarchy-row-simple | compare-hierarchy-row-compact-card
        data_json: JSON 字符串，格式为 {"compares": [{"label": "方案A", "children": ["特性1", "特性2"]}, {"label": "方案B", "children": ["特性3", "特性4"]}]}，每项包含 label 和 children 数组
        rationale: 选择该模板的理由，简述为什么层级对比适合当前内容
    """
    return TemplateSelection(
        category="comparison",
        sub_category="compare-hierarchy",
        template=template,
        data=json.loads(data_json),
        rationale=rationale,
    )


@function_tool
def compare_swot(
    template: str,
    data_json: str,
    rationale: str,
) -> TemplateSelection:
    """选择 compare-swot 类型模板 - SWOT 分析，展示四维评估。

    ## 可用模板
    - compare-swot: 标准 SWOT 分析图 (每维度 maxItems=5)

    ## 适用场景
    - SWOT 分析（优势 Strengths、劣势 Weaknesses、机会 Opportunities、威胁 Threats）
    - 战略分析、企业评估
    - 项目可行性分析
    - 竞争分析

    ## 不适用场景
    - 简单的二元对比（用 compare-binary）
    - 非 SWOT 的四象限（用 quadrant）
    - 多层级对比（用 compare-hierarchy）
    - 时间序列

    ## 与其他 comparison 类型的区别
    - compare-swot: 固定四维结构，内外部/正负面两个维度
    - compare-binary: 两方对比
    - compare-quadrant: 自定义两个维度的四象限
    - quadrant: 更通用的四象限工具

    ## 数据格式
    {"compares": [
      {"label": "优势 (Strengths)", "children": ["优势1", "优势2"]},
      {"label": "劣势 (Weaknesses)", "children": ["劣势1"]},
      {"label": "机会 (Opportunities)", "children": ["机会1"]},
      {"label": "威胁 (Threats)", "children": ["威胁1"]}
    ]}

    注意: 必须恰好 4 个 compare 项，顺序为 S/W/O/T

    Args:
        template: 模板名称，必须是: compare-swot
        data_json: JSON 字符串，格式为 {"compares": [{"label": "优势", "children": ["优势1"]}, {"label": "劣势", "children": ["劣势1"]}, {"label": "机会", "children": ["机会1"]}, {"label": "威胁", "children": ["威胁1"]}]}，必须恰好 4 个项，顺序为 S/W/O/T
        rationale: 选择该模板的理由，简述为什么 SWOT 分析适合当前内容
    """
    return TemplateSelection(
        category="comparison",
        sub_category="compare-swot",
        template=template,
        data=json.loads(data_json),
        rationale=rationale,
    )


@function_tool
def compare_quadrant(
    template: str,
    data_json: str,
    rationale: str,
) -> TemplateSelection:
    """选择 compare-quadrant 类型模板 - 对比象限，按两个维度分类对比。

    ## 可用模板
    - compare-quadrant-quarter-simple-card: 简洁卡片四象限 (每象限 maxItems=4)
    - compare-quadrant-quarter-circular: 环形四象限 (每象限 maxItems=3)
    - compare-quadrant-simple-illus: 简洁插图四象限 (每象限 maxItems=4)

    ## 适用场景
    - 按两个维度分类对比
    - 产品定位矩阵
    - 风险-收益分析
    - 重要-紧急矩阵

    ## 不适用场景
    - SWOT 分析（用 compare-swot）
    - 简单二元对比（用 compare-binary）
    - 层级对比（用 compare-hierarchy）

    ## 与其他 comparison 类型的区别
    - compare-quadrant: 自定义两个维度，灵活的四象限分析
    - compare-swot: 固定的 SWOT 四维
    - quadrant: 更通用的象限工具（在 quadrant 分类下）

    ## 数据格式
    {"xAxis": "维度1", "yAxis": "维度2", "quadrants": [{"title": "象限1", "items": [...]}]}

    Args:
        template: 模板名称，必须是: compare-quadrant-quarter-simple-card | compare-quadrant-quarter-circular | compare-quadrant-simple-illus
        data_json: JSON 字符串，格式为 {"xAxis": "重要性", "yAxis": "紧急性", "quadrants": [{"title": "重要且紧急", "items": ["任务1"]}, {"title": "重要不紧急", "items": ["任务2"]}, {"title": "紧急不重要", "items": ["任务3"]}, {"title": "不重要不紧急", "items": ["任务4"]}]}
        rationale: 选择该模板的理由，简述为什么四象限对比适合当前内容
    """
    return TemplateSelection(
        category="comparison",
        sub_category="compare-quadrant",
        template=template,
        data=json.loads(data_json),
        rationale=rationale,
    )
