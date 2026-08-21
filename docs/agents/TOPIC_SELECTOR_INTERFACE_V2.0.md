# 环球观察速递

# TopicSelector V2.0 接口规范

版本：TopicSelector V2.0

状态：设计冻结

---

# 1. 总体说明

## 1.1 Agent 定位

TopicSelector 是「环球观察速递 AI 新闻生产系统」中的：

**新闻选题决策 Agent**

负责从多个已经完成：

- 新闻搜索
- 事实核验
- 来源评级
- 热点评分

的候选新闻主题中，选择最值得进入视频生产流程的最终选题。


TopicSelector 位于：

**内容生产前的最终决策层**

负责：

> 多候选新闻主题排序、比较和制作决策。


---

## 1.2 非职责范围

TopicSelector 不负责：

- 新闻搜索
- 新闻抓取
- 新闻事实验证
- 来源可信度判断
- 热点评分计算
- 脚本生成
- 分镜设计
- 素材采集
- 视频制作


以上功能由其他 Agent 完成。


TopicSelector 只负责：

> 从已经评分完成的候选主题中，选择最值得制作的内容。

---

# 2. 系统位置


完整新闻生产链路：

NewsAgent

↓

NewsVerifier

↓

SourceRanker

↓

TopicScorer

↓

TopicSelector

↓

ScriptAgent

↓

StoryboardAgent

↓

MaterialAgent

↓

VideoAgent

↓

ReviewAgent

↓

PublishAgent



TopicSelector 位于：



选题分析层
|
↓
内容生产层入口



是进入脚本生产之前的最后一个决策节点。

---

# 3. Agent 名称


名称：

TopicSelector

中文名称：

新闻选题决策 Agent


版本：

TopicSelector V2.0





---


# 4. Agent职责


TopicSelector 的核心职责：


## 4.1 多主题比较


TopicSelector 读取多个候选新闻项目中的：



这些文件由：

生成。


---

## 4.2 新闻主题排序


根据：

- topic_score.score
- recommendation
- breakdown

对候选新闻进行排序。


输出：

TOP N 新闻选题排行榜



---

## 4.3 制作决策


判断：

哪些主题：

进入制作

哪些主题：

继续观察

哪些主题：

放弃制作


---

## 4.4 输出最终制作主题


为：
ScriptAgent


提供唯一明确制作主题。


ScriptAgent 不再自行判断：

“做什么新闻”。

只执行：

“如何制作这个新闻”。

---

# 5. 输入接口


TopicSelector 不直接读取新闻网页。


只读取：

上游 Agent 输出文件。


---

# 5.1 必需输入


多个候选项目中的：

04_热点评分/topic_score.json



目录示例：
projects/

├── 20260821_美国航母部署/

│ └──04_热点评分/

│ └──topic_score.json

├── 20260821_霍尔木兹风险/

│ └──04_热点评分/

│ └──topic_score.json

└── 20260821_俄乌动态/
└──04_热点评分/

    └──topic_score.json



---

# 6. 输入数据结构


TopicSelector 读取：

topic_score.json


标准结构：



标准结构：

```json
{
    "topic": "美国航母部署动态",

    "score": 85,

    "recommendation": "制作",

    "breakdown": {

        "international_influence": 85,

        "news_hotness": 90,

        "user_interest": 75,

        "video_potential": 80,

        "source_quality": 70

    },

    "weights": {

        "international_influence": 0.25,

        "news_hotness": 0.30,

        "user_interest": 0.20,

        "video_potential": 0.15,

        "source_quality": 0.10

    },

    "meta": {

        "unique_source_count": 20,

        "top_sources": [

            "BBC",

            "新华社"

        ]

    }
}
```
# 7. 输出接口

TopicSelector 输出：

05_选题决策/topic_selection.json

目录：

project_path/


└──05_选题决策/


    └──topic_selection.json
# 8. 输出数据结构

标准结构：

{


    "selected_topic": "美国航母部署动态",




    "decision": "进入制作",




    "selection_score": 88,




    "ranking": [


        {


            "rank": 1,


            "topic": "美国航母部署动态",


            "score": 88,


            "recommendation": "制作"


        },




        {


            "rank": 2,


            "topic": "霍尔木兹海峡风险",


            "score": 82,


            "recommendation": "制作"


        }


    ],




    "reason": [


        "国际影响力较高",


        "新闻热度持续",


        "来源可靠",


        "具有视频表达价值"


    ],




    "meta": {


        "candidate_count": 10,


        "generated_at": "2026-08-21T12:00:00Z",


        "version": "TopicSelector v2.0"


    }


}
# 9. 选题评分规则

TopicSelector 不重新计算新闻评分。

使用：

TopicScorer.score

作为基础。

## 9.1 基础排序

默认：

selection_score = topic_score.score
## 9.2 综合调整因素

允许参考：

因素	来源
热点评分	topic_score.score
国际影响力	breakdown.international_influence
视频潜力	breakdown.video_potential
来源质量	breakdown.source_quality
推荐状态	recommendation
# 10. 推荐规则
## 10.1 进入制作

条件：

score >= 80


AND


recommendation = 制作

输出：

进入制作
## 10.2 观察候选

条件：

60 <= score < 80

输出：

人工观察
## 10.3 淘汰

条件：

score < 60

输出：

不制作
# 11. 多选题策略

TopicSelector 支持两种模式。

## 11.1 单选模式

用于：

每日新闻生产。

输出：

Top 1 新闻主题

进入：

ScriptAgent。

## 11.2 多选模式

用于：

专题内容生产。

例如：

全球军事热点 TOP 3

输出：

selected_topics[]
# 12. 与 ScriptAgent 数据接口

ScriptAgent 不再自行判断：

制作什么新闻

只读取：

topic_selection.json

获取：

核心字段：

selected_topic


selection_score


reason


top_sources

用于：

确定脚本主题
引用权威来源
判断内容方向
# 13. 错误处理
## 13.1 无候选主题

如果没有：

topic_score.json

返回：

No candidate topics

并停止执行。

## 13.2 部分项目失败

允许：

跳过异常项目。

继续处理：

其他有效候选。

# 14. 与已有 Agent 兼容要求

TopicSelector 必须：

继承：

BaseAgent

遵循：

run(input_data)


execute(input_data)

接口。

不得修改：

BaseAgent


NewsAgent


NewsVerifier


SourceRanker


TopicScorer

已有接口。

# 15. 文件版本管理

设计阶段：

docs/agents/TOPIC_SELECTOR_INTERFACE_V2.0.md

实现阶段：

src/agents/topic_selector.py

测试：

tests/test_topic_selector.py

稳定版本：

topic-selector-v2.0-stable
# 16. 后续扩展

未来支持：

## 16.1 用户反馈学习

增加：

video_performance.json

记录：

播放量
完播率
点赞
评论
收藏

用于优化选题模型。

## 16.2 AI辅助选题判断

增加：

AI Topic Judge

辅助判断：

是否具有爆款潜力
是否适合短视频表达
是否具有长期价值
# 17. 冻结声明

本文件属于：

环球观察速递 AI Agent 工厂 V2.0

架构设计规范。

冻结要求：

不修改 BaseAgent
不修改 NewsAgent
不修改 NewsVerifier
不修改 SourceRanker
不修改 TopicScorer
不破坏已有数据接口

TopicSelector V2.0 仅消费上游产物，并向下游提供稳定选题接口。
