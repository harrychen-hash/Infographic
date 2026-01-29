"""
[INPUT]: category 名称
[OUTPUT]: 对应 category 的 skip tool，返回 TemplateSelection
[POS]: agentic/tools 的通用工具模块，提供跨 category 共享的功能

[PROTOCOL]:
1. 一旦本文件逻辑变更，必须同步更新此 Header。
2. 更新后必须上浮检查 tools/.folder.md 的描述是否仍然准确。
"""

from __future__ import annotations

from typing import Callable

from agents import function_tool

from ..models import TemplateSelection


def create_skip_tool(category: str) -> Callable:
    """为指定 category 创建专属的 skip tool。

    每个 category agent 都应该有一个 skip tool，用于以下场景：
    - 文字/数据不足以画图
    - 内容在原文中不是同一维度
    - 数据质量不满足最低要求（如 chart 需要 >=2 个数值数据点）

    Args:
        category: category 名称，如 "chart", "list", "sequence" 等

    Returns:
        一个 function_tool 装饰的函数，返回 TemplateSelection
    """

    @function_tool(
        name_override=f"skip_{category}",
        description_override=f"当 {category} 类型内的内容不适合生成图表时跳过。适用于：数据不足、维度不一致、质量不达标等情况。",
    )
    def skip_in_category(reason: str) -> TemplateSelection:
        """跳过当前内容，不生成可视化。

        Args:
            reason: 跳过的具体原因，说明为什么当前内容不适合生成 {category} 类型图表
        """
        return TemplateSelection(
            category=category,
            sub_category=None,
            template=None,
            data=None,
            rationale=reason,
        )

    return skip_in_category


# 预创建各 category 的 skip tools
skip_chart = create_skip_tool("chart")
skip_list = create_skip_tool("list")
skip_sequence = create_skip_tool("sequence")
skip_comparison = create_skip_tool("comparison")
skip_hierarchy = create_skip_tool("hierarchy")
skip_relation = create_skip_tool("relation")
skip_quadrant = create_skip_tool("quadrant")
