"""
[INPUT]: TemplateSelection (template, data, category)
[OUTPUT]: DSL 语法字符串
[POS]: 将 Python 数据结构转换为 @antv/infographic DSL 格式

[PROTOCOL]:
1. 一旦本文件逻辑变更，必须同步更新此 Header。
2. 更新后必须上浮检查 renderers/.folder.md 的描述是否仍然准确。

DSL 格式示例:
```
infographic chart-bar-plain-text
data
  title 年度业务指标
  values
    - label 产品创新
      value 85
theme
  palette #21EF6A #00D0FF #8F53ED
```
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..config.palette import AI_COLOR_PALETTE


def generate_dsl(
    template: str,
    category: str,
    data: Dict[str, Any],
    title: Optional[str] = None,
    desc: Optional[str] = None,
) -> str:
    """将 TemplateSelection 数据转换为 DSL 语法字符串

    Args:
        template: 模板名称，如 chart-bar-plain-text
        category: 分类，如 chart, list, sequence
        data: 填充数据，结构取决于 category
        title: 可选标题
        desc: 可选描述

    Returns:
        DSL 语法字符串
    """
    lines = [f"infographic {template}"]
    lines.append("data")

    # 添加 title 和 desc
    if title:
        lines.append(f"  title {_escape_value(title)}")
    if desc:
        lines.append(f"  desc {_escape_value(desc)}")

    # 根据 category 生成对应的 data 部分
    if category == "chart":
        lines.extend(_generate_chart_data(data))
    elif category == "list":
        lines.extend(_generate_list_data(data))
    elif category == "sequence":
        lines.extend(_generate_sequence_data(data))
    elif category == "comparison":
        lines.extend(_generate_compare_data(data))
    elif category == "hierarchy":
        lines.extend(_generate_hierarchy_data(data))
    elif category == "relation":
        lines.extend(_generate_relation_data(data))
    elif category == "quadrant":
        lines.extend(_generate_quadrant_data(data))

    # 添加 theme
    lines.append("theme")
    palette_colors = list(AI_COLOR_PALETTE["primary"].values())
    lines.append(f"  palette {' '.join(palette_colors)}")

    return "\n".join(lines)


def _escape_value(value: str) -> str:
    """转义 DSL 值中的特殊字符"""
    if not value:
        return ""
    # 如果包含空格或特殊字符，需要处理
    # DSL 使用缩进解析，换行符需要移除
    return value.replace("\n", " ").replace("\r", "").strip()


def _generate_chart_data(data: Dict[str, Any]) -> List[str]:
    """生成 chart 类型的 data 部分

    数据格式: {"values": [{"label": str, "value": num, "desc"?: str}]}
    """
    lines = []
    values = data.get("values", [])

    if values:
        lines.append("  values")
        for item in values:
            lines.append(f"    - label {_escape_value(item.get('label', ''))}")
            if "value" in item:
                lines.append(f"      value {item['value']}")
            if "desc" in item and item["desc"]:
                lines.append(f"      desc {_escape_value(item['desc'])}")

    return lines


def _generate_list_data(data: Dict[str, Any]) -> List[str]:
    """生成 list 类型的 data 部分

    数据格式: {"lists": [{"label": str, "desc"?: str, "icon"?: str}]}
    """
    lines = []
    lists = data.get("lists", [])

    if lists:
        lines.append("  lists")
        for item in lists:
            lines.append(f"    - label {_escape_value(item.get('label', ''))}")
            if "desc" in item and item["desc"]:
                lines.append(f"      desc {_escape_value(item['desc'])}")
            if "icon" in item and item["icon"]:
                lines.append(f"      icon {item['icon']}")
            if "value" in item:
                lines.append(f"      value {item['value']}")

    return lines


def _generate_sequence_data(data: Dict[str, Any]) -> List[str]:
    """生成 sequence 类型的 data 部分

    数据格式: {"sequences": [{"label": str, "desc"?: str, "time"?: str}]}
    """
    lines = []
    sequences = data.get("sequences", [])

    if sequences:
        lines.append("  sequences")
        for item in sequences:
            lines.append(f"    - label {_escape_value(item.get('label', ''))}")
            if "desc" in item and item["desc"]:
                lines.append(f"      desc {_escape_value(item['desc'])}")
            if "time" in item and item["time"]:
                lines.append(f"      time {item['time']}")
            if "icon" in item and item["icon"]:
                lines.append(f"      icon {item['icon']}")

    return lines


def _generate_compare_data(data: Dict[str, Any]) -> List[str]:
    """生成 compare 类型的 data 部分

    数据格式: {"compares": [{"label": str, "value"?: num, "children"?: [...]}]}
    """
    lines = []
    compares = data.get("compares", [])

    if compares:
        lines.append("  compares")
        for item in compares:
            lines.append(f"    - label {_escape_value(item.get('label', ''))}")
            if "value" in item:
                lines.append(f"      value {item['value']}")
            if "desc" in item and item["desc"]:
                lines.append(f"      desc {_escape_value(item['desc'])}")
            # 处理 children (用于 SWOT 等)
            children = item.get("children", [])
            if children:
                lines.append("      children")
                for child in children:
                    if isinstance(child, dict):
                        lines.append(f"        - label {_escape_value(child.get('label', ''))}")
                    else:
                        lines.append(f"        - label {_escape_value(str(child))}")

    return lines


def _generate_hierarchy_data(data: Dict[str, Any]) -> List[str]:
    """生成 hierarchy 类型的 data 部分

    数据格式: {"root": {"label": str, "children": [...]}}
    """
    lines = []
    root = data.get("root", {})

    if root:
        lines.append("  root")
        lines.extend(_generate_tree_node(root, indent=4))

    return lines


def _generate_tree_node(node: Dict[str, Any], indent: int) -> List[str]:
    """递归生成树节点"""
    lines = []
    prefix = " " * indent

    lines.append(f"{prefix}label {_escape_value(node.get('label', ''))}")

    if "desc" in node and node["desc"]:
        lines.append(f"{prefix}desc {_escape_value(node['desc'])}")

    children = node.get("children", [])
    if children:
        lines.append(f"{prefix}children")
        for child in children:
            lines.append(f"{prefix}  - label {_escape_value(child.get('label', ''))}")
            # 递归处理子节点的 children
            sub_children = child.get("children", [])
            if sub_children:
                lines.append(f"{prefix}    children")
                for sub in sub_children:
                    if isinstance(sub, dict):
                        lines.append(f"{prefix}      - label {_escape_value(sub.get('label', ''))}")
                    else:
                        lines.append(f"{prefix}      - label {_escape_value(str(sub))}")

    return lines


def _generate_relation_data(data: Dict[str, Any]) -> List[str]:
    """生成 relation 类型的 data 部分

    数据格式: {
        "nodes": [{"id": str, "label": str}],
        "relations": [{"from": str, "to": str}] 或 ["A -> B", ...]
    }
    """
    lines = []
    nodes = data.get("nodes", [])
    relations = data.get("relations", data.get("edges", []))

    if nodes:
        lines.append("  nodes")
        for node in nodes:
            lines.append(f"    - id {node.get('id', '')}")
            lines.append(f"      label {_escape_value(node.get('label', ''))}")
            if "desc" in node and node["desc"]:
                lines.append(f"      desc {_escape_value(node['desc'])}")

    if relations:
        lines.append("  relations")
        for rel in relations:
            if isinstance(rel, dict):
                # {"from": "A", "to": "B"}
                lines.append(f"    {rel.get('from', '')} -> {rel.get('to', '')}")
            else:
                # 字符串格式 "A -> B"
                lines.append(f"    {rel}")

    return lines


def _generate_quadrant_data(data: Dict[str, Any]) -> List[str]:
    """生成 quadrant 类型的 data 部分

    数据格式: {"compares": [{"label": str, "icon"?: str}]} (4 个象限)
    """
    # quadrant 使用 compares 字段，与 compare 类似
    return _generate_compare_data(data)
