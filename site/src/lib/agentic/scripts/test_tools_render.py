#!/usr/bin/env python3
"""
[INPUT]: 无 (使用预定义的测试数据)
[OUTPUT]: 每个 tool 类型的 SVG 渲染结果
[POS]: agentic/scripts 的工具渲染单元测试脚本

[PROTOCOL]:
1. 一旦本文件逻辑变更，必须同步更新此 Header。
2. 更新后必须上浮检查 scripts/.folder.md 的描述是否仍然准确。

使用方法:
    cd site/src/lib/agentic
    .venv/bin/python -m scripts.test_tools_render

测试目标:
    1. 为每个 tool 类型提供符合格式的测试数据
    2. 生成 DSL → 渲染 SVG → 保存到 site/output/test-{tool-name}.svg
    3. 验证所有 SVG 文件生成成功
"""

from __future__ import annotations

import sys
from pathlib import Path
from datetime import datetime

# 获取路径
SCRIPT_DIR = Path(__file__).parent
AGENTIC_ROOT = SCRIPT_DIR.parent
LIB_ROOT = AGENTIC_ROOT.parent  # site/src/lib
SITE_ROOT = AGENTIC_ROOT.parent.parent.parent  # site/
OUTPUT_DIR = SITE_ROOT / "output"

# ========== 解决 agents 包名冲突 ==========
paths_to_remove = [str(AGENTIC_ROOT), str(AGENTIC_ROOT.resolve()), ""]
original_paths = sys.path.copy()
for p in paths_to_remove:
    while p in sys.path:
        sys.path.remove(p)

import agents as openai_agents_sdk
sys.path = original_paths
sys.path.insert(0, str(LIB_ROOT))
sys.modules["agents"] = openai_agents_sdk

# 导入本地模块
from agentic.renderers.dsl_generator import generate_dsl
from agentic.renderers.node_bridge import render_to_svg, save_svg


# ========== 测试数据定义 ==========

TEST_CASES = {
    # ---- Chart 类型 ----
    "chart-pie": {
        "template": "chart-pie-plain-text",
        "category": "chart",
        "data": {
            "values": [
                {"label": "苹果", "value": 35},
                {"label": "香蕉", "value": 25},
                {"label": "橙子", "value": 20},
                {"label": "葡萄", "value": 20},
            ]
        },
    },
    "chart-bar": {
        "template": "chart-bar-plain-text",
        "category": "chart",
        "data": {
            "values": [
                {"label": "产品A", "value": 85},
                {"label": "产品B", "value": 72},
                {"label": "产品C", "value": 60},
            ]
        },
    },

    # ---- List 类型 ----
    "list-column": {
        "template": "list-column-simple-vertical-arrow",
        "category": "list",
        "data": {
            "lists": [
                {"label": "第一项功能"},
                {"label": "第二项功能"},
                {"label": "第三项功能"},
                {"label": "第四项功能"},
            ]
        },
    },

    # ---- Sequence 类型 ----
    "sequence-steps": {
        "template": "sequence-steps-simple",
        "category": "sequence",
        "data": {
            "sequences": [
                {"label": "分析需求"},
                {"label": "设计方案"},
                {"label": "开发实现"},
                {"label": "测试发布"},
            ]
        },
    },

    # ---- Hierarchy 类型 ----
    "hierarchy-tree": {
        "template": "hierarchy-tree-tech-style-capsule-item",
        "category": "hierarchy",
        "data": {
            "root": {
                "label": "技术栈",
                "children": [
                    {"label": "前端", "children": [{"label": "React"}, {"label": "Vue"}]},
                    {"label": "后端", "children": [{"label": "Python"}, {"label": "Go"}]},
                ]
            }
        },
    },

    # ---- Relation 类型 (已修复) ----
    "relation-dagre-flow": {
        "template": "relation-dagre-flow-tb-simple-circle-node",
        "category": "relation",
        "data": {
            "nodes": [
                {"id": "A", "label": "数据采集"},
                {"id": "B", "label": "数据处理"},
                {"id": "C", "label": "数据存储"},
                {"id": "D", "label": "数据展示"},
            ],
            "relations": [
                {"from": "A", "to": "B"},
                {"from": "B", "to": "C"},
                {"from": "C", "to": "D"},
            ]
        },
    },

    # ---- Compare Binary 类型 (已修复) ----
    "compare-binary": {
        "template": "compare-binary-horizontal-underline-text-vs",
        "category": "comparison",
        "data": {
            "compares": [
                {"label": "传统方法", "children": ["人工处理", "效率低", "成本高"]},
                {"label": "AI 方法", "children": ["自动化", "效率高", "成本低"]},
            ]
        },
    },

    # ---- Compare Hierarchy 类型 (已修复) ----
    "compare-hierarchy": {
        "template": "compare-hierarchy-left-right-circle-node-pill-badge",
        "category": "comparison",
        "data": {
            "compares": [
                {"label": "方案A", "children": ["优点1", "优点2", "优点3"]},
                {"label": "方案B", "children": ["特点1", "特点2", "特点3"]},
            ]
        },
    },

    # ---- Compare SWOT 类型 (已修复) ----
    "compare-swot": {
        "template": "compare-swot",
        "category": "comparison",
        "data": {
            "compares": [
                {"label": "优势 (Strengths)", "children": ["技术领先", "团队强大"]},
                {"label": "劣势 (Weaknesses)", "children": ["资金有限", "品牌知名度低"]},
                {"label": "机会 (Opportunities)", "children": ["市场增长", "政策支持"]},
                {"label": "威胁 (Threats)", "children": ["竞争激烈", "技术变革"]},
            ]
        },
    },

    # ---- Quadrant 类型 ----
    "quadrant-quarter": {
        "template": "compare-quadrant-quarter-simple-card",
        "category": "quadrant",
        "data": {
            "compares": [
                {"label": "高价值/高成本", "children": ["策略A", "策略B"]},
                {"label": "高价值/低成本", "children": ["策略C"]},
                {"label": "低价值/高成本", "children": ["策略D"]},
                {"label": "低价值/低成本", "children": ["策略E", "策略F"]},
            ]
        },
    },
}


def run_tests():
    """运行所有工具渲染测试"""
    print("\n" + "=" * 60)
    print("🧪 Tool Rendering Tests")
    print("=" * 60)

    # 确保输出目录存在
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"\n📁 Output directory: {OUTPUT_DIR}")

    results = {"success": [], "failed": []}

    for tool_name, test_case in TEST_CASES.items():
        print(f"\n{'─' * 40}")
        print(f"🔧 Testing: {tool_name}")
        print(f"   Template: {test_case['template']}")

        try:
            # 1. 生成 DSL
            dsl = generate_dsl(
                template=test_case["template"],
                category=test_case["category"],
                data=test_case["data"],
            )
            print(f"   ✅ DSL generated ({len(dsl)} chars)")

            # 打印 DSL 预览 (前几行)
            dsl_lines = dsl.split("\n")[:5]
            for line in dsl_lines:
                print(f"      │ {line}")
            if len(dsl.split("\n")) > 5:
                print(f"      │ ... ({len(dsl.split(chr(10))) - 5} more lines)")

            # 2. 渲染 SVG
            result = render_to_svg(dsl)

            if result["success"]:
                svg_content = result["svg"]
                # 3. 保存 SVG
                output_path = OUTPUT_DIR / f"test-{tool_name}.svg"
                save_svg(svg_content, output_path)
                print(f"   ✅ SVG saved: {output_path.name} ({len(svg_content)} bytes)")
                results["success"].append(tool_name)
            else:
                error_msg = result.get("error", "Unknown error")
                print(f"   ❌ Render failed: {error_msg}")
                results["failed"].append((tool_name, error_msg))

        except Exception as e:
            print(f"   ❌ Exception: {e}")
            results["failed"].append((tool_name, str(e)))

    # 打印总结
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    print(f"   ✅ Success: {len(results['success'])} / {len(TEST_CASES)}")
    print(f"   ❌ Failed:  {len(results['failed'])} / {len(TEST_CASES)}")

    if results["success"]:
        print("\n   Successful tools:")
        for name in results["success"]:
            print(f"      • {name}")

    if results["failed"]:
        print("\n   Failed tools:")
        for name, error in results["failed"]:
            print(f"      • {name}: {error[:50]}...")

    print("\n" + "=" * 60)

    # 返回退出码
    return 0 if not results["failed"] else 1


if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
