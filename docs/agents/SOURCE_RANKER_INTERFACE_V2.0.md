# SourceRanker V2.0 Interface Freeze

## 1. Agent基础信息

Agent名称：

SourceRanker

版本：

V2.0

职责：

新闻来源评级 Agent

状态：

INTERFACE FROZEN

说明：

定义 SourceRanker 与上下游 Agent 的稳定接口。

==================================================

## 2. Agent职责边界冻结

SourceRanker负责：

1. 接收 NewsVerifier 输出的 verification.json

2. 分析新闻来源信息

3. 根据来源质量进行评级

4. 输出标准化 source_rank.json

明确禁止：

SourceRanker 不负责：

1. 新闻搜索

（属于 NewsAgent）

2. 新闻正文采集

（属于 NewsAgent）

3. 新闻真实性判断

（属于 NewsVerifier）

4. 热点评分

（属于 TopicScorer）

5. 选题决策

（属于 TopicSelector）

6. 脚本生成

（属于 ScriptAgent）

==================================================

## 3. 输入接口冻结

SourceRanker V2.0 输入来源：

verification.json

来源：

NewsVerifier V2.0

输入结构：

{
    "topic":"",
    "articles":[],
    "sources":[],
    "facts":[],
    "conflicts":[],
    "uncertainties":[],
    "verification_status":"",
    "confidence":""
}

说明：

SourceRanker 只消费：

sources

articles中的来源信息

禁止读取：

search_results.json

禁止依赖：

verification_path

禁止增加：

xxx_path

==================================================

## 4. 系统上下文冻结

统一context：

{
    "project_path":"projects/xxx"
}

用途：

- 读取 verification.json
- 保存 source_rank.json

禁止：

verification_path

search_path

article_path

其他路径参数扩散

==================================================

## 5. 输出接口冻结

必须生成：

source_rank.json

路径：

{project_path}/03_来源评级/source_rank.json

结构：

{
    "topic":"",
    "sources":[]
}

sources数组元素必须包含：

source_id

source_name

source_type

credibility_score

verification_score

source_rank

reason

字段说明：

source_id:

来源唯一编号

source_name:

新闻来源名称

source_type:

来源类型

credibility_score:

来源可信度评分

verification_score:

与事实核验结果相关评分

source_rank:

综合评级

reason:

评级原因

==================================================

## 6. 评分模型边界冻结

SourceRanker只负责：

来源质量评分

评分依据：

- 来源历史可信度
- 来源类型
- 多来源交叉情况
- NewsVerifier提供的核验结果

禁止：

生成：

topic_score

hot_score

viral_score

这些属于其他Agent。

==================================================

## 7. BaseAgent返回协议

execute():

只负责业务逻辑。

最终返回：

由 BaseAgent.run()

统一包装。

标准：

{
    "agent_name":"SourceRanker",
    "status":"success",
    "result":{},
    "error":null
}

不要在 SourceRanker 内部重复定义。

==================================================

## 8. 数据流关系冻结

数据流：

NewsVerifier

↓

verification.json

↓

SourceRanker

↓

source_rank.json

说明：

SourceRanker 不生成：

verification.json

topic_score.json

script.md

==================================================

## 9. 版本冻结记录

Version:

V2.0

冻结内容：

- 输入统一 verification.json
- 删除 verification_path依赖
- 输出统一 source_rank.json
- 对齐 BaseAgent V2.0协议
- 明确来源评级职责

状态：

FROZEN

==================================================
