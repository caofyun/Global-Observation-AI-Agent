# 环球观察速递 AI Agent 工厂

# Agent总体架构设计 V2.0


版本：

V2.0


更新时间：

2026-08-19


说明：

本文档定义环球观察速递 AI Agent 工厂总体架构。


详细接口和实现规范见：

06_AGENT_FUNCTION_DESIGN.md



---

# 一、项目目标


环球观察速递 AI Agent 工厂目标：


通过多个AI智能体协作，辅助完成完整的资讯短视频生产流程。


实现：

一个创作者

+

AI专业团队


完成：

- 新闻发现
- 新闻分析
- 事实核验
- 选题判断
- 脚本生成
- 分镜设计
- 素材整理
- 视频制作
- 配音字幕
- 内容审核
- 发布准备



---

# 二、系统总体架构


用户

↓

新闻选题 / 创作需求

↓

AI生产总控Agent
(ProductionController)

↓

↓

BaseAgent基础框架

↓

NewsAgent

新闻发现

↓

NewsVerifier

新闻真实性验证

↓

SourceRanker

新闻来源评级

↓

TopicScorer

热点价值评分

↓

ScriptAgent

脚本生成

↓

StoryboardAgent

分镜设计

↓

MaterialAgent

素材管理

↓

VideoAgent

视频制作

↓

AudioSubtitleAgent

声音字幕

↓

ReviewAgent

内容审核

↓

PublishAgent

发布准备

↓

人工最终确认

↓

发布平台




---

# 三、Agent角色设计



# 0. BaseAgent


## 定位


所有Agent的基础框架。


## 文件

src/agents/base_agent.py


## 负责


- Agent初始化
- 标准执行接口
- 状态管理
- 日志记录


## 状态


已完成。



---


# 1. AI生产总控Agent


英文名称：

ProductionController


## 定位


整个系统的大脑。


## 文件

src/core/production_controller.py


## 负责


- 接收用户任务
- 创建项目
- 调度Agent
- 管理生产流程
- 保存项目状态



## 输出

project.json



## 状态


基础完成。



---


# 2. 新闻研究Agent


英文名称：

NewsAgent


## 定位


AI新闻记者。


## 文件

src/agents/news_agent.py



## 负责


- 搜索热点新闻
- 收集新闻来源
- 信息整理
- 新闻摘要生成


## 输入


新闻主题。


## 输出

search_results.json



## 状态


✅ V2.0基础完成



---


# 3. 新闻真实性验证Agent


英文名称：

NewsVerifier


## 定位


AI事实核验员。


## 文件

src/agents/news_verifier.py



## 负责


检查：


- 新闻完整性
- 信息一致性
- 来源交叉验证
- 真实性风险



## 输入

search_results.json


## 输出

verification.json


## 状态


✅ V2.0基础完成



---


# 4. 新闻来源评级Agent


英文名称：

SourceRanker


## 定位


新闻来源分析专家。


## 文件

src/agents/source_ranker.py



## 负责


评价：


- 来源权威性
- 来源可靠性
- 信息透明度


## 输入

verification.json


## 输出

source_rank.json


## 状态


开发中。



---


# 5. 热点价值评分Agent


英文名称：

TopicScorer


## 定位


判断新闻是否值得制作。


## 负责


评分：


- 国际影响力
- 新闻热度
- 用户关注度
- 视频传播潜力



## 输出

topic_score.json


## 状态


规划。



---


# 6. 脚本编导Agent


英文名称：

ScriptAgent


## 定位


AI视频编导。


## 负责


生成：


- 视频标题
- 开场钩子
- 旁白稿
- 视频结构



## 输入

topic_score.json


## 输出

script.md


## 状态


规划。



---


# 7. 分镜导演Agent


英文名称：

StoryboardAgent


## 定位


AI导演。


## 负责


将文字转化为：


- 时间轴
- 镜头设计
- 画面需求
- 素材需求



## 输入

script.md


## 输出

storyboard.json


## 状态


规划。



---


# 8. 素材管理Agent


英文名称：

MaterialAgent


## 定位


AI资料员。


## 负责


- 搜索素材
- 下载素材
- 分类整理
- 去重
- 标签管理
- 建立素材库



## 输入

storyboard.json


## 输出

materials.json


## 状态


规划。



---


# 9. 视频制作Agent


英文名称：

VideoAgent


## 定位


AI剪辑师。


## 负责


生成：


- 剪辑方案
- 视频时间线
- 转场方案
- 特效建议
- BGM方案



## 输入

materials.json


## 输出

production.json


## 状态


规划。



---


# 10. 声音字幕Agent


英文名称：

AudioSubtitleAgent


## 定位


AI后期制作。


## 负责


- AI配音
- 字幕生成
- 字幕优化



## 状态


规划。



---


# 11. 审核优化Agent


英文名称：

ReviewAgent


## 定位


AI审核员。


## 负责


检查：


内容：

- 事实风险


标题：

- 是否夸张


平台：

- 是否违规


表达：

- 是否需要优化



## 输出

review.json


## 状态


规划。



---


# 12. 发布助手Agent


英文名称：

PublishAgent


## 定位


AI运营助手。


## 负责


生成：


- 发布标题
- 视频简介
- 标签
- 评论引导



## 输出

publish.json


## 状态


规划。



---


# 四、人工控制节点



系统不是完全自动化。


核心原则：

AI生成

↓

人工审核

↓

进入下一阶段



关键确认节点：



## 节点1

新闻选题确认



## 节点2

脚本确认



## 节点3

素材确认



## 节点4

成片确认



## 节点5

发布确认



---


# 五、设计原则



## 1. 模块化


每个Agent独立开发。


方便：

- 测试
- 升级
- 替换



---


## 2. 数据驱动


Agent之间通过标准数据通信。


例如：

search_results.json

↓

verification.json

↓

source_rank.json

↓

script.md



---


## 3. 可人工干预


避免AI错误直接进入生产流程。



---


## 4. 数据资产沉淀


所有内容保存：


- 新闻资料
- 脚本
- 分镜
- 素材
- 视频项目
- 审核记录



---


## 5. 长期迭代


支持：

V1.0

V2.0

V3.0


持续升级。



---


# 六、开发方向



## 第一阶段


建立AI内容生产基础能力。


已完成：


- BaseAgent
- NewsAgent
- NewsVerifier
- AIModelClient



---


## 第二阶段


完善新闻分析能力。


包括：


- SourceRanker
- TopicScorer



---


## 第三阶段


完成内容生产能力。


包括：


- ScriptAgent
- StoryboardAgent
- MaterialAgent



---


## 第四阶段


实现完整AI视频生产流程。


包括：


- VideoAgent
- AudioSubtitleAgent
- ReviewAgent
- PublishAgent



---


# 七、当前Agent开发状态



| Agent | 状态 |
|-|-|
| BaseAgent | 完成 |
| ProductionController | 基础完成 |
| NewsAgent | 完成 |
| NewsVerifier | 完成 |
| SourceRanker | 开发中 |
| TopicScorer | 规划 |
| ScriptAgent | 规划 |
| StoryboardAgent | 规划 |
| MaterialAgent | 规划 |
| VideoAgent | 规划 |
| AudioSubtitleAgent | 规划 |
| ReviewAgent | 规划 |
| PublishAgent | 规划 |



---

# END