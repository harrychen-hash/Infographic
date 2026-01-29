"""
[INPUT]: 无
[OUTPUT]: logger 实例，日志配置函数
[POS]: agentic/utils 的日志模块，提供结构化日志记录

[PROTOCOL]:
1. 一旦本文件逻辑变更，必须同步更新此 Header。
2. 更新后必须上浮检查 utils/.folder.md 的描述是否仍然准确。
"""

from __future__ import annotations

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

# 日志目录
LOG_DIR = Path(__file__).parent.parent.parent.parent.parent / "logs" / "agentic"


class ColoredFormatter(logging.Formatter):
    """带颜色的控制台日志格式化器"""

    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
        "RESET": "\033[0m",
    }

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
        reset = self.COLORS["RESET"]
        record.levelname = f"{color}{record.levelname}{reset}"
        return super().format(record)


class JSONFormatter(logging.Formatter):
    """JSON 格式的日志格式化器（用于文件日志）"""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # 添加额外字段
        if hasattr(record, "extra_data"):
            log_data["data"] = record.extra_data

        return json.dumps(log_data, ensure_ascii=False, default=str)


def setup_logger(
    name: str = "agentic",
    level: int = logging.INFO,
    log_to_file: bool = True,
    log_to_console: bool = True,
) -> logging.Logger:
    """
    设置并返回 logger 实例

    Args:
        name: logger 名称
        level: 日志级别
        log_to_file: 是否输出到文件
        log_to_console: 是否输出到控制台

    Returns:
        配置好的 logger 实例
    """
    logger = logging.getLogger(name)

    # 避免重复配置
    if logger.handlers:
        return logger

    logger.setLevel(level)
    logger.propagate = False

    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_formatter = ColoredFormatter(
            "%(asctime)s │ %(levelname)s │ %(name)s │ %(message)s",
            datefmt="%H:%M:%S",
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    if log_to_file:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        log_file = LOG_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.jsonl"
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(JSONFormatter())
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str = "agentic") -> logging.Logger:
    """获取 logger 实例（如果不存在则创建）"""
    logger = logging.getLogger(name)
    if not logger.handlers:
        return setup_logger(name)
    return logger


class PipelineLogger:
    """Pipeline 专用日志记录器，提供结构化的日志方法"""

    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or get_logger("agentic.pipeline")

    def start_pipeline(self, article_length: int) -> None:
        """记录 pipeline 开始"""
        self.logger.info(f"🚀 Pipeline started | Article length: {article_length} chars")

    def end_pipeline(self, intent_count: int, success_count: int, duration: float) -> None:
        """记录 pipeline 结束"""
        self.logger.info(
            f"✅ Pipeline completed | Intents: {intent_count} | "
            f"Success: {success_count} | Duration: {duration:.2f}s"
        )

    def segmentation_start(self) -> None:
        """记录切分开始"""
        self.logger.info("📝 Segmentation started")

    def segmentation_complete(self, intent_count: int, duration: float) -> None:
        """记录切分完成"""
        self.logger.info(
            f"📝 Segmentation complete | Intents: {intent_count} | Duration: {duration:.2f}s"
        )

    def intent_processing_start(self, index: int, intent: str) -> None:
        """记录单个 intent 处理开始"""
        short_intent = intent[:50] + "..." if len(intent) > 50 else intent
        self.logger.info(f"🔄 [{index}] Processing intent: {short_intent}")

    def intent_processing_complete(
        self, index: int, category: str, template: str, duration: float
    ) -> None:
        """记录单个 intent 处理完成"""
        self.logger.info(
            f"✓  [{index}] Selected: {category}/{template} | Duration: {duration:.2f}s"
        )

    def intent_skipped(self, index: int, reason: str) -> None:
        """记录 intent 被跳过"""
        self.logger.info(f"⏭  [{index}] Skipped: {reason}")

    def intent_error(self, index: int, error: str) -> None:
        """记录 intent 处理错误"""
        self.logger.error(f"❌ [{index}] Error: {error}")

    def handoff(self, from_agent: str, to_agent: str) -> None:
        """记录 agent handoff"""
        self.logger.debug(f"🔀 Handoff: {from_agent} → {to_agent}")

    def tool_call(self, agent: str, tool: str, result_preview: str) -> None:
        """记录 tool 调用"""
        self.logger.debug(f"🔧 [{agent}] Called {tool}: {result_preview[:100]}")

    def render_start(self, index: int, template: str) -> None:
        """记录渲染开始"""
        self.logger.info(f"🎨 [{index}] Rendering: {template}")

    def render_complete(self, index: int, output_path: str, duration: float) -> None:
        """记录渲染完成"""
        self.logger.info(f"✅ [{index}] Saved: {output_path} | Duration: {duration:.2f}s")

    def render_error(self, index: int, error: str) -> None:
        """记录渲染错误"""
        self.logger.error(f"❌ [{index}] Render failed: {error}")

    def render_skipped(self, index: int, reason: str) -> None:
        """记录跳过渲染"""
        self.logger.info(f"⏭  [{index}] Render skipped: {reason}")


def get_log_dir() -> Path:
    """获取日志目录路径"""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    return LOG_DIR


def get_current_log_file() -> Path:
    """获取当前日志文件路径"""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    return LOG_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.jsonl"


# 默认 logger 实例
pipeline_logger = PipelineLogger()
