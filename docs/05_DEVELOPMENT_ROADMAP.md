# 环球观察速递 AI Agent 工厂


# 开发路线图 V2.0


版本：

V2.0


更新时间：

2026-08-19



---

# 一、开发目标



建立一个：

AI Agent + 人工审核


的智能内容生产系统。



最终实现：


从新闻发现开始，


经过：


- 新闻搜索
- 事实核验
- 来源评级
- 热点评估
- 脚本生成
- 分镜设计
- 素材管理
- 视频制作
- 配音字幕
- 内容审核
- 发布准备


完成完整的AI辅助视频生产流程。



最终目标：


一个创作者

+

一组AI Agent团队


完成专业资讯短视频生产。



---


# 二、整体开发阶段



项目分为：



## Phase 0

系统规划与架构设计阶段



## Phase 1

AI Agent基础框架阶段



## Phase 2

新闻智能分析系统阶段



## Phase 3

内容生产Agent阶段



## Phase 4

素材自动化系统阶段



## Phase 5

视频制作辅助系统阶段



## Phase 6

完整AI视频生产系统阶段



---



# 三、Phase 0

# 系统规划与架构设计阶段



## 目标


确定：

- 系统方向
- Agent架构
- 数据标准
- 工作流程
- 技术路线



## 已完成内容



### 系统设计文档


✅ 项目愿景


✅ 系统总体架构


✅ Agent功能设计


✅ 系统数据结构设计


✅ AI生产工作流设计


✅ 技术路线选择



输出：


完整系统设计文档。



状态：


✅ 完成



---



# 四、Phase 1

# AI Agent基础框架阶段



## 目标



建立：

Agent运行基础。


实现：

- Agent统一接口
- 项目管理
- 任务调度
- 数据流转
- 测试体系



---


# 已完成模块



## BaseAgent


状态：

✅ 完成


作用：


所有Agent基础父类。



代码：
src/agents/base_agent.py



---


## ProductionController


状态：

✅ 基础完成


作用：


AI生产总控。


负责：

- 创建项目
- 调度Agent
- 管理流程状态



代码：
src/core/production_controller.py




---


## AIModelClient


状态：

✅ 完成


作用：


统一AI模型调用接口。



代码：
src/utils/ai_model_client.py




---


## SearchTool


状态：

✅ 完成


作用：


新闻搜索工具。



代码：
src/utils/search_tool.py



---


## NewsAgent


状态：

✅ V2.0基础完成



功能：

- 新闻搜索
- 信息整理
- 来源记录



代码：
src/agents/news_agent.py



---


## NewsVerifier


状态：

✅ 完成



功能：

- 新闻真实性检查
- 多来源验证
- 信息完整性检查



代码：
src/agents/news_verifier.py



---


## SourceRanker


状态：

🚧 开发中



功能：

- 新闻来源评级
- 可信度分析



代码：
src/agents/source_ranker.py




---



# Phase 1 当前任务



完成：

- Agent标准接口统一
- SourceRanker完善
- Agent测试完善
- 状态管理完善



输出：

稳定的AI Agent基础框架。



---



# 五、Phase 2

# 新闻智能分析系统阶段



## 目标



建立：

新闻发现 → 新闻判断 → 选题决策


智能系统。



---


## NewsAgent



负责：


- 搜索热点新闻
- 收集新闻来源
- 整理新闻资料



输出：
search_results.json




---


## NewsVerifier



负责：


- 事实核验
- 信息一致性检查
- 风险识别



输出：
verification.json




---


## SourceRanker



负责：


- 来源权威性分析
- 来源可靠性评分
- 来源质量排序



输出：
source_rank.json




---


## TopicScorer



规划开发。


负责：


- 新闻价值评分
- 传播潜力分析
- 制作优先级判断



输出：
topic_score.json



---


# Phase 2完成目标



实现：


新闻自动研究系统。



流程：


新闻输入

↓

搜索

↓

验证

↓

评级

↓

评分

↓

人工确认



---



# 六、Phase 3

# 内容生产Agent阶段



## 目标



实现：

新闻资料 → 视频方案



---


# ScriptAgent



功能：


生成：

- 标题
- 开场钩子
- 旁白
- 视频结构



输出：
script.md



---


# StoryboardAgent



功能：


生成：


- 时间轴
- 镜头设计
- 画面需求
- 素材关键词



输出：
storyboard.json



---


# Phase 3完成目标



实现：

从新闻主题到视频策划方案。



---



# 七、Phase 4

# 素材自动化系统阶段



## 目标



建立：

AI素材管理体系。



---


# MaterialAgent



功能：


## 本地素材库


实现：

- 分类
- 标签
- 搜索
- 去重



## 网络素材管理


实现：

- 关键词扩展
- 素材搜索
- 下载管理



## 素材审核


检查：

- 清晰度
- 相关性
- 重复性



输出：
materials.json



---



# Phase 4完成目标



形成：

可复用的视频素材资产库。



---



# 八、Phase 5

# 视频制作辅助系统阶段



## 目标



辅助完成：

视频成片制作。



---


# VideoAgent



功能：


生成：

- 剪辑方案
- 时间线
- 转场
- 特效
- BGM方案



输出：
production.json



---


# AudioSubtitleAgent



功能：


实现：

- AI配音
- 自动字幕
- 字幕优化



输出：
voice.wav

subtitle.srt



---



# 九、Phase 6

# 完整AI视频生产系统阶段



## 目标



实现：

半自动甚至高度自动化的视频生产流水线。



完整流程：

新闻发现

↓

AI分析

↓

事实核验

↓

脚本生成

↓

人工确认

↓

分镜生成

↓

素材准备

↓

视频制作

↓

声音字幕

↓

审核

↓

人工确认

↓

发布



---



# 十、软件开发原则



## 1. 小步迭代



不追求一次完成。



采用：


开发

↓

测试

↓

记录

↓

升级



---



## 2. 模块独立



每个Agent：

独立开发。


方便：

- 替换
- 升级
- 扩展



---



## 3. 数据资产沉淀



所有生产数据保存：


- 新闻资料
- 验证记录
- 来源评分
- 脚本
- 分镜
- 素材
- 视频方案
- 审核记录



形成长期AI内容资产。



---



## 4. 测试优先



每个模块完成后：


必须：

- 单元测试
- 集成测试
- 更新状态文档
- Git提交



---



# 十一、当前开发阶段



当前阶段：


## Phase 1

AI Agent基础框架阶段



已经完成：


✅ 项目结构建立


✅ BaseAgent


✅ ProductionController


✅ AIModelClient


✅ SearchTool


✅ NewsAgent


✅ NewsVerifier



正在进行：


🚧 SourceRanker完善



下一阶段：


进入：

Phase 2

新闻智能分析系统开发。



---



# 十二、未来30天开发路线



## 第1阶段

完成Agent基础框架


目标：

稳定运行：

- NewsAgent
- NewsVerifier
- SourceRanker



---


## 第2阶段

完成新闻决策链


增加：

- TopicScorer



形成：

新闻发现系统。



---


## 第3阶段

开发：

- ScriptAgent
- StoryboardAgent



形成：

内容策划系统。



---


## 第4阶段

开发：

- MaterialAgent



建立：

素材自动化体系。



---


## 第5阶段

开发：

- VideoAgent
- AudioSubtitleAgent



形成：

完整AI生产闭环。



---


# END
