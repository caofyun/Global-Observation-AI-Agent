# NewsAgent V2.0 Interface Freeze

## 1. Agent基础信息

Agent名称：
NewsAgent

版本：
V2.0

职责：
新闻发现与正文采集 Agent

状态：
INTERFACE FROZEN

说明：
该文档定义 NewsAgent 与其他系统组件之间的稳定接口契约。

---

## 9. 文件路径规范

NewsAgent 输出文件必须存放于：

{project_path}/01_新闻资料/

文件：

search_results.json

news_articles.json

禁止：

硬编码绝对路径

禁止：

Agent内部创建新的路径规则

---

## 2. Agent职责边界冻结

NewsAgent负责：

1. 接收用户研究主题关键词
2. 生成搜索关键词
3. 调用搜索工具获取新闻候选
4. 获取新闻正文
5. 清洗新闻正文
6. 输出标准化新闻数据

明确禁止：

NewsAgent 不负责：

1. 新闻真实性判断
   （属于 NewsVerifier）

2. 热点评分
   （属于 TopicScorer）

3. 选题决策
   （属于 TopicSelector）

4. 脚本生成
   （属于 ScriptAgent）

5. 视频生产
   （属于 VideoAgent）

---

## 3. 输入接口冻结

NewsAgent V2.0唯一业务输入：

JSON:

{
    "topic_keyword": "研究主题关键词"
}

字段说明：

topic_keyword:
- 类型：string
- 必填：是
- 说明：用户指定的新闻研究主题

约束：
topic_keyword 为唯一业务输入字段。任何其他业务字段未经接口变更流程不得加入。

明确废弃旧接口：

{
    "topic":""
}

以及：

{
    "project_path":""
}

说明：

project_path 不属于业务输入。

项目路径属于系统运行上下文，由 BaseAgent 或运行控制器统一提供。

---

## 4. 系统上下文冻结

说明：

NewsAgent运行时可以接收统一context：

示例：

{
    "project_path":"projects/xxx"
}

用途：

- 保存输出文件
- 管理项目资源

禁止：

在 input_data 中扩展：

xxx_path

verification_path

search_path

article_path

等新的路径参数。

---

## 5. 输出接口冻结

NewsAgent V2.0必须产生两个标准文件：

--------------------------------

第一：

search_results.json

用途：

保存搜索发现结果。

要求：

只保存搜索层信息。

包含：

result_id

title

url

source

published_time

snippet

禁止：

保存事实判断结果。

--------------------------------

第二：

news_articles.json

用途：

保存新闻正文数据流。

结构要求：

articles数组。

每篇文章包含：

article_id

title

source

url

published_time

content

summary

说明：

该文件作为 NewsVerifier 后续事实核验输入。

---

## 6. BaseAgent返回协议说明

说明：

NewsAgent execute()

只负责业务逻辑结果。

最终外部返回必须符合 BaseAgent V2.0统一协议：

{
    "agent_name":"NewsAgent",
    "status":"success",
    "result":{},
    "error":null
}

不要在 NewsAgent 内部重复设计返回协议。

---

## 7. 数据流关系冻结

用户输入

topic_keyword

↓

NewsAgent

↓

search_results.json

↓

news_articles.json

↓

NewsVerifier

说明：

NewsAgent 不直接生成：

verification.json

ai_verification.json

source_rank.json

---

## 8. 版本冻结记录

Version History

V2.0

冻结内容：

- 输入统一为 topic_keyword
- project_path 转为系统context
- 新增 news_articles.json 数据流
- 保留 search_results.json 搜索层输出
- 对齐 BaseAgent V2.0协议

状态：

FROZEN
