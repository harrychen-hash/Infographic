"""
[INPUT]: segmentation, template_selection 模块
[OUTPUT]: Intent, ArticleSegmentation, TemplateSelection, TemplateInput
[POS]: models 包的入口，导出所有数据模型

[PROTOCOL]:
1. 一旦本文件逻辑变更，必须同步更新此 Header。
2. 更新后必须上浮检查 models/.folder.md 的描述是否仍然准确。
"""

from .segmentation import Intent, ArticleSegmentation
from .template_selection import TemplateSelection, TemplateInput

__all__ = [
    "Intent",
    "ArticleSegmentation",
    "TemplateSelection",
    "TemplateInput",
]
