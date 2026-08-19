# NewsVerifier V2.0 升级方案

版本：

V1.0


更新时间：

2026-08-17


项目：

Global-Observation-AI-Agent



---

# 1. 文档目的


本文档用于规划：

NewsVerifier 从 V1.0 升级到 V2.0 的开发方案。


升级目标：

在保持已有功能稳定的基础上，

增加：

- AI事实分析
- 新闻主张提取
- 来源冲突检测
- 可信度评估
- 风险提示


最终形成：

AI辅助新闻审核模块。



---

# 2. 当前 NewsVerifier V1.0 状态


当前文件：

```
src/agents/news_verifier.py
```


当前能力：


## 2.1 新闻输入读取


读取：

```
search_results.json
```


来源：

NewsAgent



---

## 2.2 新闻来源分析


当前支持：

- 来源识别
- URL解析
- 来源数量统计



---

## 2.3 新闻标题处理


当前支持：

- 标题标准化
- 重复标题过滤



---

## 2.4 基础核验报告


输出：

```
verification.json
```


包含：

- facts
- claims
- conflicts
- uncertainties



---

# 3. V2.0升级目标


NewsVerifier V2.0定位：


AI事实核验辅助Agent。



增加能力：


## 3.1 AI事实分析


通过：

```
AIModelClient

↓

Gemini模型
```


分析新闻内容。


输出：

- 事实主张
- 关键事件
- 已确认信息
- 未确认信息



---

## 3.2 新闻可信度分析


增加：

```
confidence
```


等级：


HIGH

MEDIUM

LOW



说明：


HIGH：

多个可靠来源一致。


MEDIUM：

部分来源支持，但缺少确认。


LOW：

单一来源或存在明显疑点。



---

## 3.3 信息冲突检测


检测：


不同来源之间：

- 时间差异
- 事件描述差异
- 数据差异


输出：

```
conflicts
```



---

## 3.4 内容风险分析


检测：


- 标题夸大
- 情绪化表达
- 未确认消息
- 推测性结论


输出：

```
risk_analysis
```



---

# 4. 升级后系统流程


升级前：


```
SearchTool

↓

NewsAgent

↓

search_results.json

↓

NewsVerifier V1.0

↓

verification.json

```



升级后：


```
SearchTool

↓

NewsAgent

↓

search_results.json

↓

NewsVerifier V2.0

        |

        |

        ↓

 AIModelClient

        |

        ↓

 Gemini


        |

        ↓


ai_verification.json


        |

        ↓


人工审核


```



---

# 5. 保持不变的接口


为了保证系统稳定：

以下接口不修改。



## 5.1 Agent继承关系


保持：

```python
class NewsVerifier(BaseAgent)
```



---

## 5.2 调用方式


保持：

```python
verifier = NewsVerifier()


result = verifier.run(
{
    "project_path":
    project_path
}
)
```



---

## 5.3 输入文件


保持：

```
search_results.json
```



---

# 6. 新增功能设计



## 6.1 AI分析模块


新增函数：


```python
analyze_with_ai()
```


作用：


将新闻内容发送给：

```
AIModelClient
```


返回：

AI分析结果。



---

## 6.2 AI核验报告生成


新增：


```
ai_verification.json
```


内容包括：


```json
{
    "topic":"",
    "confidence":"",
    "claims":[],
    "conflicts":[],
    "warnings":[],
    "human_review_required":true
}
```



---

# 7. 文件变化规划



## 保留文件


```
src/agents/news_verifier.py
```


升级。



---

## 新增输出


```
ai_verification.json
```



---

## 保留旧输出


```
verification.json
```


原因：

保证旧流程兼容。



---

# 8. 代码修改范围



主要修改：


```
src/agents/news_verifier.py
```



增加：


## AI模型调用


```python
AIModelClient()
```



## AI分析方法


```python
analyze_with_ai()
```



## AI报告保存


```python
save_ai_verification()
```



---

# 9. 测试方案



测试文件：


```
tests/test_news_verifier.py
```



保持原测试方式：


输入：

```
project_path
```


执行：

```
verifier.run()
```



验证：


## 原功能


检查：

```
verification.json
```


是否生成。



---

## 新功能


检查：

```
ai_verification.json
```


是否生成。



---

# 10. 开发原则



## 原则1

不破坏已有功能。



## 原则2

AI只辅助判断。

不自动决定新闻真假。



## 原则3

最终发布必须人工确认。



## 原则4

所有AI分析结果保存JSON。



## 原则5

每次升级：

必须：

设计

↓

编码

↓

测试

↓

Git提交



---

# 11. 后续升级方向


## NewsVerifier V2.1


增加：

- 新闻热度评分
- 视频价值评分



---

## NewsVerifier V2.2


增加：

多模型交叉验证。


例如：

Gemini

+

GPT



---

## NewsVerifier V3.0


增加：

实时新闻监控。


---

# 当前状态


设计阶段：

完成


下一步：

升级：

```
src/agents/news_verifier.py

NewsVerifier V1.0

↓

NewsVerifier V2.0
```

