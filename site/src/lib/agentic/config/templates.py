"""
[INPUT]: (无外部依赖)
[OUTPUT]: TEMPLATE_CATEGORIES - 模板分类元数据配置
[POS]: agentic/config 的核心配置，定义所有模板分类、子分类及其描述

[PROTOCOL]:
1. 一旦本文件逻辑变更，必须同步更新此 Header。
2. 更新后必须上浮检查 config/.folder.md 的描述是否仍然准确。
"""

from __future__ import annotations

from typing import Dict, List, Any

# 模板分类元数据配置
# 结构: Category -> Sub-category -> Templates
TEMPLATE_CATEGORIES: Dict[str, Dict[str, Any]] = {
    "chart": {
        "description": "数据图表，用于展示数值对比、占比、趋势等量化信息",
        "sub_categories": {
            "chart-pie": {
                "description": "饼图/环形图，展示占比和组成部分",
                "templates": [
                    "chart-pie-plain-text",
                    "chart-pie-compact-card",
                    "chart-pie-pill-badge",
                    "chart-pie-donut-plain-text",
                    "chart-pie-donut-compact-card",
                    "chart-pie-donut-pill-badge",
                ],
            },
            "chart-bar": {
                "description": "条形图，展示数值大小对比",
                "templates": ["chart-bar-plain-text"],
            },
            "chart-line": {
                "description": "折线图，展示趋势变化",
                "templates": ["chart-line-plain-text"],
            },
            "chart-column": {
                "description": "柱状图，展示分类数据对比",
                "templates": ["chart-column-simple"],
            },
            "chart-wordcloud": {
                "description": "词云图，展示关键词频率和重要性",
                "templates": ["chart-wordcloud", "chart-wordcloud-rotate"],
            },
        },
    },
    "comparison": {
        "description": "对比分析，用于展示两个或多个事物之间的差异和共同点",
        "sub_categories": {
            "compare-binary": {
                "description": "二元对比，左右或上下两方对比",
                "templates": [
                    "compare-binary-horizontal-arrow-simple",
                    "compare-binary-horizontal-arrow-underline-text",
                    "compare-binary-horizontal-arrow-badge-card",
                    "compare-binary-horizontal-arrow-compact-card",
                    "compare-binary-horizontal-fold-simple",
                    "compare-binary-horizontal-fold-underline-text",
                    "compare-binary-horizontal-fold-badge-card",
                    "compare-binary-horizontal-fold-compact-card",
                    "compare-binary-horizontal-vs-simple",
                    "compare-binary-horizontal-vs-underline-text",
                    "compare-binary-horizontal-vs-badge-card",
                    "compare-binary-horizontal-vs-compact-card",
                ],
            },
            "compare-hierarchy": {
                "description": "层级对比，对比不同层级或分类",
                "templates": [
                    "compare-hierarchy-left-right-simple",
                    "compare-hierarchy-left-right-compact-card",
                    "compare-hierarchy-row-simple",
                    "compare-hierarchy-row-compact-card",
                ],
            },
            "compare-swot": {
                "description": "SWOT 分析，展示优势、劣势、机会、威胁",
                "templates": ["compare-swot"],
            },
            "compare-quadrant": {
                "description": "对比象限，按两个维度分类对比",
                "templates": [
                    "compare-quadrant-quarter-simple-card",
                    "compare-quadrant-quarter-circular",
                    "compare-quadrant-simple-illus",
                ],
            },
        },
    },
    "hierarchy": {
        "description": "层级结构，用于展示组织架构、分类体系、树状关系",
        "sub_categories": {
            "hierarchy-tree": {
                "description": "树状图，展示层级和分支关系",
                "templates": [
                    "hierarchy-tree-tech-style-capsule-item",
                    "hierarchy-tree-dashed-line-rounded-rect-node",
                    "hierarchy-tree-curved-line-compact-card",
                    "hierarchy-tree-dashed-arrow-badge-card",
                ],
            },
            "hierarchy-mindmap": {
                "description": "思维导图，展示发散性思维和关联",
                "templates": [
                    "hierarchy-mindmap-branch-gradient-capsule-item",
                    "hierarchy-mindmap-level-gradient-rounded-rect-node",
                    "hierarchy-mindmap-branch-gradient-compact-card",
                ],
            },
            "hierarchy-structure": {
                "description": "组织架构图，展示组织层级",
                "templates": ["hierarchy-structure", "hierarchy-structure-mirror"],
            },
        },
    },
    "list": {
        "description": "列表展示，用于展示多个并列项目、步骤、特征",
        "sub_categories": {
            "list-column": {
                "description": "竖向列表，垂直排列的项目",
                "templates": [
                    "list-column-done-list",
                    "list-column-vertical-icon-arrow",
                    "list-column-simple-vertical-arrow",
                ],
            },
            "list-grid": {
                "description": "网格列表，矩阵排列的项目",
                "templates": [
                    "list-grid-badge-card",
                    "list-grid-candy-card-lite",
                    "list-grid-circular-progress",
                    "list-grid-compact-card",
                    "list-grid-done-list",
                    "list-grid-horizontal-icon-arrow",
                    "list-grid-progress-card",
                    "list-grid-ribbon-card",
                    "list-grid-simple",
                ],
            },
            "list-pyramid": {
                "description": "金字塔列表，层级递减的结构",
                "templates": [
                    "list-pyramid-rounded-rect-node",
                    "list-pyramid-badge-card",
                    "list-pyramid-compact-card",
                ],
            },
            "list-row": {
                "description": "横向列表，水平排列的项目",
                "templates": [
                    "list-row-circular-progress",
                    "list-row-horizontal-icon-arrow",
                    "list-row-simple-horizontal-arrow",
                    "list-row-horizontal-icon-line",
                ],
            },
            "list-sector": {
                "description": "扇形列表，放射状排列",
                "templates": [
                    "list-sector-simple",
                    "list-sector-plain-text",
                    "list-sector-half-plain-text",
                ],
            },
            "list-zigzag": {
                "description": "锯齿列表，交替排列的项目",
                "templates": [
                    "list-zigzag-up-compact-card",
                    "list-zigzag-down-compact-card",
                    "list-zigzag-up-simple",
                    "list-zigzag-down-simple",
                ],
            },
        },
    },
    "quadrant": {
        "description": "象限图，用于按两个维度对事物进行分类定位",
        "sub_categories": {
            "quadrant-quarter": {
                "description": "四象限图，按两个维度分成四个区域",
                "templates": [
                    "quadrant-quarter-simple-card",
                    "quadrant-quarter-circular",
                ],
            },
            "quadrant-simple": {
                "description": "简单象限图，基础的象限展示",
                "templates": ["quadrant-simple-illus"],
            },
        },
    },
    "relation": {
        "description": "关系图，用于展示实体之间的关联、流程、网络",
        "sub_categories": {
            "relation-dagre-flow": {
                "description": "流程关系图，展示有向流程和依赖",
                "templates": [
                    "relation-dagre-flow-tb-simple-circle-node",
                    "relation-dagre-flow-lr-simple-circle-node",
                    "relation-dagre-flow-tb-badge-card",
                    "relation-dagre-flow-lr-badge-card",
                    "relation-dagre-flow-tb-compact-card",
                    "relation-dagre-flow-lr-compact-card",
                ],
            },
            "relation-circle": {
                "description": "环形关系图，展示循环或围绕关系",
                "templates": [
                    "relation-circle-circular-progress",
                    "relation-circle-icon-badge",
                ],
            },
        },
    },
    "sequence": {
        "description": "时序/流程，用于展示步骤、阶段、时间线",
        "sub_categories": {
            "sequence-stairs": {
                "description": "阶梯式流程，逐步递进",
                "templates": [
                    "sequence-stairs-front-compact-card",
                    "sequence-stairs-front-badge-card",
                    "sequence-stairs-front-simple",
                ],
            },
            "sequence-timeline": {
                "description": "时间线，按时间顺序展示事件",
                "templates": [
                    "sequence-timeline-simple",
                    "sequence-timeline-badge-card",
                    "sequence-timeline-compact-card",
                    "sequence-timeline-circular-progress",
                    "sequence-timeline-horizontal-icon-arrow",
                ],
            },
            "sequence-steps": {
                "description": "步骤流程，展示操作步骤",
                "templates": ["sequence-steps-simple", "sequence-steps-compact-card"],
            },
            "sequence-snake": {
                "description": "蛇形流程，弯曲的步骤展示",
                "templates": [
                    "sequence-snake-steps-simple",
                    "sequence-snake-steps-badge-card",
                    "sequence-snake-steps-compact-card",
                ],
            },
            "sequence-circular": {
                "description": "循环流程，展示循环往复的过程",
                "templates": [
                    "sequence-circular-simple",
                    "sequence-circular-compact-card",
                ],
            },
            "sequence-funnel": {
                "description": "漏斗图，展示逐步筛选的过程",
                "templates": ["sequence-funnel"],
            },
            "sequence-roadmap": {
                "description": "路线图，展示规划和里程碑",
                "templates": [
                    "sequence-roadmap-vertical-simple",
                    "sequence-roadmap-vertical-badge-card",
                    "sequence-roadmap-vertical-compact-card",
                ],
            },
            "sequence-zigzag": {
                "description": "锯齿流程，交替排列的步骤",
                "templates": [
                    "sequence-zigzag-steps-simple",
                    "sequence-horizontal-zigzag-simple",
                    "sequence-horizontal-zigzag-compact-card",
                ],
            },
        },
    },
}


def get_sub_categories(category: str) -> List[str]:
    """获取指定分类下的所有子分类名称"""
    if category not in TEMPLATE_CATEGORIES:
        return []
    return list(TEMPLATE_CATEGORIES[category]["sub_categories"].keys())


def get_templates(category: str, sub_category: str) -> List[str]:
    """获取指定子分类下的所有模板名称"""
    if category not in TEMPLATE_CATEGORIES:
        return []
    sub_cats = TEMPLATE_CATEGORIES[category].get("sub_categories", {})
    if sub_category not in sub_cats:
        return []
    return sub_cats[sub_category].get("templates", [])


def get_sub_category_description(category: str, sub_category: str) -> str:
    """获取子分类的描述"""
    if category not in TEMPLATE_CATEGORIES:
        return ""
    sub_cats = TEMPLATE_CATEGORIES[category].get("sub_categories", {})
    if sub_category not in sub_cats:
        return ""
    return sub_cats[sub_category].get("description", "")
