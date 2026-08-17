# Global-Observation-AI-Agent

# PROJECT_CONTEXT.md

版本：

V1.0


更新时间：

2026-08-17


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

选题判断

↓

视频脚本生成

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



---

# 2. 项目最终目标


打造：

AI + 人工协作

的半自动视频生产系统。


原则：

AI负责：

- 信息处理
- 内容生成
- 自动化执行


人工负责：

- 最终判断
- 内容审核
- 发布确认



---

# 3. 当前应用方向


主要服务：

“环球观察速递”


内容方向：

全球新闻

国际热点

军事资讯

科技趋势

能源安全



内容原则：

- 客观
- 中立
- 不站队
- 不制造恐慌
- 不进行未经证实预测



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



---

# 5. 总体系统架构



```
用户

↓

AI内容生产总控Agent


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

# 6. 当前项目目录结构



```
Global-Observation-AI-Agent


├── agents

├── src

│   ├── agents

│   ├── config

│   └── utils


├── tests


├── docs


├── projects


├── .env


├── .gitignore


└── requirements.txt

```



---

# 7. 开发阶段状态


# Phase 0 项目设计阶段


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

# Phase 1 基础Agent框架


状态：

进行中



## 已完成



## ProjectManager


状态：

完成


功能：

项目目录管理



测试：

通过



---

## BaseAgent


状态：

完成


功能：

所有Agent基础类



测试：

通过



---

## SearchTool V1.0


状态：

完成


功能：

新闻搜索基础能力



测试：

通过



---

## NewsAgent V2.0


状态：

完成


功能：

新闻搜索结果整理



输出：

search_results.json



测试：

通过



---

## NewsVerifier V1.0


状态：

完成


文件：

```
src/agents/news_verifier.py
```



当前能力：

- 新闻来源分析
- 来源数量统计
- 标题去重
- 基础验证报告



输出：

verification.json



测试：

通过



---

## AIModelClient V2.0


状态：

完成


功能：

统一AI模型调用接口



当前支持：

Gemini



测试：

成功



测试结果：

```
status:

SUCCESS


provider:

gemini


model:

gemini-3.1-flash-lite


content:

Gemini API连接成功
```



---

# 8. 当前正在开发


阶段：

Phase 1


当前任务：

NewsVerifier V2.0升级



目标：


在V1.0基础上增加：

- AI事实分析
- 事实主张提取
- 来源冲突检测
- 可信度评分
- 风险提示



新增输出：

```
ai_verification.json
```



---

# 9. 重要设计原则


## 代码修改原则


必须：

1.

先设计


2.

再编码


3.

测试


4.

更新文档


5.

Git提交



---

## 修改代码规则


修改代码时：

不要提供局部修改。


必须提供：

完整文件。


修改位置：

增加注释说明。



---

## AI使用原则


AI不能：

自动决定新闻真假。


AI只能：

辅助分析。


最终：

人工审核。



---

# 10. Git管理规则


每完成一个功能：

执行：


```
git add

git commit

git push

```



Commit信息清晰描述：

例如：

```
Add NewsVerifier V2.0 design
```



---

# 11. 文档管理规则


docs目录是项目长期记忆。


重要变化必须更新：


```
PROJECT_CONTEXT.md


00_PROJECT_STATUS.md

```



---

# 12. 当前关键文件


## 项目状态

```
docs/00_PROJECT_STATUS.md
```



## 项目长期上下文

```
docs/PROJECT_CONTEXT.md
```



## NewsVerifier设计

```
docs/06_NEWS_VERIFIER_DESIGN.md
```



## AI数据结构

```
docs/07_AI_VERIFICATION_DATA_STRUCTURE.md
```



## NewsVerifier升级计划

```
docs/08_NEWS_VERIFIER_V2_UPGRADE_PLAN.md
```



---

# 13. 当前下一步任务


继续：

NewsVerifier V2.0升级。



顺序：

1.

升级：

```
src/agents/news_verifier.py
```


2.

更新测试：

```
tests/test_news_verifier.py
```


3.

运行测试


4.

生成：

```
ai_verification.json
```


5.

更新项目状态


6.

Git提交



---

# 14. 项目当前状态总结


项目：

🟢 正常开发


GitHub：

🟢 已连接


Gemini API：

🟢 正常


跨电脑开发：

🟢 已验证


文档体系：

🟢 已建立


当前阶段：

Phase 1


当前任务：

NewsVerifier V2.0


```