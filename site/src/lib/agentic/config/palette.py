"""
[INPUT]: 无
[OUTPUT]: AI_COLOR_PALETTE, OUTPUT_DIR 等配置常量
[POS]: agentic/config 的颜色和输出配置

[PROTOCOL]:
1. 一旦本文件逻辑变更，必须同步更新此 Header。
2. 更新后必须上浮检查 config/.folder.md 的描述是否仍然准确。
"""

from __future__ import annotations

from pathlib import Path

# AI Color (Light Mode) - 用于 infographic 生成
AI_COLOR_PALETTE = {
    "name": "ai_color_light",
    "primary": {
        "amplify_green": "#21EF6A",   # HSB: 141 86 94 - 用于正面/成功/增长
        "clarity_blue": "#00D0FF",    # HSB: 191 100 100 - 用于信息/科技/清晰
        "victory_purple": "#8F53ED",  # HSB: 263 65 93 - 用于创新/高端/突出
    },
    "gradient": {
        "0%": "#C9FFCA",   # HSB: 121 21 100 - 最浅绿
        "20%": "#BFF3FA",  # HSB: 187 24 98 - 浅青
        "40%": "#D0EAF6",  # HSB: 199 15 96 - 浅蓝
        "60%": "#EFF5FF",  # HSB: 218 6 100 - 极浅蓝
        "100%": "#F2EFEB", # HSB: 34 3 95 - 米白
    },
    # 用于图表的颜色序列
    "sequence": [
        "#21EF6A",  # amplify_green
        "#00D0FF",  # clarity_blue
        "#8F53ED",  # victory_purple
        "#C9FFCA",  # gradient 0%
        "#BFF3FA",  # gradient 20%
        "#D0EAF6",  # gradient 40%
    ],
}

# 输出目录配置
OUTPUT_DIR = Path("site/output/")

# 确保输出目录存在
def ensure_output_dir() -> Path:
    """确保输出目录存在，返回绝对路径。"""
    output_path = Path(__file__).parent.parent.parent.parent.parent / "output"
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path
