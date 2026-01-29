"""
[INPUT]: intent, paragraphs 从 category agent 传入
[OUTPUT]: TemplateSelection - 选择的模板和数据
[POS]: agentic/tools 的 sequence 分类工具集

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
def sequence_stairs(
    template: str,
    data_json: str,
    rationale: str,
) -> TemplateSelection:
    """选择 sequence-stairs 类型模板 - 阶梯式流程，展示逐步递进的过程。

    ## 可用模板
    - sequence-stairs-front-compact-card: 正面阶梯紧凑卡片 (maxItems=5)
    - sequence-stairs-front-badge-card: 正面阶梯徽章卡片 (maxItems=4)
    - sequence-stairs-front-simple: 正面阶梯简洁样式 (maxItems=6)

    ## 适用场景
    - 逐步递进的过程
    - 能力成长阶梯
    - 级别提升路径
    - 有层次感的步骤

    ## 不适用场景
    - 时间线（用 sequence-timeline）
    - 循环流程（用 sequence-circular）
    - 简单线性步骤（用 sequence-steps）

    ## 与其他 sequence 类型的区别
    - sequence-stairs: 阶梯式，强调层级递进
    - sequence-steps: 简单线性步骤
    - sequence-timeline: 时间轴，强调时间顺序

    ## 数据格式
    {"sequences": [{"label": "步骤名", "desc": "描述(可选)"}]}

    Args:
        template: 模板名称，必须是: sequence-stairs-front-compact-card | sequence-stairs-front-badge-card | sequence-stairs-front-simple
        data_json: JSON 字符串，格式为 {"sequences": [{"label": "初级"}, {"label": "中级"}, {"label": "高级"}]}，label 必填，desc 可选
        rationale: 选择该模板的理由，简述为什么阶梯流程适合当前内容
    """
    return TemplateSelection(
        category="sequence",
        sub_category="sequence-stairs",
        template=template,
        data=json.loads(data_json),
        rationale=rationale,
    )


@function_tool
def sequence_timeline(
    template: str,
    data_json: str,
    rationale: str,
) -> TemplateSelection:
    """选择 sequence-timeline 类型模板 - 时间线，按时间顺序展示事件。

    ## 可用模板
    - sequence-timeline-simple: 简洁时间线 (maxItems=8)
    - sequence-timeline-badge-card: 徽章卡片时间线 (maxItems=6)
    - sequence-timeline-compact-card: 紧凑卡片时间线 (maxItems=6)
    - sequence-timeline-circular-progress: 环形进度时间线 (maxItems=4)
    - sequence-timeline-horizontal-icon-arrow: 水平图标箭头时间线 (maxItems=5)

    ## 适用场景
    - 按时间顺序展示事件
    - 历史发展、版本演进
    - 项目里程碑、产品迭代
    - 有明确时间节点的流程

    ## 不适用场景
    - 无时间顺序的步骤（用 sequence-steps）
    - 循环流程（用 sequence-circular）
    - 递进阶梯（用 sequence-stairs）

    ## 与其他 sequence 类型的区别
    - sequence-timeline: 强调时间顺序，有时间节点
    - sequence-steps: 操作步骤，不强调时间
    - sequence-roadmap: 规划和里程碑，更面向未来

    ## 数据格式
    {"sequences": [{"label": "事件名", "time": "2024-01", "desc": "描述(可选)"}]}

    Args:
        template: 模板名称，必须是: sequence-timeline-simple | sequence-timeline-badge-card | sequence-timeline-compact-card | sequence-timeline-circular-progress | sequence-timeline-horizontal-icon-arrow
        data_json: JSON 字符串，格式为 {"sequences": [{"label": "发布v1.0", "time": "2024-01"}, {"label": "发布v2.0", "time": "2024-06"}]}，label 必填，time 和 desc 可选
        rationale: 选择该模板的理由，简述为什么时间线适合当前内容
    """
    return TemplateSelection(
        category="sequence",
        sub_category="sequence-timeline",
        template=template,
        data=json.loads(data_json),
        rationale=rationale,
    )


@function_tool
def sequence_steps(
    template: str,
    data_json: str,
    rationale: str,
) -> TemplateSelection:
    """选择 sequence-steps 类型模板 - 步骤流程，展示操作步骤。

    ## 可用模板
    - sequence-steps-simple: 简洁步骤 (maxItems=8)
    - sequence-steps-compact-card: 紧凑卡片步骤 (maxItems=6)

    ## 适用场景
    - 操作步骤、使用说明
    - 简单线性流程
    - 教程步骤、指南
    - 3-8 个步骤

    ## 不适用场景
    - 时间线事件（用 sequence-timeline）
    - 递进阶梯（用 sequence-stairs）
    - 超过 8 个步骤（用 sequence-snake）

    ## 与其他 sequence 类型的区别
    - sequence-steps: 最基础的线性步骤
    - sequence-stairs: 阶梯递进
    - sequence-snake/zigzag: 多行展示，适合更多步骤

    ## 数据格式
    {"sequences": [{"label": "步骤名", "desc": "描述(可选)"}]}

    Args:
        template: 模板名称，必须是: sequence-steps-simple | sequence-steps-compact-card
        data_json: JSON 字符串，格式为 {"sequences": [{"label": "步骤1"}, {"label": "步骤2"}, {"label": "步骤3"}]}，label 必填，desc 可选
        rationale: 选择该模板的理由，简述为什么简单步骤适合当前内容
    """
    return TemplateSelection(
        category="sequence",
        sub_category="sequence-steps",
        template=template,
        data=json.loads(data_json),
        rationale=rationale,
    )


@function_tool
def sequence_snake(
    template: str,
    data_json: str,
    rationale: str,
) -> TemplateSelection:
    """选择 sequence-snake 类型模板 - 蛇形流程，弯曲的步骤展示。

    ## 可用模板
    - sequence-snake-steps-simple: 简洁蛇形步骤 (maxItems=10)
    - sequence-snake-steps-badge-card: 徽章卡片蛇形步骤 (maxItems=8)
    - sequence-snake-steps-compact-card: 紧凑卡片蛇形步骤 (maxItems=8)

    ## 适用场景
    - 较多步骤需要节省空间
    - 6-10 个步骤
    - 视觉上需要变化
    - 连续的长流程

    ## 不适用场景
    - 少于 5 个步骤（用 sequence-steps）
    - 循环流程（用 sequence-circular）
    - 时间线（用 sequence-timeline）

    ## 与其他 sequence 类型的区别
    - sequence-snake: S 形弯曲，多行展示
    - sequence-zigzag: 锯齿形交替
    - sequence-steps: 单行线性

    ## 数据格式
    {"sequences": [{"label": "步骤名", "desc": "描述(可选)"}]}

    Args:
        template: 模板名称，必须是: sequence-snake-steps-simple | sequence-snake-steps-badge-card | sequence-snake-steps-compact-card
        data_json: JSON 字符串，格式为 {"sequences": [{"label": "阶段1"}, {"label": "阶段2"}, {"label": "阶段3"}, {"label": "阶段4"}]}，label 必填，desc 可选
        rationale: 选择该模板的理由，简述为什么蛇形流程适合当前内容
    """
    return TemplateSelection(
        category="sequence",
        sub_category="sequence-snake",
        template=template,
        data=json.loads(data_json),
        rationale=rationale,
    )


@function_tool
def sequence_circular(
    template: str,
    data_json: str,
    rationale: str,
) -> TemplateSelection:
    """选择 sequence-circular 类型模板 - 循环流程，展示循环往复的过程。

    ## 可用模板
    - sequence-circular-simple: 简洁循环流程 (maxItems=6)
    - sequence-circular-compact-card: 紧凑卡片循环流程 (maxItems=5)

    ## 适用场景
    - 循环往复的过程
    - PDCA 循环、敏捷迭代
    - 生命周期、循环系统
    - 闭环流程

    ## 不适用场景
    - 线性流程（用 sequence-steps）
    - 有起点终点的流程
    - 时间线（用 sequence-timeline）

    ## 与其他 sequence 类型的区别
    - sequence-circular: 环形闭环，无起点终点
    - sequence-steps: 线性，有起点终点
    - sequence-funnel: 漏斗筛选，数量递减

    ## 数据格式
    {"sequences": [{"label": "阶段名", "desc": "描述(可选)"}]}

    Args:
        template: 模板名称，必须是: sequence-circular-simple | sequence-circular-compact-card
        data_json: JSON 字符串，格式为 {"sequences": [{"label": "计划"}, {"label": "执行"}, {"label": "检查"}, {"label": "改进"}]}，label 必填，desc 可选
        rationale: 选择该模板的理由，简述为什么循环流程适合当前内容
    """
    return TemplateSelection(
        category="sequence",
        sub_category="sequence-circular",
        template=template,
        data=json.loads(data_json),
        rationale=rationale,
    )


@function_tool
def sequence_funnel(
    template: str,
    data_json: str,
    rationale: str,
) -> TemplateSelection:
    """选择 sequence-funnel 类型模板 - 漏斗图，展示逐步筛选的过程。

    ## 可用模板
    - sequence-funnel: 标准漏斗图 (maxItems=6)

    ## 适用场景
    - 逐步筛选、转化漏斗
    - 销售漏斗、用户转化
    - 数量逐渐减少的过程
    - 有明确数值的筛选过程

    ## 不适用场景
    - 无筛选关系的步骤（用 sequence-steps）
    - 循环流程（用 sequence-circular）
    - 无数值的流程

    ## 与其他 sequence 类型的区别
    - sequence-funnel: 漏斗形状，强调数量递减
    - sequence-stairs: 阶梯递进，强调级别提升
    - sequence-steps: 普通线性步骤

    ## 数据格式
    {"sequences": [{"label": "阶段名", "value": 数值}]}

    Args:
        template: 模板名称，必须是: sequence-funnel
        data_json: JSON 字符串，格式为 {"sequences": [{"label": "访问", "value": 1000}, {"label": "注册", "value": 300}, {"label": "付费", "value": 50}]}，label 和 value 必填
        rationale: 选择该模板的理由，简述为什么漏斗图适合当前内容
    """
    return TemplateSelection(
        category="sequence",
        sub_category="sequence-funnel",
        template=template,
        data=json.loads(data_json),
        rationale=rationale,
    )


@function_tool
def sequence_roadmap(
    template: str,
    data_json: str,
    rationale: str,
) -> TemplateSelection:
    """选择 sequence-roadmap 类型模板 - 路线图，展示规划和里程碑。

    ## 可用模板
    - sequence-roadmap-vertical-simple: 垂直简洁路线图 (maxItems=8)
    - sequence-roadmap-vertical-badge-card: 垂直徽章卡片路线图 (maxItems=6)
    - sequence-roadmap-vertical-compact-card: 垂直紧凑卡片路线图 (maxItems=6)

    ## 适用场景
    - 产品规划、发展路线
    - 里程碑计划
    - 未来规划、战略目标
    - 学习路径、成长规划

    ## 不适用场景
    - 历史事件（用 sequence-timeline）
    - 操作步骤（用 sequence-steps）
    - 循环流程（用 sequence-circular）

    ## 与其他 sequence 类型的区别
    - sequence-roadmap: 强调规划和未来目标
    - sequence-timeline: 强调过去发生的事件
    - sequence-steps: 具体操作步骤

    ## 数据格式
    {"sequences": [{"label": "里程碑", "time": "Q1 2025", "desc": "描述(可选)"}]}

    Args:
        template: 模板名称，必须是: sequence-roadmap-vertical-simple | sequence-roadmap-vertical-badge-card | sequence-roadmap-vertical-compact-card
        data_json: JSON 字符串，格式为 {"sequences": [{"label": "MVP发布", "time": "Q1 2025"}, {"label": "v2.0", "time": "Q3 2025"}]}，label 必填，time 和 desc 可选
        rationale: 选择该模板的理由，简述为什么路线图适合当前内容
    """
    return TemplateSelection(
        category="sequence",
        sub_category="sequence-roadmap",
        template=template,
        data=json.loads(data_json),
        rationale=rationale,
    )


@function_tool
def sequence_zigzag(
    template: str,
    data_json: str,
    rationale: str,
) -> TemplateSelection:
    """选择 sequence-zigzag 类型模板 - 锯齿流程，交替排列的步骤展示。

    ## 可用模板
    - sequence-zigzag-steps-simple: 简洁锯齿步骤 (maxItems=8)
    - sequence-horizontal-zigzag-simple: 水平锯齿简洁样式 (maxItems=6)
    - sequence-horizontal-zigzag-compact-card: 水平锯齿紧凑卡片 (maxItems=5)

    ## 适用场景
    - 需要视觉变化的流程
    - 交替排列的步骤
    - 5-8 个步骤
    - 需要节省空间的展示

    ## 不适用场景
    - 少于 4 个步骤（用 sequence-steps）
    - 循环流程（用 sequence-circular）
    - 时间线（用 sequence-timeline）

    ## 与其他 sequence 类型的区别
    - sequence-zigzag: 锯齿形交替，左右交错
    - sequence-snake: S 形弯曲
    - sequence-steps: 单行线性

    ## 数据格式
    {"sequences": [{"label": "步骤名", "desc": "描述(可选)"}]}

    Args:
        template: 模板名称，必须是: sequence-zigzag-steps-simple | sequence-horizontal-zigzag-simple | sequence-horizontal-zigzag-compact-card
        data_json: JSON 字符串，格式为 {"sequences": [{"label": "调研"}, {"label": "设计"}, {"label": "开发"}, {"label": "测试"}]}，label 必填，desc 可选
        rationale: 选择该模板的理由，简述为什么锯齿流程适合当前内容
    """
    return TemplateSelection(
        category="sequence",
        sub_category="sequence-zigzag",
        template=template,
        data=json.loads(data_json),
        rationale=rationale,
    )
