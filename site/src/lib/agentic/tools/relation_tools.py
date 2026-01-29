"""
[INPUT]: intent, paragraphs 从 category agent 传入
[OUTPUT]: TemplateSelection - 选择的模板和数据
[POS]: agentic/tools 的 relation 分类工具集

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
def relation_dagre_flow(
    template: str,
    data_json: str,
    rationale: str,
) -> TemplateSelection:
    """选择 relation-dagre-flow 类型模板 - 有向流程图，展示节点和连线关系。

    ## 可用模板
    - relation-dagre-flow-tb-simple-circle-node: 上下流向简洁圆形节点 (maxNodes=10)
    - relation-dagre-flow-lr-simple-circle-node: 左右流向简洁圆形节点 (maxNodes=10)
    - relation-dagre-flow-tb-badge-card: 上下流向徽章卡片 (maxNodes=8)
    - relation-dagre-flow-lr-badge-card: 左右流向徽章卡片 (maxNodes=8)
    - relation-dagre-flow-tb-compact-card: 上下流向紧凑卡片 (maxNodes=8)
    - relation-dagre-flow-lr-compact-card: 左右流向紧凑卡片 (maxNodes=8)

    ## 适用场景
    - 流程依赖关系、系统架构
    - 有向图、数据流
    - 模块依赖、调用关系
    - 工作流程、决策树

    ## 不适用场景
    - 循环关系（用 relation-circle）
    - 层级结构（用 hierarchy-tree）
    - 简单线性流程（用 sequence-steps）
    - 无连接关系的列表

    ## 与其他 relation 类型的区别
    - relation-dagre-flow: 有向图，支持复杂连线，使用 dagre 布局算法
    - relation-circle: 环形布局，围绕中心

    ## 与 hierarchy 的区别
    - relation: 网状关系，节点可以有多个父节点
    - hierarchy: 树状结构，每个节点只有一个父节点

    ## 数据格式
    {"nodes": [{"id": "1", "label": "节点1"}], "relations": [{"from": "1", "to": "2", "label": "关系(可选)"}]}

    Args:
        template: 模板名称，必须是: relation-dagre-flow-tb-simple-circle-node | relation-dagre-flow-lr-simple-circle-node | relation-dagre-flow-tb-badge-card | relation-dagre-flow-lr-badge-card | relation-dagre-flow-tb-compact-card | relation-dagre-flow-lr-compact-card
        data_json: JSON 字符串，格式为 {"nodes": [{"id": "a", "label": "服务A"}, {"id": "b", "label": "服务B"}], "relations": [{"from": "a", "to": "b", "label": "调用"}]}，nodes 需要 id 和 label，relations 需要 from 和 to，label 可选
        rationale: 选择该模板的理由，简述为什么有向流程图适合当前内容
    """
    return TemplateSelection(
        category="relation",
        sub_category="relation-dagre-flow",
        template=template,
        data=json.loads(data_json),
        rationale=rationale,
    )


@function_tool
def relation_circle(
    template: str,
    data_json: str,
    rationale: str,
) -> TemplateSelection:
    """选择 relation-circle 类型模板 - 环形关系图，展示围绕中心的关系。

    ## 可用模板
    - relation-circle-circular-progress: 环形进度关系图 (maxNodes=8)
    - relation-circle-icon-badge: 图标徽章环形图 (maxNodes=6)

    ## 适用场景
    - 围绕核心的关系
    - 循环系统、生态圈
    - 核心与周边关系
    - 等距离关系展示

    ## 不适用场景
    - 有向流程（用 relation-dagre-flow）
    - 层级结构（用 hierarchy）
    - 线性流程（用 sequence）

    ## 与其他 relation 类型的区别
    - relation-circle: 环形布局，强调围绕关系
    - relation-dagre-flow: 有向图，强调流向和依赖

    ## 数据格式
    {"nodes": [{"id": "center", "label": "核心"}, {"id": "1", "label": "节点1"}], "relations": [{"from": "center", "to": "1"}]}

    Args:
        template: 模板名称，必须是: relation-circle-circular-progress | relation-circle-icon-badge
        data_json: JSON 字符串，格式为 {"nodes": [{"id": "core", "label": "核心"}, {"id": "1", "label": "节点1"}], "relations": [{"from": "core", "to": "1"}]}，中心节点与周边节点的关系
        rationale: 选择该模板的理由，简述为什么环形关系图适合当前内容
    """
    return TemplateSelection(
        category="relation",
        sub_category="relation-circle",
        template=template,
        data=json.loads(data_json),
        rationale=rationale,
    )
