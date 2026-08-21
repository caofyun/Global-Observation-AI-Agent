# 环球观察速递

# TOPIC PIPELINE TEST PLAN V2.0

版本：
Topic Pipeline V2.0

状态：
测试设计规范


---

# 1. 测试目标


## 1.1 核心目标


验证环球观察速递 AI Agent 系统是否具备：

> 自动发现新闻热点，并筛选出最值得制作的视频选题的能力。


最终实现：

互联网实时新闻

↓

热点发现

↓

事实核验

↓

来源评级

↓

热点价值评估

↓

多主题比较

↓

输出每日推荐选题



---

# 2. 测试范围


本测试覆盖：

## 新闻选题智能层


包含：


NewsAgent

↓

NewsVerifier

↓

SourceRanker

↓

TopicScorer

↓

TopicSelector



不包含：


ScriptAgent

StoryboardAgent

MaterialAgent

VideoAgent

PublishAgent



原因：

选题正确是内容生产成功的前提。

如果选题错误，后续脚本、素材、视频制作都会产生浪费。



---

# 3. 测试目标定义


系统最终需要回答：


每天：

全球有哪些重要新闻？


哪些新闻：

- 国际影响最大？
- 当前热度最高？
- 来源最可靠？
- 最适合短视频表达？
- 综合价值最高、最值得制作？


最终输出：


今日推荐制作选题 TOP N



---

# 4. 输入测试


## 4.1 新闻搜索输入


支持用户输入：


关键词：

例如：

美国航母

中东局势

霍尔木兹海峡

俄罗斯乌克兰

中国周边安全

全球军事动态

或者：
daily_global_news


系统通过互联网实时获取最新新闻信息，并根据发布时间、搜索结果相关性及新闻热度进行候选发现。



---

# 5. 新闻来源要求


NewsAgent 应支持：


- 新闻搜索接口
- RSS
- 新闻API
- 搜索引擎结果


获取：
标题

URL

来源

发布时间

摘要

正文（可选）


---
# 6. 测试流程

完整流程：

互联网实时新闻
↓
NewsAgent
↓
新闻候选发现
↓
事件归并 / 候选主题形成
↓
NewsVerifier
↓
SourceRanker
↓
TopicScorer
↓
TopicSelector
↓
TOP N 推荐选题

---

## Step 1 新闻发现

输入：

keyword

或者：

daily_global_news

NewsAgent 通过互联网实时搜索获取相关新闻。

输出：

01_新闻资料/
news_articles.json

至少记录：

- title
- url
- source
- published_time
- summary

正文是否获取由实际搜索能力和新闻来源决定，本阶段不作为强制要求。

---

## Step 1.1 候选主题形成

对搜索得到的新闻文章进行：

- 相同事件识别
- 重复新闻归并
- 相关报道聚合
- 候选主题提取

目标：

将大量新闻文章整理为若干具有独立新闻价值的候选主题。

例如：

美国航母进入某海域
美国航母部署位置变化
美国海军发布相关声明

如果属于同一新闻事件，应尽可能归并为：

“美国航母部署动态”

而不是形成三个重复选题。

说明：

如果当前 NewsAgent 尚未具备完整的事件归并能力，本阶段允许通过测试辅助逻辑或临时方式完成，但不得修改已经冻结的上游 Agent 接口。

后续应根据真实测试结果决定是否增加独立的：

TopicDiscovery / EventCluster

模块。

---

## Step 2 事实核验

Agent：

NewsVerifier

输入：

news_articles.json

输出：

02_事实核验/
verification.json

验证：

- 是否存在多来源报道
- 是否存在事实冲突
- 是否存在明显不可靠信息
- 新闻时间是否合理
- 核验置信度

---

## Step 3 来源评级

Agent：

SourceRanker

输入：

verification.json

输出：

03_来源评级/
source_rank.json

验证：

- 来源质量
- 权威等级
- 可信评分
- 来源之间的质量差异

---

## Step 4 热点评分

Agent：

TopicScorer

输入：

source_rank.json

verification.json

输出：

04_热点评分/
topic_score.json

验证：

- international_influence
- news_hotness
- user_interest
- video_potential
- source_quality
- score
- recommendation

---

## Step 5 选题决策

Agent：

TopicSelector

输入：

多个候选项目中的：

04_热点评分/
topic_score.json

输出：

05_选题决策/
topic_selection.json

最终输出：

- TOP 1 推荐选题
- TOP 3 候选选题
- 完整排行榜
- 每个选题的评分
- 推荐状态
- 主要来源
- 选择理由

---

## Step 6 人工复核

人工查看：

05_选题决策/topic_selection.json

判断：

- TOP1 是否值得制作
- TOP3 是否具有制作价值
- 是否存在重复选题
- 是否存在明显低价值选题
- 是否存在事实风险
- AI排序是否符合实际新闻价值

人工评价结果记录到测试记录中。

---

## 测试原则

本阶段重点不是立即修改 Agent 算法。

首先验证：

“真实互联网新闻”

能否稳定经过：

新闻发现
↓
候选主题形成
↓
事实核验
↓
来源评级
↓
热点评分
↓
多主题排序
↓
最终选题

形成完整、可重复运行的：

Topic Pipeline V2.0

如果测试发现某个环节能力不足：

先记录问题，

再决定是否修改对应 Agent。

不得为了让测试通过而人为调整测试结果。
# 7. 测试案例设计




## 测试案例1：军事热点




输入：



美国航母部署





预期：


系统能够发现：


- 航母动态
- 海军部署
- 地缘影响




输出：


推荐制作






---


## 测试案例2：能源风险




输入：



霍尔木兹海峡





预期：


识别：


- 国际能源影响
- 地缘风险
- 视频表达价值




---


## 测试案例3：竞争热点




同时输入：





美国航母

俄乌局势

中东能源

亚洲安全





验证：


系统是否能够：


排序


比较


选择最高价值主题。






---

# 8. 输出标准

最终输出：

05_选题决策/topic_selection.json

TopicSelector 的输出必须能够直接供人工查看，并能够被后续 ScriptAgent 读取。

标准结构：

```json
{
    "selected_topic": "美国航母部署动态",

    "decision": "进入制作",

    "selection_score": 88,

    "ranking": [
        {
            "rank": 1,
            "topic": "美国航母部署动态",
            "score": 88,
            "recommendation": "制作",
            "top_sources": [
                "BBC",
                "Reuters",
                "新华社"
            ]
        },
        {
            "rank": 2,
            "topic": "霍尔木兹海峡风险",
            "score": 84,
            "recommendation": "制作",
            "top_sources": [
                "Reuters",
                "BBC"
            ]
        }
    ],

    "reason": [
        "国际影响力较高",
        "新闻热度持续",
        "来源可靠",
        "具有视频表达价值"
    ],

    "generated_at": "2026-08-21T12:00:00Z",

    "version": "TopicSelector v2.0"
}
```
## 8.1 输出要求

至少必须包含：

selected_topic
decision
selection_score
ranking
reason
generated_at
version

其中 ranking 中每个候选主题至少包含：

rank
topic
score
recommendation
top_sources
## 8.2 TOP N

默认输出：

TOP 1：

最终推荐制作选题。

TOP 3：

最值得关注的候选选题。

完整 ranking：

保留所有通过测试的候选主题及其排序结果。

这样既方便人工选择，也方便后续系统继续处理。

# 9. 人工评价标准

AI输出后，由人工评价。

评价问题：

## 9.1 选题价值

是否值得制作？

评分：

5 很值得


4 值得


3 一般


2 不建议


1 错误
## 9.2 排名准确性

AI第一名：

是否符合人工判断？

记录：
AI选择

人工选择

差异原因
# 10. 测试成功标准

第一阶段测试目标不是立即证明选题模型已经达到最终准确率，而是验证整个实时新闻选题链路能够稳定运行。

满足以下条件：

## 条件1：实时新闻获取

系统能够通过互联网获取最新新闻信息，并记录：

- 新闻标题
- 新闻URL
- 新闻来源
- 发布时间
- 新闻摘要或正文
## 条件1.1：新闻时效性

系统获取的新闻必须记录明确的：

- published_time

并能够根据发布时间判断新闻的新旧程度。

测试时应重点检查：

- 是否能够获取当天或近期新闻
- 是否混入大量过时新闻
- 搜索结果是否按照新闻相关性与时效性进行合理筛选
- 同一事件的旧报道是否会被误认为最新新闻
- 新闻发布时间异常或缺失时是否能够正常处理

对于实时热点测试：

优先使用最近24小时内发生或持续发展的新闻作为候选。

对于持续发展的重大事件：

允许使用超过24小时的报道作为背景信息，但不得仅因为旧报道数量较多而错误提高新闻热度评分。

测试记录中应保留：

- 搜索时间
- 新闻发布时间
- 新闻来源
- 新闻标题

用于后续判断系统是否真正具备实时热点发现能力。

## 条件2：候选主题生成

系统能够将搜索结果整理为多个候选新闻主题，并对同一新闻事件进行合理归并，避免同一事件形成大量重复选题。

## 条件3：新闻分析链路完整

能够依次完成：

新闻搜索

↓

事实核验

↓

来源评级

↓

热点价值评分

↓

多主题排序

↓

选题决策

## 条件4：最终选题输出

系统能够输出：

- TOP 1 推荐选题
- TOP 3 候选选题
- 每个选题的评分
- 推荐状态
- 主要来源
- 选择理由

## 条件5：人工评价

连续测试不少于20个新闻主题。

记录：

- AI TOP1
- 人工认为的TOP1
- AI TOP3
- 人工认为的TOP3
- 差异原因

第一阶段不设置固定准确率门槛。

完成20个以上真实新闻主题测试后，根据人工评价结果建立初始基准。

后续版本再根据测试数据设定：

- TOP1人工认可率目标
- TOP3覆盖率目标
- 重复选题率
- 错误新闻率
- 低价值选题率

## 条件6：稳定性

连续运行多次后：

- Agent之间的数据接口保持一致
- 中间文件能够正常生成
- 单个新闻失败不会导致整个选题流程崩溃
- 最终能够稳定生成topic_selection.json

# 11. 后续优化方向
## 11.1 增加热点数据

未来加入：

search_trend.json


social_signal.json



增强：

user_interest

## 11.2 增加历史反馈

记录：

video_performance.json

包含：

播放量

完播率

点赞

评论

用于优化评分模型。


---


# 12. 当前开发阶段

## 12.1 已完成的 Agent

当前已经完成：

✅ NewsAgent

✅ NewsVerifier V2.0

✅ SourceRanker V2.0

✅ TopicScorer V2.0

✅ TopicSelector V2.0

这些 Agent 已完成基础实现及接口设计。

---

## 12.2 当前未完成内容

目前尚未完成：

❌ Topic Pipeline V2.0 真实互联网端到端验证

❌ 大量新闻事件的自动归并验证

❌ 多候选主题的真实排序验证

❌ TOP1 / TOP3 人工评价基准

❌ 连续运行稳定性验证

因此：

当前不能认为 Topic Pipeline 已经达到生产级稳定状态。

---

## 12.3 当前任务

当前阶段暂停 ScriptAgent 等后续生产 Agent 的开发。

优先完成：

Topic Pipeline V2.0

真实新闻测试。

测试目标：

互联网实时新闻
↓
新闻发现
↓
候选主题形成
↓
事实核验
↓
来源评级
↓
热点评分
↓
多主题排序
↓
TOP1 / TOP3 推荐

只有当上述链路能够稳定运行后，

才进入：

ScriptAgent V2.0

的设计与实现。
# 13. 下一阶段

通过 Topic Pipeline 验证后：

进入：

ScriptAgent V2.0

实现：

选题

↓

脚本

↓

分镜

↓

素材

↓

视频生产