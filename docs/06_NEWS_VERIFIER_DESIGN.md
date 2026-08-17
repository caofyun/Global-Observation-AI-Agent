# NewsVerifier V2.0 设计文档

版本：

V1.0


更新时间：

2026-08-17


项目：

Global-Observation-AI-Agent


---

# 1. 模块定位


NewsVerifier 是新闻智能体系统中的：

AI事实核验与风险分析模块。


核心目标：

将搜索得到的新闻信息，通过 AI 分析：

- 提取事实主张
- 比较不同来源
- 发现信息冲突
- 判断可信程度
- 标记不确定内容
- 给出人工审核建议


注意：

NewsVerifier 不负责决定新闻真假。


它负责：

"证据整理 + 风险提示 + 人工辅助判断"



---

# 2. 在系统中的位置


整体流程：

用户输入新闻关键词

    ↓

SearchTool

    ↓

NewsAgent

    ↓

search_results.json

    ↓

NewsVerifier V2.0

    ↓

AIModelClient

    ↓

Gemini模型

    ↓

ai_verification.json

    ↓

人工审核

    ↓

ScriptAgent





---


# 3. 输入数据设计




输入：


search_results.json




示例：




```json
{
    "keyword": "美国航母中东部署",


    "results": [


        {
            "title":
            "xxx新闻标题",


            "source":
            "xxx媒体",


            "url":
            "xxx",


            "content":
            "新闻正文",


            "publish_time":
            "2026-08-17"
        }


    ]
}
4. AI分析任务设计
4.1 事实主张提取

目标：

从新闻文本中提取：

可验证事实。

例如：

原文：

"美国海军某航母已经进入某地区。"

AI提取：

{
    "claim":
    "美国海军某航母进入某地区",


    "category":
    "军事部署"
}
4.2 来源比较

比较：

不同新闻来源之间：

是否描述相同事件
是否存在时间差异
是否存在事实冲突

例如：

来源A：

"航母已经抵达"

来源B：

"航母正在前往"

输出：

{
    "conflict": true,


    "reason":
    "事件状态描述不同"
}
4.3 可信度分析

AI输出：

等级：

HIGH

MEDIUM

LOW

说明：

HIGH:

多个可靠来源一致

MEDIUM:

部分来源支持，但缺少官方确认

LOW:

单一来源或未经证实信息

4.4 风险检测

检测：

标题风险

例如：

标题：

"战争即将爆发"

AI判断：

{
    "risk":
    "HIGH",


    "reason":
    "标题超过已确认事实"
}
内容风险

检测：

过度推测
情绪化表达
未确认消息
预测性结论
5. 输出数据设计

输出文件：

ai_verification.json

结构：

{


"topic":


"美国航母中东部署",




"overall_confidence":


"MEDIUM",






"claims":[




{


"claim":


"美国航母进入相关区域",




"supporting_sources":


[


"来源A",


"来源B"


],




"conflicting_sources":


[],




"confidence":


"HIGH"




}




],






"risk_analysis":{




"title_risk":


"LOW",




"content_risk":


"MEDIUM",




"warnings":


[


"缺少官方确认"


]


},






"human_review_required":


true




}
6. AI调用设计

调用：

AIModelClient

结构：

NewsVerifier


        ↓


AIModelClient


        ↓


Gemini 3.1 Flash-Lite


        ↓


返回分析结果


7. 人工审核节点设计

AI完成后：

不能自动发布。

流程：

AI分析


 ↓


生成报告


 ↓


人工检查


 ↓


确认


 ↓


进入脚本生成



人工重点检查：

事实是否准确

来源是否可靠

是否存在夸大

标题是否超过事实

是否需要删除内容

8. 与其他Agent关系
NewsAgent

负责：

发现新闻

输出：

search_results.json

NewsVerifier

负责：

验证新闻

输出：

ai_verification.json

ScriptAgent

负责：

根据确认后的事实生成视频脚本。

9. 后续升级方向
V2.1

增加：

自动新闻评分
热点价值判断
V2.2

增加：

多模型交叉验证

例如：

Gemini

GPT

V3.0

增加：

实时新闻监控。

10. 当前开发原则

AI只辅助判断。

不自动决定新闻真假。

最终发布必须人工确认。

所有分析过程保存JSON。

模块保持独立，方便未来扩展。