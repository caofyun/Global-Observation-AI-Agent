# NewsVerifier V2.0 Interface Freeze

## 1. Agent基础信息

Agent名称：
NewsVerifier

版本：
V2.0

职责：
新闻事实核验 Agent

状态：
INTERFACE FROZEN

说明：
该文档定义 NewsVerifier 与其他系统组件之间的稳定接口。

---

## 2. Agent职责边界冻结

NewsVerifier负责：

1. 接收 NewsAgent 输出的新闻正文数据

2. 对新闻正文中的事实声明进行核验

3. 分析来源可信度

4. 对不同来源信息进行交叉比对

5. 标记：

- 已验证事实
- 存在冲突的信息
- 未确定的信息

6. 输出标准化 verification.json

明确禁止：

NewsVerifier 不负责：

1. 新闻搜索

（属于 NewsAgent）

2. 新闻发现

（属于 NewsAgent）

3. 热点评分

（属于 TopicScorer）

4. 选题决策

（属于 TopicSelector）

5. 脚本生成

（属于 ScriptAgent）

6. 视频生产

（属于 VideoAgent）

---

## 3. 输入接口冻结

定义唯一业务输入。

要求：

NewsVerifier V2.0 输入来源：

news_articles.json

结构：

{
    "articles":[]
}

每篇文章来自：

NewsAgent V2.0

包含：

article_id

title

source

url

published_time

content

summary

禁止：

直接读取：

search_results.json

禁止：

依赖：

search_results_path

禁止：

扩展：

xxx_path

---

## 4. 系统上下文冻结

说明：

NewsVerifier运行时可以接收统一context。

示例：

{
    "project_path":"projects/xxx"
}

用途：

- 读取新闻资料
- 保存核验结果

禁止：

在业务输入中增加：

verification_path

article_path

search_path

等路径字段。

---

## 5. 输出接口冻结

NewsVerifier V2.0必须生成：

verification.json

路径：

根据统一project_path管理。

例如：

{project_path}/02_事实核验/verification.json

结构必须包含：

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

字段说明：

topic:

研究主题


articles:

参与核验的新闻文章列表


sources:

新闻来源信息


facts:

已经确认的事实


conflicts:

不同来源之间存在的矛盾


uncertainties:

无法确认的信息


verification_status:

整体核验状态


confidence:

核验置信度

---

## 6. AI辅助分析输出说明

说明：

AI辅助分析可以独立存在。

例如：

ai_verification.json

但：

不能替代：

verification.json

不能改变：

NewsVerifier V2.0主输出协议。

---

## 6.1 V2.1 扩展预留说明（非V2.0冻结字段）

说明：

为未来任务级统一追踪，可能增加字段：

{
    "verification_id":""
}

用途：

- 唯一标识一次事实核验任务
- 形成：
  - verification_id -> 多个 article_id

示例关系：

verification任务
  |
  └── 多篇 article

注意：

该字段仅作为未来扩展预留，不属于当前 V2.0 冻结接口。

当前 V2.0 必须保持接口完整稳定，不应提前加入。

建议后续发布至：

NewsVerifier V2.1

---

## 7. BaseAgent返回协议说明

说明：

NewsVerifier.execute()

只负责业务逻辑。

最终外部返回：

由 BaseAgent.run()

统一包装。

标准格式：

{
    "agent_name":"NewsVerifier",
    "status":"success",
    "result":{},
    "error":null
}

不要在 NewsVerifier 内部重复设计返回协议。

---

## 8. 数据流关系冻结

数据流：

NewsAgent

↓

news_articles.json

↓

NewsVerifier

↓

verification.json

↓

SourceRanker

说明：

NewsVerifier 不生成：

search_results.json

source_rank.json

topic_score.json

---

## 9. 版本冻结记录

Version:

V2.0

冻结内容：

- 输入统一为 news_articles.json
- 删除 search_results.json 依赖
- 输出统一 verification.json
- 对齐 BaseAgent V2.0协议
- 明确事实核验职责边界

状态：

FROZEN
