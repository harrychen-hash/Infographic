"""
[INPUT]: 测试文章文本
[OUTPUT]: 打印切分结果
[POS]: agentic 模块的测试脚本

[PROTOCOL]:
1. 一旦本文件逻辑变更，必须同步更新此 Header。
2. 更新后必须上浮检查 .folder.md 的描述是否仍然准确。

Usage:
    cd site/src/lib
    pip install -r agentic/requirements.txt
    python -m agentic.test_segmentation
"""

import json
import sys
from pathlib import Path

# 确保父目录在 Python 路径中
sys.path.insert(0, str(Path(__file__).parent.parent))

from agentic.agents import segment_article_sync
from agentic.models import ArticleSegmentation

# 测试文章
TEST_ARTICLE = """
# 人工智能正在改变医疗行业

人工智能技术在医疗领域的应用正在快速增长。根据最新研究，AI 辅助诊断的准确率已经达到 95%，在某些领域甚至超过了人类医生。

## 诊断领域的突破

在影像诊断方面，深度学习算法已经能够识别 X 光、CT 和 MRI 图像中的异常。谷歌的 DeepMind 团队开发的系统在眼科疾病诊断中表现出色，能够检测出 50 多种眼部疾病。

这些系统不仅提高了诊断速度，还降低了误诊率。据统计，AI 辅助诊断可以将误诊率降低约 30%。

## 药物研发的加速

传统药物研发需要 10-15 年时间，成本高达数十亿美元。而 AI 可以大幅缩短这一周期。

AlphaFold 预测蛋白质结构的突破性进展，使得科学家能够更快地理解疾病机制。这项技术已经被用于研究新冠病毒和潜在的治疗方案。

## 面临的挑战

尽管前景光明，AI 医疗仍面临诸多挑战。数据隐私、算法偏见、以及监管框架的不完善都是需要解决的问题。

医疗 AI 的决策过程往往是"黑箱"，这在需要高度透明度的医疗领域引发了担忧。如何确保 AI 系统的可解释性和可追溯性，是当前研究的重点之一。
"""


def main():
    print("=" * 60)
    print("Article Segmentation Agent Test")
    print("=" * 60)
    print()

    print("Input article length:", len(TEST_ARTICLE), "characters")
    print()

    print("Running segmentation...")
    result: ArticleSegmentation = segment_article_sync(TEST_ARTICLE)

    print()
    print("=" * 60)
    print(f"Found {len(result.intents)} intents:")
    print("=" * 60)

    for i, intent in enumerate(result.intents, 1):
        print(f"\n[Intent {i}]")
        print(f"  Description: {intent.intent}")
        print(f"  Paragraphs ({len(intent.paragraphs)}):")
        for j, para in enumerate(intent.paragraphs, 1):
            preview = para[:100] + "..." if len(para) > 100 else para
            print(f"    {j}. {preview}")

    print()
    print("=" * 60)
    print("Raw JSON output:")
    print("=" * 60)
    print(json.dumps(result.model_dump(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
