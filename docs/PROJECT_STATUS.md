# 环球观察速递 AI Agent 工厂

# PROJECT_STATUS.md V2.0

版本：
V2.0

更新时间：
2026-08-19

项目状态：
架构升级阶段


---

# 一、项目定位

## 项目名称

环球观察速递 AI Agent 工厂


## 项目目标

打造一个 AI 驱动的全球新闻视频生产系统。

输入：

全球热点新闻


自动完成：

1. 新闻发现
2. 新闻真实性验证
3. 新闻来源评级
4. 热点评分
5. 选题判断
6. 视频脚本生成
7. 素材管理
8. 视频生产辅助


最终输出：

- 新闻分析报告
- 视频口播稿
- 分镜方案
- 素材清单
- 字幕方案
- 视频生产项目


---

# 二、当前系统版本


当前版本：

V2.0 架构升级版


开发阶段：

基础能力建设完成


下一阶段：

AI Agent 工厂化开发


---

# 三、已完成模块


## 1. BaseAgent

状态：

✅ 已完成


位置：
src/agents/base_agent.py


功能：

- Agent基础类
- 统一Agent接口
- 生命周期管理
- 日志管理基础


作用：

所有AI Agent的父类。


---

## 2. NewsAgent

状态：

✅ 已完成


位置：
src/agents/news_agent.py


功能：

新闻搜索与采集。


输入：

新闻关键词


输出：
search_results.json


当前能力：

- 搜索新闻
- 保存搜索结果
- 基础新闻数据结构


---

## 3. NewsVerifier

状态：

✅ 已完成


位置：
src/agents/news_verifier.py



功能：

新闻真实性验证。


输入：
search_results.json


输出：


当前能力：

- 检查新闻完整性
- 分析新闻来源
- AI辅助真实性判断


---

## 4. AIModelClient

状态：

✅ 已完成


位置：
src/utils/ai_model_client.py


功能：

统一AI模型调用接口。


支持：

- Gemini API
- 后续扩展其他模型


作用：

所有Agent通过统一接口调用AI。


---

# 四、当前系统流程


目前：
用户输入新闻主题

    ↓

NewsAgent

    ↓

search_results.json

    ↓

NewsVerifier

    ↓

verification.json


已经形成：

新闻采集 → 新闻验证

基础链路。


---

# 五、正在开发模块


## SourceRanker Agent

状态：

🚧 设计阶段


目标：

新闻来源评级。


输入：

verification.json


输出：

source_rank.json


评价：

- 来源权威性
- 信息透明度
- 历史可靠性
- 新闻原创性



---

## TopicScorer Agent

状态：

未开始


目标：

判断新闻是否值得制作视频。


评分：

- 国际影响力
- 新闻热度
- 用户关注度
- 视频传播潜力


---

# 六、未来Agent规划


## 新闻智能链

NewsAgent

↓

NewsVerifier

↓

SourceRanker

↓

TopicScorer

↓

TopicSelector



## 内容生产链

ScriptAgent

↓

MaterialAgent

↓

SubtitleAgent

↓

VideoAgent


---

# 七、开发原则


## 原则1

先设计，后编码。


流程：
需求

↓

设计文档

↓

代码实现

↓

自动测试

↓

Git提交



---

## 原则2

禁止破坏已有接口。


修改已有模块必须：

说明：

- 修改原因
- 影响范围
- 测试结果



---

## 原则3

所有模块必须拥有：

设计文档：
docs/


代码：
src/


测试：


---

# 八、AI工具分工


## ChatGPT

负责：

- 系统架构
- 产品规划
- 技术路线
- 代码审查


---

## Cursor / AI Coding Agent

负责：

- 编写代码
- 修改代码
- 自动测试
- 重构


---

## GitHub

负责：

- 版本管理
- 历史记录
- 项目备份



---

# 九、当前开发任务


## 第1阶段：系统工程化


任务：

1. 建立docs设计体系

2. 完善项目目录

3. 建立测试体系

4. 固化Agent接口



---

# 十、下一步任务


当前任务：

创建：
docs/01_SYSTEM_ARCHITECTURE.md


内容：

定义：

- 整体架构
- Agent关系
- 数据流
- 技术路线



---

# 项目负责人

Human:

环球观察速递创始人


AI:

AI Architecture Assistant

AI Coding Agents
