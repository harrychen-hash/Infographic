"""
[INPUT]: DSL 语法字符串
[OUTPUT]: SVG 字符串 或 错误信息
[POS]: 调用 Node.js @antv/infographic SSR 渲染器

[PROTOCOL]:
1. 一旦本文件逻辑变更，必须同步更新此 Header。
2. 更新后必须上浮检查 renderers/.folder.md 的描述是否仍然准确。

使用方式:
    from renderers import render_to_svg

    result = render_to_svg(dsl_syntax)
    if result["success"]:
        svg_content = result["svg"]
    else:
        error_msg = result["error"]
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path
from typing import TypedDict


class RenderResult(TypedDict):
    """渲染结果类型"""
    success: bool
    svg: str | None
    error: str | None


# 获取 site 目录 (Node.js 项目根目录)
SITE_ROOT = Path(__file__).parent.parent.parent.parent.parent


def render_to_svg(dsl_syntax: str, width: int = 800, height: int = 600) -> RenderResult:
    """通过 Node.js subprocess 渲染 DSL 到 SVG

    Args:
        dsl_syntax: @antv/infographic DSL 语法字符串
        width: SVG 宽度，默认 800
        height: SVG 高度，默认 600

    Returns:
        RenderResult: {"success": bool, "svg": str | None, "error": str | None}
    """
    # 将 DSL 写入临时文件以避免命令行转义问题
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".dsl",
        delete=False,
        encoding="utf-8",
    ) as f:
        f.write(dsl_syntax)
        dsl_file = f.name

    # Node.js 渲染脚本
    node_script = f'''
const fs = require('fs');
const {{ renderToString }} = require('@antv/infographic/ssr');

const dsl = fs.readFileSync('{dsl_file}', 'utf-8');

renderToString(dsl, {{ width: {width}, height: {height} }})
  .then(svg => {{
    console.log(JSON.stringify({{ success: true, svg: svg }}));
  }})
  .catch(err => {{
    console.log(JSON.stringify({{ success: false, error: err.message }}));
  }});
'''

    try:
        result = subprocess.run(
            ["node", "-e", node_script],
            capture_output=True,
            text=True,
            cwd=str(SITE_ROOT),
            timeout=30,
        )

        # 清理临时文件
        Path(dsl_file).unlink(missing_ok=True)

        if result.returncode != 0:
            # Node.js 执行错误
            return {
                "success": False,
                "svg": None,
                "error": f"Node.js error: {result.stderr or result.stdout}",
            }

        # 解析 JSON 输出
        try:
            output = json.loads(result.stdout)
            return output
        except json.JSONDecodeError:
            return {
                "success": False,
                "svg": None,
                "error": f"Invalid JSON output: {result.stdout[:500]}",
            }

    except subprocess.TimeoutExpired:
        Path(dsl_file).unlink(missing_ok=True)
        return {
            "success": False,
            "svg": None,
            "error": "Rendering timeout (30s)",
        }
    except FileNotFoundError:
        Path(dsl_file).unlink(missing_ok=True)
        return {
            "success": False,
            "svg": None,
            "error": "Node.js not found. Please install Node.js.",
        }
    except Exception as e:
        Path(dsl_file).unlink(missing_ok=True)
        return {
            "success": False,
            "svg": None,
            "error": str(e),
        }


def save_svg(svg_content: str, output_path: str | Path) -> Path:
    """保存 SVG 内容到文件

    Args:
        svg_content: SVG 字符串
        output_path: 输出文件路径

    Returns:
        Path: 保存的文件路径
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg_content, encoding="utf-8")
    return path
