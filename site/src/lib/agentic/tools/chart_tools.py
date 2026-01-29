"""
[INPUT]: intent, paragraphs 从 category agent 传入
[OUTPUT]: TemplateSelection - 选择的模板和数据
[POS]: agentic/tools 的 chart 分类工具集

[PROTOCOL]:
1. 一旦本文件逻辑变更，必须同步更新此 Header。
2. 更新后必须上浮检查 tools/.folder.md 的描述是否仍然准确。
"""

from __future__ import annotations

from typing import Literal

from agents import function_tool

from ..models import TemplateSelection
from .common import log_tool_call, parse_data_json, validate_list_field


# Type aliases for template parameters
ChartPieTemplate = Literal[
    "chart-pie-plain-text"
]

ChartBarTemplate = Literal["chart-bar-plain-text"]

ChartLineTemplate = Literal["chart-line-plain-text"]

ChartColumnTemplate = Literal["chart-column-simple"]

ChartWordcloudTemplate = Literal["chart-wordcloud"]


@function_tool
def chart_pie(
    template: ChartPieTemplate,
    data_json: str,
    rationale: str,
) -> TemplateSelection:
    """选择 chart-pie 类型模板 - 饼图/环形图，展示占比关系。

    ## 可用模板
    - 由对应的 Literal 类型定义（与 getTemplates 对齐）

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
    {"title": "<可选标题>", "values": [{"label": "<分类名>", "value": <数值>, "desc": "<可选描述>"}...]}

    Args:
        template: 模板名称（必填），取值由对应的 Literal 类型定义
        data_json: JSON 字符串（必填）。
            格式: {"title": "<可选标题>", "values": [{"label": "<名称>", "value": <数值>, "desc": "<可选描述>"}...]}
            规则:
            - title 可选，用于图表标题（如"2023年市场份额"）
            - label 必须从段落提取真实内容，禁止 A/B/C、类别1/类别2 等占位符
            - label 要极简：用名词，去掉多余修饰（如"研发"而非"研发部门"）
            - label 不超过10个字符
            - label 语种必须与输入段落一致（中文输入→中文label）
            - value 必须是数值，各项之和应约等于100
            - values 数组 3-6 项
            示例1: {"values": [{"label": "苹果", "value": 45}, {"label": "三星", "value": 35}, {"label": "其他", "value": 20}]}
            示例2: {"title": "部门预算占比", "values": [{"label": "研发", "value": 35}, {"label": "销售", "value": 25}, {"label": "运营", "value": 20}, {"label": "行政", "value": 15}, {"label": "其他", "value": 5}]}
            示例3: {"values": [{"label": "移动端", "value": 55, "desc": "手机+平板"}, {"label": "桌面端", "value": 30}, {"label": "其他", "value": 15}]}
        rationale: 选择该模板的理由（必填）
    """
    data = parse_data_json(data_json)
    log_tool_call("chart_pie", template, data_json, rationale, data)
    ok, reason = validate_list_field(data, "values", min_len=2)
    if not ok:
        return TemplateSelection(
            category="chart",
            sub_category="chart-pie",
            template=None,
            data=None,
            rationale=f"数据不完整，无法渲染饼图：{reason}",
        )
    return TemplateSelection(
        category="chart",
        sub_category="chart-pie",
        template=template,
        data=data,
        rationale=rationale,
    )


@function_tool
def chart_bar(
    template: ChartBarTemplate,
    data_json: str,
    rationale: str,
) -> TemplateSelection:
    """选择 chart-bar 类型模板 - 横向条形图，展示数值大小对比。

    ## 可用模板
    - 由对应的 Literal 类型定义（与 getTemplates 对齐）

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
    {"title": "<可选标题>", "values": [{"label": "<类别名>", "value": <数值>, "desc": "<可选描述>"}...]}

    Args:
        template: 模板名称（必填），取值由对应的 Literal 类型定义
        data_json: JSON 字符串（必填）。
            格式: {"title": "<可选标题>", "values": [{"label": "<类别名>", "value": <数值>, "desc": "<可选描述>"}...]}
            规则:
            - title 可选，用于图表标题（如"城市GDP排名"）
            - label 必须从段落提取真实内容，禁止 A/B/C、类别1/类别2 等占位符
            - label 要极简：用名词，去掉多余修饰（如"上海"而非"上海市"）
            - label 不超过15个字符
            - label 语种必须与输入段落一致（中文输入→中文label）
            - value 必须是数值
            - values 数组 3-10 项，按数值从大到小排序
            示例1: {"values": [{"label": "上海", "value": 4.32}, {"label": "北京", "value": 4.03}, {"label": "深圳", "value": 3.24}]}
            示例2: {"title": "用户偏好排名", "values": [{"label": "性能", "value": 92}, {"label": "价格", "value": 85}, {"label": "外观", "value": 78}, {"label": "售后", "value": 65}]}
            示例3: {"values": [{"label": "深圳", "value": 120, "desc": "华南区"}, {"label": "上海", "value": 115, "desc": "华东区"}, {"label": "北京", "value": 98, "desc": "华北区"}]}
        rationale: 选择该模板的理由（必填）
    """
    data = parse_data_json(data_json)
    log_tool_call("chart_bar", template, data_json, rationale, data)
    ok, reason = validate_list_field(data, "values", min_len=2)
    if not ok:
        return TemplateSelection(
            category="chart",
            sub_category="chart-bar",
            template=None,
            data=None,
            rationale=f"数据不完整，无法渲染条形图：{reason}",
        )
    return TemplateSelection(
        category="chart",
        sub_category="chart-bar",
        template=template,
        data=data,
        rationale=rationale,
    )


@function_tool
def chart_line(
    template: ChartLineTemplate,
    data_json: str,
    rationale: str,
) -> TemplateSelection:
    """选择 chart-line 类型模板 - 折线图，展示趋势变化。

    ## 可用模板
    - 由对应的 Literal 类型定义（与 getTemplates 对齐）

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
    {"title": "<可选标题>", "values": [{"label": "<时间点>", "value": <数值>, "desc": "<可选描述>"}...]}

    Args:
        template: 模板名称（必填），取值由对应的 Literal 类型定义
        data_json: JSON 字符串（必填）。
            格式: {"title": "<可选标题>", "values": [{"label": "<时间点>", "value": <数值>, "desc": "<可选描述>"}...]}
            规则:
            - title 可选，用于图表标题（如"营收增长趋势"）
            - label 必须从段落提取真实时间点，禁止 A/B/C 等占位符
            - label 要极简：用简短时间标识（如"2023"而非"2023年度"）
            - label 不超过8个字符
            - label 语种必须与输入段落一致
            - value 必须是数值
            - values 数组 3-12 项，按时间顺序排列
            示例1: {"values": [{"label": "Q1", "value": 85}, {"label": "Q2", "value": 92}, {"label": "Q3", "value": 78}, {"label": "Q4", "value": 105}]}
            示例2: {"title": "年度营收", "values": [{"label": "2020", "value": 50}, {"label": "2021", "value": 65}, {"label": "2022", "value": 82}, {"label": "2023", "value": 100}]}
            示例3: {"values": [{"label": "1月", "value": 1000}, {"label": "2月", "value": 600}, {"label": "3月", "value": 1200}]}
        rationale: 选择该模板的理由（必填）
    """
    data = parse_data_json(data_json)
    log_tool_call("chart_line", template, data_json, rationale, data)
    ok, reason = validate_list_field(data, "values", min_len=2)
    if not ok:
        return TemplateSelection(
            category="chart",
            sub_category="chart-line",
            template=None,
            data=None,
            rationale=f"数据不完整，无法渲染折线图：{reason}",
        )
    return TemplateSelection(
        category="chart",
        sub_category="chart-line",
        template=template,
        data=data,
        rationale=rationale,
    )


@function_tool
def chart_column(
    template: ChartColumnTemplate,
    data_json: str,
    rationale: str,
) -> TemplateSelection:
    """选择 chart-column 类型模板 - 纵向柱状图，展示分类数据对比。

    ## 可用模板
    - 由对应的 Literal 类型定义（与 getTemplates 对齐）

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
    {"title": "<可选标题>", "values": [{"label": "<类别名>", "value": <数值>, "desc": "<可选描述>"}...]}

    Args:
        template: 模板名称（必填），取值由对应的 Literal 类型定义
        data_json: JSON 字符串（必填）。
            格式: {"title": "<可选标题>", "values": [{"label": "<类别名>", "value": <数值>, "desc": "<可选描述>"}...]}
            规则:
            - title 可选，用于图表标题（如"部门人数"）
            - label 必须从段落提取真实类别，禁止 A/B/C、类别1/类别2 等占位符
            - label 要极简：用名词，去掉多余修饰（如"研发"而非"研发部门"）
            - label 不超过8个字符
            - label 语种必须与输入段落一致（中文输入→中文label）
            - value 必须是数值
            - values 数组 3-8 项
            示例1: {"values": [{"label": "研发", "value": 120}, {"label": "销售", "value": 85}, {"label": "运营", "value": 45}, {"label": "行政", "value": 30}]}
            示例2: {"title": "产品销量", "values": [{"label": "A产品", "value": 5000}, {"label": "B产品", "value": 3200}, {"label": "C产品", "value": 2800}]}
            示例3: {"values": [{"label": "华东", "value": 1.2, "desc": "上海为主"}, {"label": "华南", "value": 0.9}, {"label": "华北", "value": 0.85}]}
        rationale: 选择该模板的理由（必填）
    """
    data = parse_data_json(data_json)
    log_tool_call("chart_column", template, data_json, rationale, data)
    ok, reason = validate_list_field(data, "values", min_len=2)
    if not ok:
        return TemplateSelection(
            category="chart",
            sub_category="chart-column",
            template=None,
            data=None,
            rationale=f"数据不完整，无法渲染柱状图：{reason}",
        )
    return TemplateSelection(
        category="chart",
        sub_category="chart-column",
        template=template,
        data=data,
        rationale=rationale,
    )


@function_tool
def chart_wordcloud(
    template: ChartWordcloudTemplate,
    data_json: str,
    rationale: str,
) -> TemplateSelection:
    """选择 chart-wordcloud 类型模板 - 词云图，展示关键词频率。

    ## 可用模板
    - 由对应的 Literal 类型定义（与 getTemplates 对齐）

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
    {"title": "<可选标题>", "values": [{"label": "<关键词>", "value": <权重数值>}...]}

    Args:
        template: 模板名称（必填），取值由对应的 Literal 类型定义
        data_json: JSON 字符串（必填）。
            格式: {"title": "<可选标题>", "values": [{"label": "<关键词>", "value": <权重>}...]}
            规则:
            - title 可选，用于图表标题（如"技术热词"）
            - label 必须从段落提取真实关键词，禁止占位符
            - label 要极简：用核心词汇（如"AI"而非"人工智能技术"）
            - label 不超过10个字符
            - label 语种必须与输入段落一致
            - value 表示权重/频率，数值越大词越突出
            - values 数组 5-30 项，词语越多效果越好
            示例1: {"values": [{"label": "AI", "value": 100}, {"label": "大数据", "value": 85}, {"label": "云计算", "value": 72}, {"label": "区块链", "value": 55}, {"label": "物联网", "value": 42}]}
            示例2: {"title": "用户评价", "values": [{"label": "好用", "value": 100}, {"label": "便宜", "value": 90}, {"label": "快速", "value": 80}, {"label": "稳定", "value": 70}, {"label": "简洁", "value": 60}, {"label": "美观", "value": 50}]}
            示例3: {"values": [{"label": "数字化", "value": 100}, {"label": "智能制造", "value": 90}, {"label": "绿色低碳", "value": 80}, {"label": "可持续", "value": 70}]}
        rationale: 选择该模板的理由（必填）
    """
    data = parse_data_json(data_json)
    log_tool_call("chart_wordcloud", template, data_json, rationale, data)
    ok, reason = validate_list_field(data, "values", min_len=3)
    if not ok:
        return TemplateSelection(
            category="chart",
            sub_category="chart-wordcloud",
            template=None,
            data=None,
            rationale=f"数据不完整，无法渲染词云：{reason}",
        )
    return TemplateSelection(
        category="chart",
        sub_category="chart-wordcloud",
        template=template,
        data=data,
        rationale=rationale,
    )
