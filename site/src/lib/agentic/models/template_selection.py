"""
[INPUT]: (无外部依赖)
[OUTPUT]: TemplateSelection - 模板选择结果模型
[POS]: agentic/models 的输出模型，定义 template selection 的结果结构

[PROTOCOL]:
1. 一旦本文件逻辑变更，必须同步更新此 Header。
2. 更新后必须上浮检查 models/.folder.md 的描述是否仍然准确。
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class TemplateSelection(BaseModel):
    """模板选择结果，包含选定的模板和填充数据

    当 category='skip' 时，sub_category/template/data 可以为 None
    """

    category: str = Field(description="图表大类，如 chart, list, sequence, skip 等")
    sub_category: Optional[str] = Field(
        description="子分类，如 chart-pie, list-column 等。skip 时为 None",
        default=None,
    )
    template: Optional[str] = Field(
        description="具体模板名称，如 chart-pie-plain-text。skip 时为 None",
        default=None,
    )
    data: Optional[Dict[str, Any]] = Field(
        description="填充模板的结构化数据。skip 时为 None",
        default=None,
    )
    rationale: Optional[str] = Field(
        description="选择该模板的理由或跳过的原因",
        default=None,
    )


class TemplateInput(BaseModel):
    """传递给 template selection 流程的输入"""

    intent: str = Field(description="意图描述")
    paragraphs: List[str] = Field(description="相关段落内容")
