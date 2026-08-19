# 环球观察速递 AI Agent 工厂

# 系统数据结构设计 V2.0


版本：

V2.0


更新时间：

2026-08-19


---

# 一、设计目标


为了实现多个 AI Agent 之间稳定协同工作，系统建立统一的数据标准。


所有 Agent 遵循：


输入标准数据

↓

执行任务

↓

输出标准数据


保证：


- Agent之间可以通信
- 数据格式统一
- 项目过程可追踪
- 支持人工审核
- 支持未来系统升级


---

# 二、数据设计原则


## 1. 数据驱动


Agent之间不直接依赖。


通过标准文件进行数据交换。


例如：


NewsAgent

↓

search_results.json


NewsVerifier

↓

verification.json


SourceRanker

↓

source_rank.json



---

## 2. 单一数据责任


每个Agent：

只负责创建和维护自己的数据。


例如：


NewsAgent：

负责新闻搜索结果。


NewsVerifier：

负责真实性验证。



---

## 3. 数据可追溯


所有生产过程保存：


- 输入数据
- 输出数据
- Agent状态
- 人工确认记录



---

## 4. 支持人工控制


关键节点：

AI生成

↓

人工确认

↓

进入下一阶段



---

# 三、核心数据流程


完整生产流程：

用户需求

↓

project.json

↓

search_results.json

↓

verification.json

↓

source_rank.json

↓

topic_score.json

↓

script.md

↓

storyboard.json

↓

materials.json

↓

production.json

↓

review.json

↓

publish.json


---

# 四、核心数据文件说明



# 1. project.json


## 作用


管理整个视频项目。


## 创建者


ProductionController


## 使用者


所有Agent



## 示例


```json
{
    "project_id": "20260816_US_Carrier",
    "title": "美国航母进入中东",
    "platform": [
        "抖音",
        "B站"
    ],
    "duration": "90s",
    "status": "NEWS_RESEARCH",
    "created_time": "",
    "agents_status": {
        "news_agent": "completed",
        "news_verifier": "completed",
        "source_ranker": "running"
    }
}
2. search_results.json
作用

保存新闻搜索结果。

创建者

NewsAgent

输入

新闻主题。

输出内容

包括：

新闻标题
新闻链接
新闻来源
发布时间
新闻摘要
示例
{
    "topic": "美国航母进入中东",
    "results": [
        {
            "title": "",
            "source": "",
            "url": "",
            "summary": ""
        }
    ]
}
3. verification.json
作用

保存新闻真实性验证结果。

创建者

NewsVerifier

输入

search_results.json

输出内容

包括：

信息一致性
来源交叉验证
可信度评分
风险提示
示例
{
    "verification_status": "verified",
    "confidence": 85,
    "risk_notes": []
}

4. source_rank.json
作用

新闻来源评级。

创建者

SourceRanker

输入

verification.json

输出内容

包括：

来源等级
权威评分
可靠性分析
示例
{
    "sources": [
        {
            "name": "",
            "rank": "A",
            "score": 90
        }
    ]
}
5. topic_score.json
作用

判断新闻是否适合制作视频。

创建者

TopicScorer

评分维度

包括：

国际影响力
新闻热度
用户关注度
视频传播潜力
输出
{
    "score": 85,
    "recommendation": "制作"
}
6. script.md
作用

保存视频脚本。

创建者

ScriptAgent

输入

topic_score.json

内容包括：
标题
开场钩子
旁白
节奏设计
结尾引导

示例结构：
# 视频标题


## 开场


## 正文


## 结尾
7. storyboard.json
作用

保存视频分镜信息。

创建者

StoryboardAgent

输入

script.md

示例
{
    "scenes":[
        {
            "id":1,
            "time":"00:00-00:05",
            "voice":"",
            "visual":"",
            "material_keywords":[
                "aircraft carrier"
            ]
        }
    ]
}
8. materials.json
作用

保存视频素材信息。

创建者

MaterialAgent

输入

storyboard.json

保存：
图片
视频
地图
音频
来源
授权信息
示例
{
    "materials":[
        {
            "id":"001",
            "type":"video",
            "filename":"",
            "path":"",
            "source":"",
            "license":"",
            "used_scene":1
        }
    ]
}
9. production.json
作用

保存视频制作方案。

创建者

VideoAgent

内容：
时间线
素材对应关系
转场
特效
BGM

示例：
{
    "timeline":[
        {
            "start":"00:00",
            "end":"00:05",
            "material":"001",
            "effect":"",
            "subtitle":""
        }
    ]
}
10. review.json
作用

视频审核结果。

创建者

ReviewAgent

检查：
事实准确性
标题风险
平台规则
表达问题

示例：
{
    "fact_check":"pass",
    "title_check":"pass",
    "platform_risk":"low",
    "suggestions":[]
}
11. publish.json
作用

发布信息管理。

创建者

PublishAgent

内容：
标题
简介
标签
评论引导
发布状态

示例：
{
    "title":"",
    "description":"",
    "hashtags":[],
    "status":"WAIT_USER_CONFIRM"
}
五、项目目录数据标准

每个视频项目：
projects/

└──20260816_美国航母进入中东

    ├──project.json

    ├──01_新闻资料

    │
    │──search_results.json
    │──verification.json
    │──source_rank.json


    ├──02_脚本

    │
    │──script.md


    ├──03_分镜

    │
    │──storyboard.json


    ├──04_素材

    │
    │──materials.json
    │──images/
    │──videos/


    ├──05_制作

    │
    │──production.json


    ├──06_审核

    │
    │──review.json


    └──07_发布

        └──publish.json

六、Agent与数据关系
| Agent                | 输入                  | 输出                  |
| -------------------- | ------------------- | ------------------- |
| ProductionController | 用户需求                | project.json        |
| NewsAgent            | 新闻主题                | search_results.json |
| NewsVerifier         | search_results.json | verification.json   |
| SourceRanker         | verification.json   | source_rank.json    |
| TopicScorer          | source_rank.json    | topic_score.json    |
| ScriptAgent          | topic_score.json    | script.md           |
| StoryboardAgent      | script.md           | storyboard.json     |
| MaterialAgent        | storyboard.json     | materials.json      |
| VideoAgent           | materials.json      | production.json     |
| ReviewAgent          | production.json     | review.json         |
| PublishAgent         | review.json         | publish.json        |

七、未来扩展

未来支持：

用户反馈数据

保存：

播放量
点赞
收藏
评论

用于优化选题。
素材评分数据

保存：

使用次数
点击效果
视频表现
AI优化数据

用于：

Agent能力提升
自动优化生产流程
个性化内容生成

八、版本升级路线

V1.0：

完成基础数据设计。

V2.0：

建立Agent标准数据接口。

V3.0：

支持数据库、云存储、自动化工作流。