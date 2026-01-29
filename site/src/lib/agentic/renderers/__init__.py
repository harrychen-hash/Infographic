"""
[INPUT]: dsl_generator, node_bridge 模块
[OUTPUT]: generate_dsl, render_to_svg 函数
[POS]: renderers 包的入口，导出渲染相关函数

[PROTOCOL]:
1. 一旦本文件逻辑变更，必须同步更新此 Header。
2. 更新后必须上浮检查 renderers/.folder.md 的描述是否仍然准确。
"""

from .dsl_generator import generate_dsl
from .node_bridge import render_to_svg, save_svg

__all__ = [
    "generate_dsl",
    "render_to_svg",
    "save_svg",
]
