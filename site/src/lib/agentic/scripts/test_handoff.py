"""
[INPUT]: template_selector agent, 8 个测试用例
[OUTPUT]: 每个用例的 handoff 目标和最终 category
[POS]: 验证 template_selector 的 handoff 准确性 (包括 skip 场景)

[PROTOCOL]:
1. 一旦本文件逻辑变更，必须同步更新此 Header。
2. 更新后必须上浮检查 scripts/.folder.md 的描述是否仍然准确。

Usage:
    cd site/src/lib
    python -m agentic.scripts.test_handoff
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

# 确保父目录在 Python 路径中
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents import Runner

from agentic.agents.template_selector import template_selector
from agentic.models import TemplateSelection


# 测试用例：每个 category 一个典型案例
TEST_CASES = [
    {
        "name": "List Agent",
        "expected_category": "list",
        "intent": "AI 医疗面临的挑战及其解决需求",
        "paragraphs": [
            "尽管前景光明，AI 医疗仍面临诸多挑战：数据隐私问题、算法偏见、监管合规等。",
            "医疗 AI 的决策过程往往是'黑箱'，这给医生和患者带来信任问题。",
            "此外，不同医院的数据格式不统一，导致模型难以泛化。",
        ],
    },
    {
        "name": "Chart Agent",
        "expected_category": "chart",
        "intent": "2023年各科技公司市场份额分析",
        "paragraphs": [
            "根据最新数据，苹果占据智能手机市场 27% 的份额，三星紧随其后占 21%。",
            "小米和 OPPO 分别以 12% 和 9% 的份额位列第三和第四。",
            "其他品牌共计占据剩余 31% 的市场份额。",
        ],
    },
    {
        "name": "Comparison Agent",
        "expected_category": "comparison",
        "intent": "传统方法 vs AI 方法的优劣对比",
        "paragraphs": [
            "传统诊断方法依赖医生经验，准确率约 70%，但解释性强。",
            "AI 辅助诊断准确率可达 95%，但缺乏可解释性，且需要大量标注数据。",
            "在成本方面，传统方法人力成本高，AI 方法前期投入大但边际成本低。",
        ],
    },
    {
        "name": "Hierarchy Agent",
        "expected_category": "hierarchy",
        "intent": "机器学习知识体系的层级结构",
        "paragraphs": [
            "机器学习可分为监督学习、无监督学习和强化学习三大类。",
            "监督学习下又包含分类和回归两个子类别。",
            "分类任务常用算法包括决策树、SVM、神经网络等。",
        ],
    },
    {
        "name": "Sequence Agent",
        "expected_category": "sequence",
        "intent": "产品开发的五个阶段",
        "paragraphs": [
            "第一阶段：需求分析，收集用户需求并确定产品方向。",
            "第二阶段：设计原型，创建交互原型和视觉设计。",
            "第三阶段：开发实现，编码实现功能并进行单元测试。",
            "第四阶段：测试验收，进行集成测试和用户验收测试。",
            "第五阶段：发布上线，部署到生产环境并监控运行。",
        ],
    },
    {
        "name": "Quadrant Agent",
        "expected_category": "quadrant",
        "intent": "技术成熟度与市场需求的四象限分析",
        "paragraphs": [
            "高成熟度+高需求（明星）：云计算、移动支付。",
            "高成熟度+低需求（现金牛）：传统数据库、ERP系统。",
            "低成熟度+高需求（问号）：量子计算、脑机接口。",
            "低成熟度+低需求（瘦狗）：某些小众技术领域。",
        ],
    },
    {
        "name": "Relation Agent",
        "expected_category": "relation",
        "intent": "微服务架构中各模块之间的依赖关系",
        "paragraphs": [
            "用户服务依赖认证服务进行身份验证。",
            "订单服务需要调用用户服务获取用户信息，同时依赖库存服务检查库存。",
            "支付服务与订单服务双向通信，完成支付后更新订单状态。",
            "所有服务都通过消息队列进行异步解耦。",
        ],
    },
    {
        "name": "Skip Agent",
        "expected_category": "skip",
        "intent": "文章开篇引言",
        "paragraphs": [
            "在这个快速变化的时代，技术创新正以前所未有的速度改变着我们的生活。",
            "回首过去十年，我们见证了无数激动人心的变革。",
            "本文将带您一起探索这些变化背后的故事。",
        ],
    },
]


async def test_single_handoff(case: dict) -> dict:
    """测试单个用例的 handoff"""
    input_text = f"""## 意图
{case["intent"]}

## 段落内容
{chr(10).join(case["paragraphs"])}
"""

    print(f"\n{'='*60}")
    print(f"测试: {case['name']}")
    print(f"预期 Category: {case['expected_category']}")
    print(f"{'='*60}")
    print(f"输入意图: {case['intent'][:50]}...")

    try:
        result = await Runner.run(template_selector, input_text)

        # 获取最终输出
        final_output = result.final_output

        # 尝试解析 category
        actual_category = None
        if isinstance(final_output, TemplateSelection):
            actual_category = final_output.category
        elif isinstance(final_output, dict):
            actual_category = final_output.get("category")
        elif isinstance(final_output, str):
            # 解析 TemplateSelection 的字符串表示
            # 格式: category='list' sub_category='...' ...
            import re
            match = re.search(r"category='([^']+)'", final_output)
            if match:
                actual_category = match.group(1)

        # 检查 handoff 路径（通过查看 result 的 agent 名称）
        last_agent = result.last_agent.name if result.last_agent else "Unknown"

        is_correct = actual_category == case["expected_category"]
        status = "✅ PASS" if is_correct else "❌ FAIL"

        print(f"Handoff 到: {last_agent}")
        print(f"实际 Category: {actual_category}")
        print(f"结果: {status}")

        return {
            "name": case["name"],
            "expected": case["expected_category"],
            "actual": actual_category,
            "handoff_to": last_agent,
            "passed": is_correct,
        }

    except Exception as e:
        print(f"错误: {e}")
        return {
            "name": case["name"],
            "expected": case["expected_category"],
            "actual": None,
            "handoff_to": None,
            "passed": False,
            "error": str(e),
        }


async def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("Handoff 准确性测试")
    print("=" * 60)

    results = []
    for case in TEST_CASES:
        result = await test_single_handoff(case)
        results.append(result)

    # 汇总结果
    print("\n" + "=" * 60)
    print("测试汇总")
    print("=" * 60)

    passed = sum(1 for r in results if r["passed"])
    total = len(results)

    for r in results:
        status = "✅" if r["passed"] else "❌"
        print(f"{status} {r['name']}: 预期={r['expected']}, 实际={r['actual']}")

    print(f"\n通过率: {passed}/{total} ({passed/total*100:.0f}%)")


if __name__ == "__main__":
    asyncio.run(main())
