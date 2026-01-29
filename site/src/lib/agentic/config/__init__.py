"""
[INPUT]: templates 模块
[OUTPUT]: TEMPLATE_CATEGORIES, get_sub_categories, get_templates
[POS]: config 包的入口，导出模板配置

[PROTOCOL]:
1. 一旦本文件逻辑变更，必须同步更新此 Header。
2. 更新后必须上浮检查 config/.folder.md 的描述是否仍然准确。
"""

from .templates import TEMPLATE_CATEGORIES, get_sub_categories, get_templates

__all__ = ["TEMPLATE_CATEGORIES", "get_sub_categories", "get_templates"]
