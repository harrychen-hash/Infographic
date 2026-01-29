"""
[INPUT]: OPENAI_* 环境变量 (API_KEY, MODEL, TEMPERATURE, TOP_P, 等)
[OUTPUT]: get_openai_client(), get_default_model(), get_model_settings()
[POS]: agentic/utils 的客户端工具，提供 OpenAI SDK 初始化和完整模型配置

[PROTOCOL]:
1. 一旦本文件逻辑变更，必须同步更新此 Header。
2. 更新后必须上浮检查 utils/.folder.md 的描述是否仍然准确。
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Literal, Optional


def _load_env_file(file_path: Path, key: str) -> Optional[str]:
    """从 .env 文件读取指定的环境变量"""
    if not file_path.exists():
        return None

    content = file_path.read_text()
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue

        k, v = line.split("=", 1)
        k = k.strip()
        v = v.strip().strip("\"'")

        if k == key and v:
            return v

    return None


def _get_env_value(key: str, default: str = "") -> str:
    """获取环境变量，优先从 os.environ，其次从 .env.local 文件"""
    # 1. 优先从环境变量获取
    value = os.environ.get(key, "")
    if value:
        return value

    # 2. 尝试从 .env.local 文件读取
    candidates = [
        Path.cwd() / ".env.local",
        Path.cwd() / "site" / ".env.local",
        Path(__file__).parent.parent.parent.parent.parent / ".env.local",
    ]

    for env_path in candidates:
        value = _load_env_file(env_path, key)
        if value:
            return value

    return default


def _get_api_key() -> str:
    """获取 OpenAI API Key"""
    key = _get_env_value("OPENAI_API_KEY")
    if key and "your-api" not in key.lower():
        return key

    raise ValueError(
        "OPENAI_API_KEY is missing. Set it in site/.env.local or as environment variable."
    )


@lru_cache(maxsize=1)
def get_openai_client():
    """获取 OpenAI 客户端实例（单例模式）"""
    from openai import OpenAI
    api_key = _get_api_key()
    return OpenAI(api_key=api_key)


def get_default_model() -> str:
    """获取默认模型名称"""
    return _get_env_value("OPENAI_MODEL", "gpt-4o")


def _parse_float(value: str, default: float | None = None) -> float | None:
    """解析浮点数，失败返回 default"""
    if not value:
        return default
    try:
        return float(value)
    except ValueError:
        return default


def _parse_int(value: str, default: int | None = None) -> int | None:
    """解析整数，失败返回 default"""
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def _parse_bool(value: str, default: bool | None = None) -> bool | None:
    """解析布尔值，失败返回 default"""
    if not value:
        return default
    return value.lower() in ("true", "1", "yes", "on")


def _parse_literal(value: str, valid: tuple, default: str | None = None) -> str | None:
    """解析字面量，不在有效值中返回 default"""
    if not value:
        return default
    return value if value in valid else default


def _is_reasoning_model(model: str) -> bool:
    """检查是否为推理模型 (GPT-5.x, o1, o3 等)，这些模型不支持 temperature 等采样参数"""
    model_lower = model.lower()
    # GPT-5.x 系列
    if model_lower.startswith("gpt-5"):
        return True
    # o1, o3 系列 (reasoning models)
    if model_lower.startswith("o1") or model_lower.startswith("o3"):
        return True
    return False


@lru_cache(maxsize=1)
def get_model_settings():
    """获取完整的 ModelSettings 配置

    从环境变量读取所有 OpenAI Agents SDK 支持的 ModelSettings 参数。
    返回 ModelSettings 实例，可直接传给 Agent 的 model_settings 参数。

    注意: GPT-5.x 和 o1/o3 等推理模型不支持 temperature, top_p, frequency_penalty,
    presence_penalty 等采样参数，会自动排除。

    支持的环境变量:
    - OPENAI_TEMPERATURE: 采样温度 (0-2) [非推理模型]
    - OPENAI_TOP_P: nucleus 采样 (0-1) [非推理模型]
    - OPENAI_FREQUENCY_PENALTY: 频率惩罚 (-2 to 2) [非推理模型]
    - OPENAI_PRESENCE_PENALTY: 存在惩罚 (-2 to 2) [非推理模型]
    - OPENAI_MAX_TOKENS: 最大输出 token 数
    - OPENAI_REASONING_EFFORT: GPT-5.x 推理强度 (none|low|medium|high)
    - OPENAI_VERBOSITY: GPT-5.x 输出详细度 (low|medium|high)
    - OPENAI_PARALLEL_TOOL_CALLS: 是否并行调用工具 (true|false)
    - OPENAI_TRUNCATION: 截断策略 (auto|disabled)
    - OPENAI_STORE: 是否存储到 OpenAI (true|false)
    """
    # 延迟导入，避免循环依赖
    from agents import ModelSettings

    # 获取当前模型
    model = get_default_model()
    is_reasoning = _is_reasoning_model(model)

    # 构建 ModelSettings 参数 (只传非 None 的值)
    settings_kwargs: dict[str, Any] = {}

    # 采样参数 - 仅非推理模型支持
    if not is_reasoning:
        temperature = _parse_float(_get_env_value("OPENAI_TEMPERATURE"))
        top_p = _parse_float(_get_env_value("OPENAI_TOP_P"))
        frequency_penalty = _parse_float(_get_env_value("OPENAI_FREQUENCY_PENALTY"))
        presence_penalty = _parse_float(_get_env_value("OPENAI_PRESENCE_PENALTY"))

        if temperature is not None:
            settings_kwargs["temperature"] = temperature
        if top_p is not None:
            settings_kwargs["top_p"] = top_p
        if frequency_penalty is not None:
            settings_kwargs["frequency_penalty"] = frequency_penalty
        if presence_penalty is not None:
            settings_kwargs["presence_penalty"] = presence_penalty

    # 通用参数
    max_tokens = _parse_int(_get_env_value("OPENAI_MAX_TOKENS"))
    parallel_tool_calls = _parse_bool(_get_env_value("OPENAI_PARALLEL_TOOL_CALLS"))
    truncation = _parse_literal(
        _get_env_value("OPENAI_TRUNCATION"),
        ("auto", "disabled"),
    )
    store = _parse_bool(_get_env_value("OPENAI_STORE"))

    if max_tokens is not None:
        settings_kwargs["max_tokens"] = max_tokens
    if parallel_tool_calls is not None:
        settings_kwargs["parallel_tool_calls"] = parallel_tool_calls
    if truncation is not None:
        settings_kwargs["truncation"] = truncation
    if store is not None:
        settings_kwargs["store"] = store

    # 推理模型专用参数
    if is_reasoning:
        reasoning_effort = _parse_literal(
            _get_env_value("OPENAI_REASONING_EFFORT"),
            ("none", "low", "medium", "high"),
        )
        verbosity = _parse_literal(
            _get_env_value("OPENAI_VERBOSITY"),
            ("low", "medium", "high"),
        )

        if verbosity is not None:
            settings_kwargs["verbosity"] = verbosity

        if reasoning_effort is not None:
            try:
                from openai.types.shared import Reasoning
                settings_kwargs["reasoning"] = Reasoning(effort=reasoning_effort)
            except ImportError:
                # openai SDK 版本不支持
                pass

    return ModelSettings(**settings_kwargs)


# 兼容性别名
def get_default_temperature() -> float:
    """获取默认 temperature 值 (兼容性函数)"""
    value = _get_env_value("OPENAI_TEMPERATURE", "1.0")
    try:
        return float(value)
    except ValueError:
        return 1.0
