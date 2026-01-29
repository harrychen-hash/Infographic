"""
[INPUT]: intent, paragraphs 从 category agent 传入
[OUTPUT]: TemplateSelection - 选择的模板和数据
[POS]: agentic/tools 的 hierarchy 分类工具集

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
def hierarchy_tree(
    template: str,
    data_json: str,
    rationale: str,
) -> TemplateSelection:
    """选择 hierarchy-tree 类型模板 - 树状图，展示层级和分支关系。

    ## 可用模板
    - hierarchy-tree-tech-style-capsule-item: 科技风格胶囊节点 (maxDepth=3, maxChildren=4)
    - hierarchy-tree-dashed-line-rounded-rect-node: 虚线圆角矩形节点 (maxDepth=3, maxChildren=4)
    - hierarchy-tree-curved-line-compact-card: 曲线紧凑卡片 (maxDepth=3, maxChildren=3)
    - hierarchy-tree-dashed-arrow-badge-card: 虚线箭头徽章卡片 (maxDepth=3, maxChildren=3)

    ## 适用场景
    - 层级分类、分支结构
    - 知识体系、目录结构
    - 产品分类、功能模块
    - 每个节点只有一个父节点

    ## 不适用场景
    - 网状关系、多父节点（用 relation-dagre-flow）
    - 发散思维（用 hierarchy-mindmap）
    - 组织架构（用 hierarchy-structure）

    ## 与其他 hierarchy 类型的区别
    - hierarchy-tree: 严格的树状结构，从根到叶
    - hierarchy-mindmap: 中心发散，更自由
    - hierarchy-structure: 组织架构，人员层级

    ## 与 relation 的区别
    - hierarchy: 树状结构，每个节点只有一个父节点
    - relation: 网状关系，节点可以有多个父节点

    ## 数据格式
    {"root": {"label": "根节点", "children": [{"label": "子节点1", "children": [...]}]}}

    Args:
        template: 模板名称，必须是: hierarchy-tree-tech-style-capsule-item | hierarchy-tree-dashed-line-rounded-rect-node | hierarchy-tree-curved-line-compact-card | hierarchy-tree-dashed-arrow-badge-card
        data_json: JSON 字符串，格式为 {"root": {"label": "系统", "children": [{"label": "模块A", "children": [{"label": "功能1"}]}]}}，包含嵌套的 label 和 children
        rationale: 选择该模板的理由，简述为什么树状图适合当前内容
    """
    return TemplateSelection(
        category="hierarchy",
        sub_category="hierarchy-tree",
        template=template,
        data=json.loads(data_json),
        rationale=rationale,
    )


@function_tool
def hierarchy_mindmap(
    template: str,
    data_json: str,
    rationale: str,
) -> TemplateSelection:
    """选择 hierarchy-mindmap 类型模板 - 思维导图，展示发散性思维和关联。

    ## 可用模板
    - hierarchy-mindmap-branch-gradient-capsule-item: 分支渐变胶囊 (maxBranches=6, maxDepth=3)
    - hierarchy-mindmap-level-gradient-rounded-rect-node: 层级渐变圆角矩形 (maxBranches=5, maxDepth=3)
    - hierarchy-mindmap-branch-gradient-compact-card: 分支渐变紧凑卡片 (maxBranches=4, maxDepth=3)

    ## 适用场景
    - 发散性思维、头脑风暴
    - 知识关联、概念图
    - 中心主题的多方向延伸
    - 创意整理、笔记总结

    ## 不适用场景
    - 严格的层级分类（用 hierarchy-tree）
    - 组织架构（用 hierarchy-structure）
    - 流程依赖（用 relation-dagre-flow）

    ## 与其他 hierarchy 类型的区别
    - hierarchy-mindmap: 中心发散，强调关联和创意
    - hierarchy-tree: 严格树状，从上到下
    - hierarchy-structure: 组织架构，人员层级

    ## 数据格式
    {"root": {"label": "中心主题", "children": [{"label": "分支1", "children": [...]}]}}

    Args:
        template: 模板名称，必须是: hierarchy-mindmap-branch-gradient-capsule-item | hierarchy-mindmap-level-gradient-rounded-rect-node | hierarchy-mindmap-branch-gradient-compact-card
        data_json: JSON 字符串，格式为 {"root": {"label": "主题", "children": [{"label": "分支1", "children": [{"label": "细节"}]}]}}，从中心向外发散
        rationale: 选择该模板的理由，简述为什么思维导图适合当前内容
    """
    return TemplateSelection(
        category="hierarchy",
        sub_category="hierarchy-mindmap",
        template=template,
        data=json.loads(data_json),
        rationale=rationale,
    )


@function_tool
def hierarchy_structure(
    template: str,
    data_json: str,
    rationale: str,
) -> TemplateSelection:
    """选择 hierarchy-structure 类型模板 - 组织架构图，展示组织层级。

    ## 可用模板
    - hierarchy-structure: 标准组织架构图 (maxDepth=4, maxChildren=5)
    - hierarchy-structure-mirror: 镜像组织架构图 (maxDepth=4, maxChildren=4)

    ## 适用场景
    - 公司组织架构
    - 团队层级结构
    - 管理层级
    - 人员从属关系

    ## 不适用场景
    - 产品分类（用 hierarchy-tree）
    - 发散思维（用 hierarchy-mindmap）
    - 流程依赖（用 relation-dagre-flow）

    ## 与其他 hierarchy 类型的区别
    - hierarchy-structure: 专为组织架构设计，强调职位层级
    - hierarchy-tree: 通用树状结构
    - hierarchy-mindmap: 发散思维，不强调层级

    ## 数据格式
    {"root": {"label": "CEO", "title": "首席执行官", "children": [{"label": "CTO", "title": "技术总监", "children": [...]}]}}

    Args:
        template: 模板名称，必须是: hierarchy-structure | hierarchy-structure-mirror
        data_json: JSON 字符串，格式为 {"root": {"label": "CEO", "title": "首席执行官", "children": [{"label": "CTO", "title": "技术总监"}]}}，label 必填，title 可选
        rationale: 选择该模板的理由，简述为什么组织架构图适合当前内容
    """
    return TemplateSelection(
        category="hierarchy",
        sub_category="hierarchy-structure",
        template=template,
        data=json.loads(data_json),
        rationale=rationale,
    )
