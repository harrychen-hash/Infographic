"""
[INPUT]: intent, paragraphs 从 template_selector 传入
[OUTPUT]: skip result - 跳过可视化的原因
[POS]: agents/category_agents 的 skip 分类 agent，处理不适合可视化的内容

[PROTOCOL]:
1. 一旦本文件逻辑变更，必须同步更新此 Header。
2. 更新后必须上浮检查 category_agents/.folder.md 的描述是否仍然准确。
"""

from __future__ import annotations

from agents import Agent, function_tool

from ...utils import get_default_model


@function_tool
def skip_visualization(reason: str) -> str:
    """跳过当前意图块，不生成可视化。

    当内容不适合任何可视化方案时调用此工具。

    Args:
        reason: 跳过的原因，如"纯叙述性内容"、"缺乏结构化数据"、"引言过渡段落"等
    """
    return f"category='skip' sub_category=None template=None data=None rationale='{reason}'"


SKIP_AGENT_INSTRUCTIONS = """你是内容可视化评估专家。你的任务是确认当前内容确实不适合任何可视化方案。

## 适合跳过的情况

1. **纯叙述性内容** - 没有结构化数据，纯粹是故事性描述
2. **引言/结语** - 开场白、总结语、过渡段落
3. **抒情性内容** - 情感表达、观点阐述，无具体数据或结构
4. **已经是图表描述** - 文字本身在描述一张已有的图表
5. **缺乏足够信息** - 内容太少或太模糊，无法提取有意义的数据

## 不应跳过的情况

即使内容看起来简单，以下情况仍应可视化：
- 有明确的列表项（即使只有2-3项）
- 有对比关系（A vs B）
- 有流程或步骤
- 有层级或分类关系
- 有任何可量化的数据

## 输出

确认内容不适合可视化后，调用 skip_visualization 工具，并提供清晰的跳过原因。
"""

skip_agent = Agent(
    name="Skip Agent",
    handoff_description="当内容不适合任何可视化方案时使用，如纯叙述性文字、引言、过渡段落等",
    instructions=SKIP_AGENT_INSTRUCTIONS,
    tools=[skip_visualization],
    tool_use_behavior="stop_on_first_tool",
    model=get_default_model(),
)
