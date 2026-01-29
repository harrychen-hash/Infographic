"""
[INPUT]: agents, models, config 子模块
[OUTPUT]: 所有 agent、数据模型、配置和流水线函数
[POS]: agentic 包的主入口，提供统一的导出接口

[PROTOCOL]:
1. 一旦本文件逻辑变更，必须同步更新此 Header。
2. 更新后必须上浮检查 .folder.md 的描述是否仍然准确。

Agentic Article Processing Pipeline
使用 OpenAI Agents SDK 构建的文章处理流水线
"""

# Agents
from .agents import (
    segmentation_agent,
    segment_article,
    segment_article_sync,
    template_selector,
    chart_agent,
    comparison_agent,
    hierarchy_agent,
    list_agent,
    quadrant_agent,
    relation_agent,
    sequence_agent,
)
from .agents.pipeline import (
    process_article,
    process_article_sync,
    process_intents,
    select_template_for_intent,
)

# Models
from .models import Intent, ArticleSegmentation, TemplateSelection, TemplateInput

# Config
from .config import TEMPLATE_CATEGORIES, get_sub_categories, get_templates

__all__ = [
    # Segmentation
    "segmentation_agent",
    "segment_article",
    "segment_article_sync",
    # Template Selection
    "template_selector",
    "chart_agent",
    "comparison_agent",
    "hierarchy_agent",
    "list_agent",
    "quadrant_agent",
    "relation_agent",
    "sequence_agent",
    # Pipeline
    "process_article",
    "process_article_sync",
    "process_intents",
    "select_template_for_intent",
    # Models
    "Intent",
    "ArticleSegmentation",
    "TemplateSelection",
    "TemplateInput",
    # Config
    "TEMPLATE_CATEGORIES",
    "get_sub_categories",
    "get_templates",
]
