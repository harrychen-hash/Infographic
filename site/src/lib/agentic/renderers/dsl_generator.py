"""
[INPUT]: TemplateSelection (template, data, category)
[OUTPUT]: DSL 语法字符串
[POS]: 将 Python 数据结构转换为 @antv/infographic DSL 格式（按官方 DataSchema）

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

from typing import Any, Dict, Iterable, List, Optional

from ..config.palette import AI_COLOR_PALETTE

DATA_KEY_ORDER = [
    "title",
    "desc",
    "xTitle",           # chart 轴标题
    "yTitle",           # chart 轴标题
    "primaryYTitle",    # chart-combo: 左Y轴标题
    "secondaryYTitle",  # chart-combo: 右Y轴标题
    "primaryLabel",     # chart-combo: 左轴图例
    "secondaryLabel",   # chart-combo: 右轴图例
    "primaryMin",       # chart-combo: 左轴起始值
    "primaryMax",       # chart-combo: 左轴最大值
    "primaryStep",      # chart-combo: 左轴刻度间隔
    "secondaryMin",     # chart-combo: 右轴起始值
    "secondaryMax",     # chart-combo: 右轴最大值
    "secondaryStep",    # chart-combo: 右轴刻度间隔
    "items",
    "lists",
    "sequences",
    "root",
    "compares",
    "nodes",
    "relations",
    "values",
    "primaryValues",    # chart-combo: 柱状图数据（左轴）
    "secondaryValues",  # chart-combo: 折线图数据（右轴）
    "order",
    "illus",
    "attributes",
]

ITEM_KEY_ORDER = [
    "id",
    "label",
    "value",
    "desc",
    "icon",
    "illus",
    "attributes",
    "group",
    "category",
    "children",
]

RELATION_KEY_ORDER = [
    "id",
    "from",
    "to",
    "label",
    "direction",
    "showArrow",
    "arrowType",
]

INLINE_KEY_PREFS = {
    "items": ["label", "id", "value", "title"],
    "lists": ["label", "id", "value", "title"],
    "sequences": ["label", "id", "value", "title"],
    "values": ["label", "id", "value", "title"],
    "primaryValues": ["label", "id", "value", "title"],    # chart-combo
    "secondaryValues": ["label", "id", "value", "title"],  # chart-combo
    "compares": ["label", "id", "value", "title"],
    "nodes": ["id", "label", "value", "title"],
    "children": ["label", "id", "value", "title"],
    "default": ["label", "id", "value", "title"],
}


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
    # chart-combo 需要 values 占位字段以通过 isCompleteParsedInfographicOptions() 检查
    if template == "chart-combo" and "values" not in data:
        data = {**data, "values": [{"label": "placeholder", "value": 0}]}

    lines = [f"infographic {template}"]
    lines.append("data")
    lines.extend(_generate_data_block(data, title=title, desc=desc))

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


def _generate_data_block(
    data: Dict[str, Any],
    title: Optional[str] = None,
    desc: Optional[str] = None,
) -> List[str]:
    """生成 data 部分（按官方 DataSchema 渲染）"""
    lines: List[str] = []

    effective_title = title if title is not None else data.get("title")
    effective_desc = desc if desc is not None else data.get("desc")

    if effective_title:
        lines.append(f"  title {_format_scalar(effective_title)}")
    if effective_desc:
        lines.append(f"  desc {_format_scalar(effective_desc)}")

    for key in DATA_KEY_ORDER:
        if key in ("title", "desc"):
            continue
        if key not in data:
            continue
        _emit_key_value(lines, key, data.get(key), indent=2)

    return lines


def _emit_key_value(
    lines: List[str],
    key: str,
    value: Any,
    indent: int,
) -> None:
    if _is_empty(value):
        return

    prefix = " " * indent
    if isinstance(value, list):
        lines.append(f"{prefix}{key}")
        _emit_list(lines, key, value, indent + 2)
        return

    if isinstance(value, dict):
        lines.append(f"{prefix}{key}")
        if key == "root":
            _emit_object(lines, value, indent + 2, key_order=ITEM_KEY_ORDER)
        else:
            _emit_object(lines, value, indent + 2)
        return

    lines.append(f"{prefix}{key} {_format_scalar(value)}")


def _emit_object(
    lines: List[str],
    obj: Dict[str, Any],
    indent: int,
    key_order: Optional[List[str]] = None,
) -> None:
    for key in _ordered_keys(obj, key_order):
        _emit_key_value(lines, key, obj.get(key), indent)


def _emit_list(
    lines: List[str],
    key: str,
    items: Iterable[Any],
    indent: int,
) -> None:
    if key == "relations":
        _emit_relations(lines, items, indent)
        return

    for item in items:
        if isinstance(item, dict):
            inline_prefs = INLINE_KEY_PREFS.get(key, INLINE_KEY_PREFS["default"])
            _emit_object_item(
                lines,
                item,
                indent,
                inline_prefs=inline_prefs,
                key_order=ITEM_KEY_ORDER,
            )
        else:
            lines.append(f"{' ' * indent}- {_format_scalar(item)}")


def _emit_object_item(
    lines: List[str],
    item: Dict[str, Any],
    indent: int,
    inline_prefs: List[str],
    key_order: Optional[List[str]] = None,
) -> None:
    inline_key = _pick_inline_key(item, inline_prefs)
    prefix = " " * indent
    if inline_key:
        lines.append(
            f"{prefix}- {inline_key} {_format_scalar(item.get(inline_key))}"
        )
    else:
        lines.append(f"{prefix}-")

    for key in _ordered_keys(item, key_order):
        if key == inline_key:
            continue
        if key == "children" and isinstance(item.get(key), list):
            _emit_key_value(lines, key, item.get(key), indent + 2)
            continue
        _emit_key_value(lines, key, item.get(key), indent + 2)


def _emit_relations(lines: List[str], items: Iterable[Any], indent: int) -> None:
    prefix = " " * indent
    for rel in items:
        if isinstance(rel, dict):
            from_value = rel.get("from")
            to_value = rel.get("to")
            extra_keys = [k for k in rel.keys() if k not in ("from", "to")]
            if (
                from_value is not None
                and to_value is not None
                and not extra_keys
            ):
                lines.append(
                    f"{prefix}{_format_scalar(from_value)} -> {_format_scalar(to_value)}"
                )
            else:
                _emit_object_item(
                    lines,
                    rel,
                    indent,
                    inline_prefs=["from", "id", "label"],
                    key_order=RELATION_KEY_ORDER,
                )
        else:
            lines.append(f"{prefix}{_format_scalar(rel)}")


def _is_empty(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str) and not value.strip():
        return True
    if isinstance(value, (list, tuple, dict)) and len(value) == 0:
        return True
    return False


def _is_scalar(value: Any) -> bool:
    return isinstance(value, (str, int, float, bool))


def _format_scalar(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    return _escape_value(str(value))


def _pick_inline_key(item: Dict[str, Any], prefs: List[str]) -> Optional[str]:
    for key in prefs:
        if key in item and _is_scalar(item.get(key)) and not _is_empty(item.get(key)):
            return key
    for key in item.keys():
        if _is_scalar(item.get(key)) and not _is_empty(item.get(key)):
            return key
    return None


def _ordered_keys(obj: Dict[str, Any], preferred: Optional[List[str]]) -> List[str]:
    keys = list(obj.keys())
    if not preferred:
        return keys
    ordered = [key for key in preferred if key in obj]
    ordered.extend([key for key in keys if key not in ordered])
    return ordered
