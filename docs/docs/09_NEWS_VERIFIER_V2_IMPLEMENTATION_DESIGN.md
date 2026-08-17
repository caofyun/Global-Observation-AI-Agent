此文档作为NewsVerifier V2.0 开发前的技术冻结文档
作用：

明确V2.0改什么
明确V2.0不改什么
防止代码开发过程中反复修改架构
为后续测试和升级提供依据

# Global-Observation-AI-Agent


# 09_NEWS_VERIFIER_V2_IMPLEMENTATION_DESIGN.md


版本：

V1.0


更新时间：

2026-08-17



---

# 1. 文档目的


本文档用于定义：

NewsVerifier V2.0

的具体实现方案。



目标：

在保持 NewsVerifier V1.0 基础能力不变的情况下，

增加：

AI辅助事实分析能力。



---

# 2. 当前V1.0状态


当前文件：

```
src/agents/news_verifier.py
```



当前版本：

```
NewsVerifier V1.0
```



已有功能：


## 2.1 新闻数据读取


读取：

```
01_新闻资料/search_results.json
```



---

## 2.2 基础完整性检查


检查：

- 标题是否存在
- URL是否存在
- 来源是否可识别



---

## 2.3 新闻来源识别


支持：

- search_results中的source字段
- URL域名解析



---

## 2.4 标题去重


通过：

标题标准化


去除：

- 空格
- 标点
- 中英文符号



---

## 2.5 来源统计


统计：

不同新闻来源数量。



---

## 2.6 输出


生成：

```
verification.json
```



---

# 3. V2.0升级目标


NewsVerifier V2.0增加：

AI辅助事实核验能力。



注意：

AI不是最终事实裁判。


AI作用：

辅助分析。


最终：

人工审核。



---

# 4. V2.0新增能力


## 4.1 AI语义分析


输入：

基础核验结果。


调用：

```
AIModelClient
```



当前模型：

```
Gemini-3.1-flash-lite
```



输出：

AI分析结果。



---

## 4.2 新闻事实主张提取


AI分析：

新闻中包含的主要事实声明。



例如：


输入：

```
某国宣布新的军事部署
```


提取：

```
claim:

某国进行了军事部署
```



---

## 4.3 多来源一致性分析


分析：

多个来源是否描述：

- 相同事件
- 不同细节
- 相互矛盾



---

## 4.4 不确定信息识别


识别：

- 未确认消息
- 推测内容
- 来源不足
- 各方不同表述



---

## 4.5 可信度评分


生成：

```
HIGH

MEDIUM

LOW
```



说明：

不是事实真假判断。


表示：

当前资料支持程度。



---

# 5. V2.0数据流程


## V1.0流程


```
search_results.json

        ↓

基础检查

        ↓

来源统计

        ↓

verification.json
```



---

## V2.0流程


```
search_results.json

        ↓

基础检查

        ↓

来源统计

        ↓

生成基础verification

        ↓

AIModelClient

        ↓

Gemini分析

        ↓

生成AI核验结果

        ↓

ai_verification.json
```



---

# 6. V2.0代码设计


文件：

```
src/agents/news_verifier.py
```



---

# 6.1 保留结构


保持：

```python
class NewsVerifier(BaseAgent)
```



保持：

```python
execute()
```



保持输入方式：


```python
{
    "project_path": project_path
}
```



---

# 6.2 新增AI客户端


新增：


```python
AIModelClient
```



作用：

调用统一AI接口。



---

# 6.3 新增方法


增加：


```python
analyze_with_ai()
```



作用：


将基础核验结果发送给AI。



---

# 6.4 新增方法


增加：

```python
save_ai_verification()
```



作用：

保存：

```
ai_verification.json
```



---

# 7. 数据结构设计



## verification.json


继续保持：

```json
{
    "topic":"",
    "status":"",
    "results":[],
    "facts":[],
    "claims":[],
    "conflicts":[],
    "uncertainties":[]
}
```



---

# ai_verification.json


新增：

```json
{
    "topic":"",

    "ai_model":
    "gemini-3.1-flash-lite",

    "confidence":
    "MEDIUM",

    "claims":[],

    "supporting_evidence":[],

    "conflicts":[],

    "uncertainties":[],

    "risk_notes":[],

    "ai_summary":"",

    "human_review_required":true
}
```



---

# 8. AI提示词设计原则


发送给AI的信息：

包括：

- 新闻标题
- 来源
- 发布时间
- URL
- 多来源摘要



要求AI：

1.

提取事实声明


2.

分析来源一致性


3.

指出冲突


4.

标记不确定信息


5.

给出可信度等级



禁止：

- 自动判定真假
- 政治立场判断
- 战争预测



---

# 9. 测试方案


测试文件：

```
tests/test_news_verifier.py
```



---

## V2.0测试目标


验证：

## 1.

能够读取：

```
search_results.json
```



## 2.

能够调用：

```
AIModelClient
```



## 3.

能够生成：

```
verification.json
```



## 4.

能够生成：

```
ai_verification.json
```



## 5.

异常情况处理：


包括：

- API失败
- 文件不存在
- JSON错误
- AI返回异常



---

# 10. 兼容性要求


V2.0必须兼容：


V1.0输入：

```
search_results.json
```



V1.0输出：

```
verification.json
```



不能破坏：

- NewsAgent
- ProjectManager
- BaseAgent



---

# 11. 开发步骤


## Step 1

修改：

```
src/agents/news_verifier.py
```



增加：

AI能力。



---

## Step 2

更新：

```
tests/test_news_verifier.py
```



---

## Step 3

运行测试。


---

## Step 4

生成：

```
ai_verification.json
```



---

## Step 5

更新：

```
PROJECT_CONTEXT.md

00_PROJECT_STATUS.md

CHANGELOG.md
```



---

## Step 6

Git提交：

```
git add .

git commit

git push
```



---

# 12. 当前状态


文档状态：

完成设计。


下一步：

进入：

NewsVerifier V2.0代码实现。



---

# END