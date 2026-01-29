"""
[INPUT]: segmentation_agent, template_selector, category_agents 模块
[OUTPUT]: 所有 agent 和相关函数
[POS]: agents 包的入口，导出所有 agent 和相关函数

[PROTOCOL]:
1. 一旦本文件逻辑变更，必须同步更新此 Header。
2. 更新后必须上浮检查 agents/.folder.md 的描述是否仍然准确。
"""

from .segmentation_agent import (
    segmentation_agent,
    segment_article,
    segment_article_sync,
)
from .template_selector import template_selector
from .category_agents import (
    chart_agent,
    comparison_agent,
    hierarchy_agent,
    list_agent,
    quadrant_agent,
    relation_agent,
    sequence_agent,
)

__all__ = [
    # Segmentation
    "segmentation_agent",
    "segment_article",
    "segment_article_sync",
    # Template Selection
    "template_selector",
    # Category Agents
    "chart_agent",
    "comparison_agent",
    "hierarchy_agent",
    "list_agent",
    "quadrant_agent",
    "relation_agent",
    "sequence_agent",
]
