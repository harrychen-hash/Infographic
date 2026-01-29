"""
[INPUT]: intent, paragraphs 从 category agent 传入
[OUTPUT]: TemplateSelection - 选择的模板和数据
[POS]: agentic/tools 的 chart 分类工具集

[PROTOCOL]:
1. 一旦本文件逻辑变更，必须同步更新此 Header。
2. 更新后必须上浮检查 tools/.folder.md 的描述是否仍然准确。
"""

from __future__ import annotations

import json

from agents import function_tool

from ..models import TemplateSelection


@function_tool
def chart_pie(
    template: str,
    data_json: str,
    rationale: str,
) -> TemplateSelection:
    """选择 chart-pie 类型模板 - 饼图/环形图，展示占比关系。

    ## 可用模板
    - chart-pie-plain-text: 纯文本饼图 (maxItems=6, maxLabelLength=10)
    - chart-pie-compact-card: 紧凑卡片饼图 (maxItems=4, maxLabelLength=8)
    - chart-pie-donut-plain-text: 环形图纯文本 (maxItems=6, maxLabelLength=10)
    - chart-pie-donut-pill-badge: 环形图胶囊徽章 (maxItems=5, maxLabelLength=8)

    ## 适用场景
    - 占比关系、部分与整体
    - 百分比数据（各项之和=100%）
    - 市场份额、预算分配

    ## 不适用场景
    - 趋势变化（用 chart-line）
    - 数值大小对比（用 chart-bar）
    - 时间序列数据
    - 超过 6 个分类
    - 定性描述（用 list）

    ## 与其他 chart 类型的区别
    - chart-pie: 占比关系，各项相加=100%
    - chart-bar: 数值大小对比，横向条形
    - chart-line: 趋势变化，连续数据
    - chart-column: 分类对比，纵向柱状
    - chart-wordcloud: 词频展示，关键词云

    ## 数据格式
    {"values": [{"label": "分类名", "value": 数值, "desc": "描述(可选)"}]}

    Args:
        template: 模板名称，必须是: chart-pie-plain-text | chart-pie-compact-card | chart-pie-donut-plain-text | chart-pie-donut-pill-badge
        data_json: JSON 字符串，格式为 {"values": [{"label": "苹果", "value": 30}, {"label": "香蕉", "value": 25}]}，label 和 value 必填，desc 可选
        rationale: 选择该模板的理由，简述为什么饼图适合当前内容
    """
    return TemplateSelection(
        category="chart",
        sub_category="chart-pie",
        template=template,
        data=json.loads(data_json),
        rationale=rationale,
    )


@function_tool
def chart_bar(
    template: str,
    data_json: str,
    rationale: str,
) -> TemplateSelection:
    """选择 chart-bar 类型模板 - 横向条形图，展示数值大小对比。

    ## 可用模板
    - chart-bar-plain-text: 纯文本条形图 (maxItems=10, maxLabelLength=15)

    ## 适用场景
    - 类别对比、排名展示
    - 数值大小对比
    - 需要 >=2 个数值数据点

    ## 不适用场景
    - 时间序列（用 chart-line）
    - 占比数据（用 chart-pie）
    - 趋势变化
    - 定性描述、单一数值

    ## 与其他 chart 类型的区别
    - chart-bar: 横向条形，适合较长标签，强调排名
    - chart-column: 纵向柱状，适合短标签，强调对比
    - chart-pie: 占比关系
    - chart-line: 连续趋势

    ## 数据格式
    {"values": [{"label": "类别名", "value": 数值, "desc": "描述(可选)"}]}

    Args:
        template: 模板名称，必须是: chart-bar-plain-text
        data_json: JSON 字符串，格式为 {"values": [{"label": "产品A", "value": 85}, {"label": "产品B", "value": 72}]}，label 和 value 必填，desc 可选
        rationale: 选择该模板的理由，简述为什么条形图适合当前内容
    """
    return TemplateSelection(
        category="chart",
        sub_category="chart-bar",
        template=template,
        data=json.loads(data_json),
        rationale=rationale,
    )


@function_tool
def chart_line(
    template: str,
    data_json: str,
    rationale: str,
) -> TemplateSelection:
    """选择 chart-line 类型模板 - 折线图，展示趋势变化。

    ## 可用模板
    - chart-line-plain-text: 纯文本折线图 (maxItems=12, maxLabelLength=8)

    ## 适用场景
    - 趋势变化、时间序列
    - 连续数据、>=3 个有序数据点
    - 上升或下降趋势展示

    ## 不适用场景
    - 类别对比（用 chart-bar）
    - 占比数据（用 chart-pie）
    - 无顺序数据
    - 定性描述、<3 个数据点

    ## 与其他 chart 类型的区别
    - chart-line: 连续趋势，数据点用线连接
    - chart-bar/column: 离散对比
    - chart-pie: 占比关系

    ## 数据格式
    {"values": [{"label": "时间点", "value": 数值, "desc": "描述(可选)"}]}

    Args:
        template: 模板名称，必须是: chart-line-plain-text
        data_json: JSON 字符串，格式为 {"values": [{"label": "Q1", "value": 100}, {"label": "Q2", "value": 150}, {"label": "Q3", "value": 180}]}，label 和 value 必填，desc 可选
        rationale: 选择该模板的理由，简述为什么折线图适合当前内容
    """
    return TemplateSelection(
        category="chart",
        sub_category="chart-line",
        template=template,
        data=json.loads(data_json),
        rationale=rationale,
    )


@function_tool
def chart_column(
    template: str,
    data_json: str,
    rationale: str,
) -> TemplateSelection:
    """选择 chart-column 类型模板 - 纵向柱状图，展示分类数据对比。

    ## 可用模板
    - chart-column-simple: 简洁柱状图 (maxItems=8, maxLabelLength=8)

    ## 适用场景
    - 数值对比、离散时间点
    - 类别对比
    - 需要 >=2 个数值数据点

    ## 不适用场景
    - 连续趋势（用 chart-line）
    - 占比数据（用 chart-pie）
    - 定性描述
    - 标签过长（用 chart-bar）

    ## 与其他 chart 类型的区别
    - chart-column: 纵向柱状，适合短标签
    - chart-bar: 横向条形，适合长标签
    - chart-line: 连续趋势
    - chart-pie: 占比关系

    ## 数据格式
    {"values": [{"label": "类别名", "value": 数值, "desc": "描述(可选)"}]}

    Args:
        template: 模板名称，必须是: chart-column-simple
        data_json: JSON 字符串，格式为 {"values": [{"label": "2022", "value": 85}, {"label": "2023", "value": 92}]}，label 和 value 必填，desc 可选
        rationale: 选择该模板的理由，简述为什么柱状图适合当前内容
    """
    return TemplateSelection(
        category="chart",
        sub_category="chart-column",
        template=template,
        data=json.loads(data_json),
        rationale=rationale,
    )


@function_tool
def chart_wordcloud(
    template: str,
    data_json: str,
    rationale: str,
) -> TemplateSelection:
    """选择 chart-wordcloud 类型模板 - 词云图，展示关键词频率。

    ## 可用模板
    - chart-wordcloud: 标准词云 (maxItems=30, maxLabelLength=10)
    - chart-wordcloud-rotate: 旋转词云

    ## 适用场景
    - 关键词频率、词频统计
    - 主题分布、>=5 个词语
    - 视觉丰富的展示

    ## 不适用场景
    - 精确数值对比
    - 趋势变化
    - 少于 5 个词
    - 需要精确排名

    ## 与其他 chart 类型的区别
    - chart-wordcloud: 词语大小表示频率，适合关键词展示
    - chart-bar: 精确数值对比
    - chart-pie: 占比关系

    ## 数据格式
    {"values": [{"label": "关键词", "value": 权重数值}]}

    Args:
        template: 模板名称，必须是: chart-wordcloud | chart-wordcloud-rotate
        data_json: JSON 字符串，格式为 {"values": [{"label": "AI", "value": 100}, {"label": "机器学习", "value": 80}, {"label": "深度学习", "value": 60}]}，label 和 value 必填
        rationale: 选择该模板的理由，简述为什么词云图适合当前内容
    """
    return TemplateSelection(
        category="chart",
        sub_category="chart-wordcloud",
        template=template,
        data=json.loads(data_json),
        rationale=rationale,
    )
