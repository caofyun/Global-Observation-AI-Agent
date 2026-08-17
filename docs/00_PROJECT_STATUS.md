# Global-Observation-AI-Agent

## 项目状态文档 V1.0

更新时间：
2026-08-17

---

# 1. 项目简介

## 项目名称

Global-Observation-AI-Agent


## 项目目标

打造一个 AI 驱动的短视频内容生产智能体系统。

目标：

从新闻选题开始：

新闻发现
→ 新闻筛选
→ 新闻事实核验
→ 视频脚本生成
→ 分镜设计
→ 素材搜索
→ 素材下载
→ 素材分类整理
→ 配音生成
→ 字幕生成
→ 视频剪辑
→ 人工审核
→ 发布


最终形成：

AI辅助 + 人工确认

的半自动/自动化视频生产流水线。


---

# 2. 核心设计原则


## 原则1：AI辅助，不替代人工

所有重要内容：

新闻事实
标题
脚本
最终视频

必须经过人工确认。


## 原则2：模块化 Agent 架构

每个功能独立：

NewsAgent

NewsVerifier

ScriptAgent

MaterialAgent

VoiceAgent

SubtitleAgent

VideoAgent


通过统一接口协作。


## 原则3：AI模型可替换

不绑定单一模型。

当前：

Gemini

未来支持：

OpenAI

Claude

其他模型。


---

# 3. 当前技术架构

Global-Observation-AI-Agent

├── agents
│
├── src
│ ├── config
│ │
│ └── utils
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
└── requirements.txt



---




## NewsAgent V2.0




状态：


完成




功能：


调用 SearchTool


生成：


search_results.json




测试：


通过




---




## NewsVerifier V1.0




状态：


完成




功能：


基础新闻验证流程。




生成：


verification.json




测试：


通过




---


# 5. AI能力接入




## AI配置模块




状态：


完成




文件：



src/config/ai_config.py





功能：


读取：


.env




管理：


AI_PROVIDER


AI_MODEL


AI_API_KEY






---


# AIModelClient V2.0




状态：


完成




功能：


统一AI调用接口。




当前支持：


Gemini




模型：


gemini-3.1-flash-lite




调用流程：





AIModelClient

↓

google-genai SDK

↓

Gemini API

↓

返回AI结果







测试：


成功




测试结果：



status: SUCCESS

provider:
gemini

model:
gemini-3.1-flash-lite

content:
Gemini API连接成功





---


# 6. 安全配置




## .env保护




状态：


完成




规则：


API Key只保存在：


.env




禁止上传GitHub。




---


## .gitignore




已配置：





.env

pycache/

*.pyc





状态：


正常




---


# 7. GitHub工程管理




状态：


完成




已实现：


- Git仓库初始化


- GitHub连接


- Commit


- Push


- 第二台电脑恢复测试






---


# 8. 跨电脑开发测试




状态：


成功




流程：





GitHub

↓

新电脑clone项目

↓

安装Python依赖

↓

配置.env

↓

运行测试

↓

恢复AI能力





一键生成视频项目。




---


# 12. 当前重要决策




1.


AI模型采用可切换架构。




2.


当前使用：


Gemini 3.1 Flash-Lite




3.


所有自动发布功能：


必须人工确认。




4.


代码修改：


采用完整文件替换方式。




5.


每个阶段完成后：


更新本文件。




---


# 当前状态总结




项目状态：


🟢 正常




AI连接：


🟢 成功




GitHub：


🟢 正常




跨电脑开发：


🟢 成功




下一任务：


NewsVerifier V2.0