"""
[INPUT]: intent, paragraphs 从 category agent 传入
[OUTPUT]: TemplateSelection - 选择的模板和数据
[POS]: agentic/tools 的 list 分类工具集

[PROTOCOL]:
1. 一旦本文件逻辑变更，必须同步更新此 Header。
2. 更新后必须上浮检查 tools/.folder.md 的描述是否仍然准确。
"""

from __future__ import annotations

import json
import sys

from agents import function_tool

from ..models import TemplateSelection


def _debug_log(tool_name: str, template: str, data_json: str, rationale: str):
    """调试日志：打印 LLM 传给 tool 的参数"""
    print(f"\n[DEBUG] Tool called: {tool_name}", file=sys.stderr)
    print(f"  template: {template}", file=sys.stderr)
    print(f"  data_json: {data_json[:200] if data_json else 'EMPTY'}...", file=sys.stderr)
    print(f"  rationale: {rationale[:100] if rationale else 'EMPTY'}...", file=sys.stderr)


@function_tool
def list_column(
    template: str,
    data_json: str,
    rationale: str,
) -> TemplateSelection:
    """选择 list-column 类型模板 - 垂直排列的列表项。

    ## 可用模板
    - list-column-done-list: 带勾选标记的完成列表 (maxItems=10, maxLabelLength=30)
    - list-column-vertical-icon-arrow: 带图标和箭头的垂直列表 (maxItems=6, maxLabelLength=20)
    - list-column-simple-vertical-arrow: 简洁的垂直箭头列表 (maxItems=8, maxLabelLength=25)

    ## 适用场景
    - 并列要点、特征列举
    - 垂直展示、较长标签
    - 任务清单、检查列表

    ## 不适用场景
    - 顺序关系（用 sequence）
    - 层级结构（用 hierarchy）
    - 时间线

    ## 与其他 list 类型的区别
    - list-column: 单列垂直排列，适合较长标签（maxLabelLength 20-30）
    - list-grid: 网格排列 (2x2, 3x3)，适合短标签
    - list-row: 单行水平排列，适合 3-5 项
    - list-pyramid: 金字塔层级，适合重要性递减
    - list-sector: 扇形放射状，适合围绕中心主题
    - list-zigzag: 锯齿交替，适合视觉变化

    ## 数据格式
    {"lists": [{"label": "项目名", "desc": "描述(可选)", "icon": "图标(可选)"}]}

    Args:
        template: 模板名称，必须是: list-column-done-list | list-column-vertical-icon-arrow | list-column-simple-vertical-arrow
        data_json: JSON 字符串，格式为 {"lists": [{"label": "项目1"}, {"label": "项目2", "desc": "描述"}]}，label 必填，desc 和 icon 可选
        rationale: 选择该模板的理由，简述为什么垂直列表适合当前内容
    """
    _debug_log("list_column", template, data_json, rationale)
    return TemplateSelection(
        category="list",
        sub_category="list-column",
        template=template,
        data=json.loads(data_json),
        rationale=rationale,
    )


@function_tool
def list_grid(
    template: str,
    data_json: str,
    rationale: str,
) -> TemplateSelection:
    """选择 list-grid 类型模板 - 网格/矩阵排列的多个项目。

    ## 可用模板
    - list-grid-badge-card: 徽章卡片网格 (maxItems=9, maxLabelLength=12)
    - list-grid-candy-card-lite: 糖果风格轻量卡片 (maxItems=6, maxLabelLength=10)
    - list-grid-circular-progress: 带进度的环形卡片
    - list-grid-compact-card: 紧凑卡片网格
    - list-grid-done-list: 完成列表网格
    - list-grid-horizontal-icon-arrow: 带图标箭头的水平网格
    - list-grid-progress-card: 进度卡片网格
    - list-grid-ribbon-card: 丝带卡片网格 (maxItems=6, maxLabelLength=12)
    - list-grid-simple: 简洁网格

    ## 适用场景
    - 多维分类、矩阵展示
    - 特征对比、多个独立信息点
    - 2x2, 2x3 或 3x3 布局

    ## 不适用场景
    - 线性流程（用 sequence）
    - 层级关系（用 hierarchy）
    - 时间序列

    ## 与其他 list 类型的区别
    - list-grid: 网格排列，适合 4-9 个短标签项目
    - list-column: 单列垂直，适合长标签
    - list-row: 单行水平，适合 3-5 项

    ## 数据格式
    {"lists": [{"label": "项目名", "desc": "描述(可选)", "icon": "图标(可选)"}]}

    Args:
        template: 模板名称，必须是: list-grid-badge-card | list-grid-candy-card-lite | list-grid-circular-progress | list-grid-compact-card | list-grid-done-list | list-grid-horizontal-icon-arrow | list-grid-progress-card | list-grid-ribbon-card | list-grid-simple
        data_json: JSON 字符串，格式为 {"lists": [{"label": "功能1"}, {"label": "功能2"}, {"label": "功能3"}, {"label": "功能4"}]}，label 必填，desc 和 icon 可选
        rationale: 选择该模板的理由，简述为什么网格列表适合当前内容
    """
    return TemplateSelection(
        category="list",
        sub_category="list-grid",
        template=template,
        data=json.loads(data_json),
        rationale=rationale,
    )


@function_tool
def list_pyramid(
    template: str,
    data_json: str,
    rationale: str,
) -> TemplateSelection:
    """选择 list-pyramid 类型模板 - 层级递减的金字塔结构。

    ## 可用模板
    - list-pyramid-rounded-rect-node: 圆角矩形节点金字塔
    - list-pyramid-badge-card: 徽章卡片金字塔
    - list-pyramid-compact-card: 紧凑卡片金字塔

    ## 适用场景
    - 重要性递减的层级
    - 从多到少的筛选
    - 概念范围从大到小

    ## 不适用场景
    - 平行并列关系（用 list-grid）
    - 时间顺序（用 sequence）
    - 组织架构（用 hierarchy）

    ## 与其他 list 类型的区别
    - list-pyramid: 金字塔形状，上窄下宽，强调层级
    - list-column: 等宽垂直排列
    - list-grid: 网格排列

    ## 数据格式
    {"lists": [{"label": "层级名", "desc": "描述(可选)"}]}

    Args:
        template: 模板名称，必须是: list-pyramid-rounded-rect-node | list-pyramid-badge-card | list-pyramid-compact-card
        data_json: JSON 字符串，格式为 {"lists": [{"label": "顶层"}, {"label": "中层"}, {"label": "底层"}]}，label 必填，desc 可选
        rationale: 选择该模板的理由，简述为什么金字塔列表适合当前内容
    """
    return TemplateSelection(
        category="list",
        sub_category="list-pyramid",
        template=template,
        data=json.loads(data_json),
        rationale=rationale,
    )


@function_tool
def list_row(
    template: str,
    data_json: str,
    rationale: str,
) -> TemplateSelection:
    """选择 list-row 类型模板 - 水平排列的列表项。

    ## 可用模板
    - list-row-horizontal-icon-arrow: 带图标箭头的横向列表 (maxItems=5, maxLabelLength=10)
    - list-row-circular-progress: 带环形进度的横向列表
    - list-row-simple-horizontal-arrow: 简洁横向箭头列表
    - list-row-horizontal-icon-line: 带图标线条的横向列表

    ## 适用场景
    - 并列要点、3-5 个项目
    - 平行的多个特征
    - 无顺序的信息点

    ## 不适用场景
    - 有先后顺序的步骤（用 sequence）
    - 时间线（用 sequence-timeline）
    - 流程（用 sequence）
    - 超过 5 个项目（用 list-grid）

    ## 与其他 list 类型的区别
    - list-row: 单行水平排列，适合 3-5 项短标签
    - list-column: 单列垂直排列，适合长标签
    - list-grid: 网格排列，适合更多项目

    ## 数据格式
    {"lists": [{"label": "项目名", "desc": "描述(可选)", "icon": "图标(可选)"}]}

    Args:
        template: 模板名称，必须是: list-row-horizontal-icon-arrow | list-row-circular-progress | list-row-simple-horizontal-arrow | list-row-horizontal-icon-line
        data_json: JSON 字符串，格式为 {"lists": [{"label": "要点1"}, {"label": "要点2"}, {"label": "要点3"}]}，label 必填，desc 和 icon 可选
        rationale: 选择该模板的理由，简述为什么横向列表适合当前内容
    """
    return TemplateSelection(
        category="list",
        sub_category="list-row",
        template=template,
        data=json.loads(data_json),
        rationale=rationale,
    )


@function_tool
def list_sector(
    template: str,
    data_json: str,
    rationale: str,
) -> TemplateSelection:
    """选择 list-sector 类型模板 - 放射状/扇形排列的项目。

    ## 可用模板
    - list-sector-simple: 简洁扇形列表 (maxItems=6, maxLabelLength=15)
    - list-sector-plain-text: 纯文本扇形列表
    - list-sector-half-plain-text: 半圆纯文本扇形

    ## 适用场景
    - 围绕中心主题
    - 多角度展示
    - 发散思维

    ## 不适用场景
    - 线性流程（用 sequence）
    - 数值对比（用 chart）
    - 时间线

    ## 与其他 list 类型的区别
    - list-sector: 放射状排列，适合围绕中心主题
    - list-row/column: 线性排列
    - list-grid: 网格排列

    ## 数据格式
    {"lists": [{"label": "分支名", "desc": "描述(可选)"}]}

    Args:
        template: 模板名称，必须是: list-sector-simple | list-sector-plain-text | list-sector-half-plain-text
        data_json: JSON 字符串，格式为 {"lists": [{"label": "分支1"}, {"label": "分支2"}, {"label": "分支3"}]}，label 必填，desc 可选
        rationale: 选择该模板的理由，简述为什么扇形列表适合当前内容
    """
    return TemplateSelection(
        category="list",
        sub_category="list-sector",
        template=template,
        data=json.loads(data_json),
        rationale=rationale,
    )


@function_tool
def list_zigzag(
    template: str,
    data_json: str,
    rationale: str,
) -> TemplateSelection:
    """选择 list-zigzag 类型模板 - 交替/锯齿排列的项目。

    ## 可用模板
    - list-zigzag-up-compact-card: 向上锯齿紧凑卡片 (maxItems=6, maxLabelLength=15)
    - list-zigzag-down-compact-card: 向下锯齿紧凑卡片
    - list-zigzag-up-simple: 向上锯齿简洁样式 (maxItems=6, maxLabelLength=20)
    - list-zigzag-down-simple: 向下锯齿简洁样式

    ## 适用场景
    - 视觉丰富的列表
    - 交替展示
    - 多个并列要点

    ## 不适用场景
    - 严格顺序（用 sequence）
    - 数值对比（用 chart）
    - 时间线

    ## 与其他 list 类型的区别
    - list-zigzag: Z字形交替排列，视觉节奏感强
    - list-column: 直线垂直排列
    - list-grid: 网格排列

    ## 数据格式
    {"lists": [{"label": "项目名", "desc": "描述(可选)", "icon": "图标(可选)"}]}

    Args:
        template: 模板名称，必须是: list-zigzag-up-compact-card | list-zigzag-down-compact-card | list-zigzag-up-simple | list-zigzag-down-simple
        data_json: JSON 字符串，格式为 {"lists": [{"label": "项目1"}, {"label": "项目2"}, {"label": "项目3"}]}，label 必填，desc 和 icon 可选
        rationale: 选择该模板的理由，简述为什么锯齿列表适合当前内容
    """
    return TemplateSelection(
        category="list",
        sub_category="list-zigzag",
        template=template,
        data=json.loads(data_json),
        rationale=rationale,
    )
