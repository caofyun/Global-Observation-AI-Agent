# AI Verification 数据结构设计

版本：

V1.0


更新时间：

2026-08-17


项目：

Global-Observation-AI-Agent


---

# 1. 文档目的


定义 NewsVerifier V2.0 的标准数据格式。


目标：

让新闻核验结果能够被后续 Agent 使用。


数据流：

SearchTool

↓

NewsAgent

↓

search_results.json

↓

NewsVerifier V2.0

↓

ai_verification.json

↓

ScriptAgent





---


# 2. ai_verification.json 定位




文件：



ai_verification.json





作用：


保存 AI 对新闻事件的：


- 事实分析
- 来源比较
- 冲突检测
- 可信度判断
- 风险提示




注意：


该文件不是最终新闻结论。


它是：


AI辅助审核报告。






---


# 3. 顶层数据结构




```json
{
    "topic": "",
    "analysis_time": "",
    "overall_confidence": "",
    "claims": [],
    "source_analysis": {},
    "risk_analysis": {},
    "human_review_required": true
}
4. 字段说明
topic

类型：

string

说明：

新闻主题。

示例：

美国航母中东部署
analysis_time

类型：

string

说明：

AI分析时间。

格式：

YYYY-MM-DD
overall_confidence

类型：

string

说明：

整体可信度。

可选：

HIGH


MEDIUM


LOW
5. claims 事实主张结构

claims保存新闻中的可验证事实。

示例：

[
    {
        "claim":
        "美国航母进入中东相关区域",


        "category":
        "军事部署",


        "confidence":
        "MEDIUM",


        "supporting_sources":
        [],


        "conflicting_sources":
        []
    }
]

字段：

claim

事实内容。

category

事实分类。

例如：

军事


外交


经济


科技
confidence

该事实可信度。

supporting_sources

支持该事实的来源。

conflicting_sources

存在不同描述的来源。

6. source_analysis

来源分析。

结构：

{
    "total_sources": 5,


    "reliable_sources": 3,


    "source_consistency":
    "MEDIUM"
}

字段：

total_sources：

来源数量。

reliable_sources：

较可靠来源数量。

source_consistency：

来源一致程度。

7. risk_analysis

风险分析。

结构：

{
    "title_risk":
    "LOW",


    "content_risk":
    "MEDIUM",


    "warnings":
    [
        "缺少官方确认"
    ]
}

字段：

title_risk：

标题风险。

content_risk：

内容风险。

warnings：

提醒事项。

8. human_review_required

类型：

boolean

说明：

是否需要人工审核。

默认：

true

原因：

新闻内容不能完全自动发布。

9. 完整示例
{
    "topic":
    "美国航母中东部署",


    "analysis_time":
    "2026-08-17",


    "overall_confidence":
    "MEDIUM",




    "claims":
    [


        {
            "claim":
            "美国航母进入相关区域",


            "category":
            "军事部署",


            "confidence":
            "MEDIUM",


            "supporting_sources":
            [
                "来源A",
                "来源B"
            ],


            "conflicting_sources":
            []
        }


    ],




    "source_analysis":
    {
        "total_sources":5,


        "reliable_sources":3,


        "source_consistency":
        "MEDIUM"
    },




    "risk_analysis":
    {


        "title_risk":
        "LOW",


        "content_risk":
        "MEDIUM",


        "warnings":
        [
            "等待官方进一步确认"
        ]


    },




    "human_review_required":
    true
}
10. 后续扩展

未来增加：

情绪分析
sentiment_analysis
热点评分
hot_score
视频价值判断
video_priority
多模型验证
model_consensus
当前状态

设计：完成

