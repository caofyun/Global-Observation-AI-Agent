# Global-Observation-AI-Agent

# 项目状态文档 V1.1


更新时间：

2026-08-18


项目状态：

Active Development


---


# 1. 项目简介


## 项目名称


Global-Observation-AI-Agent


## 项目目标


打造一个 AI 驱动的短视频内容生产智能体系统。


目标：

从新闻选题开始：

新闻发现

↓

新闻筛选

↓

新闻事实核验

↓

视频脚本生成

↓

分镜设计

↓

素材搜索

↓

素材整理

↓

配音生成

↓

字幕生成

↓

视频剪辑

↓

人工审核

↓

发布



最终形成：

AI辅助 + 人工确认

的半自动视频生产流水线。



---


# 2. 核心设计原则


## 原则1：AI辅助，不替代人工


所有重要内容：

- 新闻事实
- 标题
- 脚本
- 最终视频


必须经过人工确认。



---


## 原则2：模块化 Agent 架构


每个功能独立：

- NewsAgent
- NewsVerifier
- ScriptAgent
- MaterialAgent
- VoiceAgent
- SubtitleAgent
- VideoAgent


通过统一接口协作。



---


## 原则3：AI模型可替换


不绑定单一模型。


当前：

Gemini


未来支持：

- OpenAI
- Claude
- 其他模型



---


# 3. 当前技术架构


## 开发环境


语言：

Python 3.13


开发：

VS Code


版本管理：

GitHub



---


## AI模型


当前：

Gemini


模型：

gemini-3.1-flash-lite



调用方式：

Google GenAI SDK



---


# 4. 当前代码架构状态


项目结构：
Global-Observation-AI-Agent

├── src
│
│ ├── agents
│ │
│ │ ├── base_agent.py
│ │ ├── news_agent.py
│ │ └── news_verifier.py
│ │
│ ├── config
│ │
│ │ └── ai_config.py
│ │
│ ├── core
│ │
│ │ ├── ProjectManager
│ │ ├── production_controller.py
│ │ └── init.py
│ │
│ └── utils
│ │
│ ├── ai_model_client.py
│ └── search_tool.py
│
├── tests
│
├── projects
│
├── docs
│
├── .env
│
├── .gitignore
│
├── main.py
│
└── requirements.txt




---


# 5. Agent Status


| 模块 | 版本 | 状态 | 测试 |
|---|---|---|---|
| BaseAgent | V1.0 | 完成 | PASS |
| SearchTool | V1.0 | 完成 | PASS |
| NewsAgent | V2.0 | 完成 | PASS |
| NewsVerifier | V1.0 | 完成 | PASS |
| AIModelClient | V2.0 | 完成 | PASS |
| ProjectManager | V1.0 | 完成 | PASS |
| ProductionController | V1.0 | 基础完成 | 待完善 |
| ScriptAgent | - | 计划 | - |
| StoryboardAgent | - | 计划 | - |
| MaterialAgent | - | 计划 | - |
| VideoAgent | - | 计划 | - |



---


# 6. 已完成模块


## BaseAgent


状态：

完成


功能：

所有Agent基础类。


测试：

通过。



---


## SearchTool V1.0


状态：

完成


功能：

新闻关键词搜索。


测试：

通过。



---


## NewsAgent V2.0


状态：

完成


功能：

整理新闻搜索结果。


输出：

search_results.json



测试：

通过。



---


## NewsVerifier V1.0


状态：

完成


文件：
src/agents/news_verifier.py



功能：

- 新闻来源分析
- 来源数量统计
- 标题去重
- 基础验证报告


输出：
verification.json



测试：

通过。



---


## AIModelClient V2.0


状态：

完成


功能：

统一AI模型调用接口。


支持：

Gemini


测试：

成功。



测试结果：

status:

SUCCESS

provider:

gemini

model:

gemini-3.1-flash-lite

content:

Gemini API连接成功



---


# 7. 测试状态


测试框架：

pytest



当前测试文件：
test_ai_config.py

test_ai_model_client.py

test_base_agent.py

test_news_agent.py

test_news_agent_v2.py

test_news_verifier.py

test_project_manager.py

test_search_tool.py




当前状态：

PASS



---


# 8. Current Sprint


当前阶段：

Phase 1


任务：

NewsVerifier V2.0 Upgrade



目标：


增强新闻事实核验能力。



计划增加：


- AI事实分析
- 事实主张提取
- 来源冲突检测
- 可信度评分
- 风险提示


新增输出：
ai_verification.json



任务列表：
[完成] AIModelClient接入

[完成] 基础验证流程

[进行中] AI事实分析

[待完成] 事实主张提取

[待完成] 来源冲突检测

[待完成] 可信度评分

[待完成] ai_verification.json生成

[待完成] 测试

[待完成] Git提交



---


# 9. Recent Completed


2026-08-17


完成：

✅ PROJECT_CONTEXT项目长期上下文建立

✅ CHANGELOG版本管理建立

✅ Gemini API连接测试成功



---


2026-08-16


完成：

✅ AIModelClient V2.0

✅ NewsVerifier V1.0



---


2026-08-14


完成：

✅ NewsAgent V2.0



---


2026-08-13


完成：

✅ SearchTool V1.0



---


2026-08-12


完成：

✅ BaseAgent基础框架



---


# 10. GitHub工程管理


状态：

完成


已实现：


- Git仓库初始化
- GitHub连接
- Commit
- Push
- 跨电脑Clone测试



---


# 11. 安全配置


## .env保护


API Key：

只保存在：
.env


禁止上传GitHub。



.gitignore：

已配置：
.env

pycache/

*.pyc




---


# 12. 文档管理规则


重要变化必须更新：

PROJECT_CONTEXT.md

00_PROJECT_STATUS.md

CHANGELOG.md

TASKS.md




---


# 13. 下一步任务


当前：

NewsVerifier V2.0升级



完成顺序：


1.

升级：
src/agents/news_verifier.py


2.

更新测试：
tests/test_news_verifier.py



3.

运行测试


4.

生成：
ai_verification.json



5.

更新文档


6.

Git提交



---


# 当前状态总结


项目：

🟢 正常开发


代码架构：

🟢 已建立


Agent框架：

🟢 Phase 1接近完成


AI连接：

🟢 Gemini正常


GitHub：

🟢 正常


测试体系：

🟢 已建立


当前任务：

NewsVerifier V2.0


版本：

00_PROJECT_STATUS V1.1

