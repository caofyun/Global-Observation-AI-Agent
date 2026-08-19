# Global-Observation-AI-Agent

# PROJECT_CONTEXT.md

版本：

V1.1

更新时间：

2026-08-18

项目状态：

Active Development

---

# 1. 项目简介

## 项目名称

Global-Observation-AI-Agent

## 项目定位

开发一个：

AI驱动的短视频内容生产智能体系统。

目标：

帮助创作者完成：

新闻发现

↓

新闻分析

↓

新闻核验

↓

选题判断

↓

视频脚本生成

↓

分镜设计

↓

素材搜索

↓

素材整理

↓

自动剪辑

↓

配音

↓

字幕

↓

视频生成

↓

人工审核

↓

发布

最终形成：

AI辅助 + 人工确认

的半自动视频生产系统。

---

# 2. 项目最终目标

打造：

AI + 人工协作

的智能内容生产平台。

原则：

AI负责：

* 信息处理
* 数据分析
* 内容生成
* 自动化执行

人工负责：

* 最终判断
* 内容审核
* 发布确认

---

# 3. 当前应用方向

主要服务：

“环球观察速递”

内容方向：

* 全球新闻
* 国际热点
* 军事资讯
* 科技趋势
* 能源安全

内容原则：

* 客观
* 中立
* 不站队
* 不制造恐慌
* 不进行未经证实预测

---

# 4. 技术架构

## 开发语言

Python 3.13

## 开发环境

VS Code

## 版本管理

GitHub

## AI模型

当前：

Gemini

模型：

gemini-3.1-flash-lite

## AI调用方式

Google GenAI SDK

设计原则：

AI模型可替换。

未来支持：

* OpenAI
* Claude
* 其他模型

---

# 5. 系统总体架构

```
用户

↓

ProductionController

↓

AI内容生产总控层


↓

--------------------------------

新闻生产链：

SearchTool

↓

NewsAgent

↓

NewsVerifier

↓

ScriptAgent

↓

StoryboardAgent


--------------------------------


素材生产链：

MaterialAgent

↓

素材搜索

↓

素材下载

↓

素材分类

↓

素材匹配


--------------------------------


视频生产链：

VoiceAgent

↓

SubtitleAgent

↓

VideoAgent


--------------------------------


人工审核

↓

发布

```

---

# 6. 核心系统分层

当前系统采用：

模块化 Agent 架构。

整体分为四层：

## Layer 1：控制层

位置：

```
src/core
```

主要组件：

```
ProjectManager

ProductionController
```

职责：

* 项目管理
* Agent调度
* 工作流程控制
* 生产任务协调

---

## Layer 2：Agent层

位置：

```
src/agents
```

当前Agent：

| Agent        | 状态    |
| ------------ | ----- |
| BaseAgent    | 完成    |
| NewsAgent    | 完成    |
| NewsVerifier | 开发升级中 |

未来：

| Agent           | 状态 |
| --------------- | -- |
| ScriptAgent     | 计划 |
| StoryboardAgent | 计划 |
| MaterialAgent   | 计划 |
| VoiceAgent      | 计划 |
| SubtitleAgent   | 计划 |
| VideoAgent      | 计划 |

---

## Layer 3：工具层

位置：

```
src/utils
```

当前工具：

### AIModelClient

功能：

统一AI模型调用。

支持：

Gemini API

---

### SearchTool

功能：

新闻搜索能力。

---

## Layer 4：配置层

位置：

```
src/config
```

当前：

```
ai_config.py
```

负责：

* AI Provider配置
* 模型配置
* API Key管理

---

# 7. Agent Registry

当前系统Agent注册表：

| 模块                   | 版本   | 状态   | 说明       |
| -------------------- | ---- | ---- | -------- |
| BaseAgent            | V1.0 | 完成   | Agent基础类 |
| SearchTool           | V1.0 | 完成   | 搜索能力     |
| NewsAgent            | V2.0 | 完成   | 新闻整理     |
| NewsVerifier         | V1.0 | 完成   | 新闻核验     |
| AIModelClient        | V2.0 | 完成   | AI接口     |
| ProjectManager       | V1.0 | 完成   | 项目管理     |
| ProductionController | V1.0 | 基础完成 | 流程控制     |

---

# 8. 当前项目目录结构

```
Global-Observation-AI-Agent


├── src

│
├── agents

│   ├── base_agent.py

│   ├── news_agent.py

│   └── news_verifier.py


├── config

│   └── ai_config.py


├── core

│   ├── ProjectManager

│   ├── production_controller.py

│   └── __init__.py


├── utils

│   ├── ai_model_client.py

│   └── search_tool.py


├── tests

├── projects

├── docs

├── .env

├── .gitignore

└── main.py

```

---

# 9. 当前开发阶段

## Phase 0 项目设计阶段

状态：

完成

完成：

✅ 项目愿景

✅ AI智能体总体架构

✅ 开发路线图

✅ 系统数据结构设计

✅ AI生产工作流设计

✅ 技术路线选择

---

# Phase 1 Agent基础框架

状态：

进行中

已完成：

✅ BaseAgent

✅ SearchTool

✅ NewsAgent

✅ NewsVerifier V1.0

✅ AIModelClient

✅ ProjectManager

当前：

NewsVerifier V2.0升级

---

# 10. 数据流设计

核心数据流：

```
SearchTool

↓

search_results.json

↓

NewsAgent

↓

新闻结构化数据

↓

NewsVerifier

↓

verification.json

↓

AI事实分析

↓

ai_verification.json

```

数据原则：

每个Agent：

输入明确。

输出明确。

通过数据结构协作。

---

# 11. 重要开发原则

## 代码修改原则

必须：

1. 需求分析

2. 设计文档

3. 代码实现

4. 测试

5. 更新文档

6. Git提交

---

## AI使用原则

AI不能：

自动决定新闻真假。

AI只能：

辅助分析。

最终：

人工审核。

---

# 12. 文档管理规则

项目长期记忆：

```
PROJECT_CONTEXT.md
```

项目当前状态：

```
00_PROJECT_STATUS.md
```

任务管理：

```
TASKS.md
```

版本历史：

```
CHANGELOG.md
```

重要变化必须同步更新。

---

# 13. 当前下一步任务

继续：

NewsVerifier V2.0升级。

目标：

增加：

* AI事实分析
* 事实主张提取
* 来源冲突检测
* 可信度评分
* 风险提示

新增：

```
ai_verification.json
```

---

# 项目当前状态总结

项目：

🟢 Active Development

架构：

🟢 Agent系统已建立

AI：

🟢 Gemini API正常

GitHub：

🟢 正常

测试体系：

🟢 已建立

当前阶段：

Phase 1

当前任务：

NewsVerifier V2.0

版本：

PROJECT_CONTEXT V1.1
