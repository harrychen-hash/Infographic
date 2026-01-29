"""
[INPUT]: (无外部依赖)
[OUTPUT]: Intent, ArticleSegmentation - 文章意图切分的数据模型
[POS]: agentic/models 的核心模型，定义 segmentation agent 的输出结构

[PROTOCOL]:
1. 一旦本文件逻辑变更，必须同步更新此 Header。
2. 更新后必须上浮检查 models/.folder.md 的描述是否仍然准确。
"""

from pydantic import BaseModel, Field


class Intent(BaseModel):
    """单个意图块，包含意图描述和相关段落"""

    intent: str = Field(description="该意图的核心描述")
    paragraphs: list[str] = Field(description="属于该意图的段落内容列表")


class ArticleSegmentation(BaseModel):
    """文章意图切分结果，包含多个意图块"""

    intents: list[Intent] = Field(description="文章中识别出的所有意图块")
