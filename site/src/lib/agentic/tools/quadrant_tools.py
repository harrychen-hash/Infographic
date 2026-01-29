"""
[INPUT]: intent, paragraphs 从 category agent 传入
[OUTPUT]: TemplateSelection - 选择的模板和数据
[POS]: agentic/tools 的 quadrant 分类工具集

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
def quadrant_quarter(
    template: str,
    data_json: str,
    rationale: str,
) -> TemplateSelection:
    """选择 quadrant-quarter 类型模板 - 四象限图，按两个维度分成四个区域。

    ## 可用模板
    - quadrant-quarter-simple-card: 简洁卡片四象限 (每象限 maxItems=4)
    - quadrant-quarter-circular: 环形四象限 (每象限 maxItems=3)

    ## 适用场景
    - 两个维度的分类分析
    - 重要-紧急矩阵（艾森豪威尔矩阵）
    - 风险-收益分析
    - 技术成熟度 vs 市场需求
    - BCG 矩阵

    ## 不适用场景
    - SWOT 分析（用 compare-swot）
    - 简单的列表分类（用 list）
    - 线性流程（用 sequence）

    ## 与 quadrant-simple 的区别
    - quadrant-quarter: 强调两个维度的坐标轴，适合定位分析
    - quadrant-simple: 简单四格展示，不强调坐标维度

    ## 与 compare-quadrant 的区别
    - quadrant: 独立的象限分类，用于通用四象限分析
    - compare-quadrant: 在 comparison 类别下，更强调对比

    ## 数据格式
    {"xAxis": "维度1名称", "yAxis": "维度2名称", "quadrants": [{"title": "高优先", "items": ["任务1", "任务2"]}]}

    Args:
        template: 模板名称，必须是: quadrant-quarter-simple-card | quadrant-quarter-circular
        data_json: JSON 字符串，格式为 {"xAxis": "重要性", "yAxis": "紧急性", "quadrants": [{"title": "立即处理", "items": ["任务1"]}, {"title": "计划执行", "items": ["任务2"]}, {"title": "委托他人", "items": ["任务3"]}, {"title": "暂时搁置", "items": ["任务4"]}]}
        rationale: 选择该模板的理由，简述为什么四象限分析适合当前内容
    """
    return TemplateSelection(
        category="quadrant",
        sub_category="quadrant-quarter",
        template=template,
        data=json.loads(data_json),
        rationale=rationale,
    )


@function_tool
def quadrant_simple(
    template: str,
    data_json: str,
    rationale: str,
) -> TemplateSelection:
    """选择 quadrant-simple 类型模板 - 简单象限图，基础的四格展示。

    ## 可用模板
    - quadrant-simple-illus: 简洁插图象限 (每象限 maxItems=4)

    ## 适用场景
    - 简单四分类展示
    - 不需要强调坐标维度
    - 四个并列的分类
    - 2x2 网格展示

    ## 不适用场景
    - 需要强调两个维度的分析（用 quadrant-quarter）
    - SWOT 分析（用 compare-swot）
    - 超过 4 个分类（用 list-grid）

    ## 与 quadrant-quarter 的区别
    - quadrant-simple: 简单四格，不强调坐标轴
    - quadrant-quarter: 强调 X/Y 轴维度

    ## 数据格式
    {"quadrants": [{"title": "分类1", "items": ["项目1", "项目2"]}]}

    Args:
        template: 模板名称，必须是: quadrant-simple-illus
        data_json: JSON 字符串，格式为 {"quadrants": [{"title": "类别A", "items": ["项目1"]}, {"title": "类别B", "items": ["项目2"]}, {"title": "类别C", "items": ["项目3"]}, {"title": "类别D", "items": ["项目4"]}]}，必须 4 个象限
        rationale: 选择该模板的理由，简述为什么简单象限适合当前内容
    """
    return TemplateSelection(
        category="quadrant",
        sub_category="quadrant-simple",
        template=template,
        data=json.loads(data_json),
        rationale=rationale,
    )
