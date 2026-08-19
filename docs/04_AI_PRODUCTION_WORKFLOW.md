# 环球观察速递 AI Agent 工厂

# AI生产工作流设计 V2.0


版本：

V2.0


更新时间：

2026-08-19



---

# 一、文档定位



本文件定义：

环球观察速递 AI Agent 工厂运行流程。


前置文档：

## 01_SYSTEM_ARCHITECTURE

解决：

系统是什么。



## 02_AGENT_DESIGN

解决：

有哪些Agent。



## 03_DATA_STRUCTURE_DESIGN

解决：

数据如何流转。



## 04_AI_PRODUCTION_WORKFLOW

解决：

Agent按照什么顺序运行。

什么时候自动执行。

什么时候等待人工确认。



---

# 二、设计目标



建立一套：


AI自动执行

+

人工关键审核


的视频生产工作流。


目标：


从新闻发现开始，


最终生成：


- 视频项目
- 视频脚本
- 分镜方案
- 素材包
- 剪辑方案
- 审核报告
- 发布资料



---

# 三、总体工作流程



完整流程：

用户提出选题

↓

ProductionController

↓

NewsAgent
新闻搜索

↓

NewsVerifier
事实核验

↓

SourceRanker
来源评级

↓

TopicScorer
热点评分

↓

人工确认选题

↓

ScriptAgent
脚本生成

↓

人工确认脚本

↓

StoryboardAgent
分镜设计

↓

MaterialAgent
素材管理

↓

人工确认素材

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
发布资料生成

↓

人工最终确认

↓

发布平台



---

# 四、项目状态管理



每个项目通过状态管理整个生命周期。


状态流程：

CREATED

项目创建

↓

NEWS_SEARCHING

新闻搜索中

↓

NEWS_VERIFYING

新闻真实性验证中

↓

SOURCE_RANKING

来源评级中

↓

TOPIC_SCORING

热点价值评分中

↓

WAIT_NEWS_CONFIRM

等待新闻选题确认

↓

SCRIPT_GENERATING

脚本生成中

↓

WAIT_SCRIPT_CONFIRM

等待脚本确认

↓

STORYBOARD_CREATING

分镜生成中

↓

MATERIAL_PREPARING

素材准备中

↓

WAIT_MATERIAL_CONFIRM

等待素材确认

↓

VIDEO_CREATING

视频制作中

↓

AUDIO_CREATING

声音字幕处理中

↓

REVIEWING

审核中

↓

WAIT_PUBLISH_CONFIRM

等待发布确认

↓

COMPLETED

完成



异常状态：

ERROR



记录：
error.log



---

# 五、详细工作流程设计



# Step 1 新闻搜索阶段



## 输入



用户输入：


例如：

美国航母进入中东



## 执行Agent


NewsAgent



## 工作内容



- 搜索相关新闻
- 收集新闻来源
- 整理新闻信息
- 提取关键事实



## 输出

search_results.json



状态：

NEWS_SEARCHING

↓

NEWS_VERIFYING



---


# Step 2 新闻真实性验证阶段



## 执行Agent


NewsVerifier



## 输入

search_results.json



## 工作内容



检查：


- 信息完整性
- 新闻一致性
- 多来源验证
- 潜在风险



## 输出

verification.json



状态：

NEWS_VERIFYING

↓

SOURCE_RANKING



---

# Step 3 新闻来源评级阶段



## 执行Agent


SourceRanker



## 输入

verification.json




## 工作内容



分析：


- 来源权威性
- 来源可靠性
- 来源透明度
- 信息可信等级



## 输出

source_rank.json



状态：

SOURCE_RANKING

↓

TOPIC_SCORING



---

# Step 4 热点价值评分阶段



## 执行Agent


TopicScorer



## 输入

source_rank.json



## 评分维度



- 国际影响力
- 新闻热度
- 用户关注度
- 传播潜力
- 制作价值



## 输出

topic_score.json



状态：

WAIT_NEWS_CONFIRM



等待人工确认。


用户决定：


继续制作


或者：


修改选题。



---

# Step 5 脚本生成阶段



## 执行Agent


ScriptAgent



## 输入

topic_score.json



## 工作内容



生成：


- 视频标题
- 开场钩子
- 旁白文本
- 视频结构
- 时长设计



## 输出

script.md



状态：

WAIT_SCRIPT_CONFIRM



人工确认：


- 标题
- 表达方式
- 内容方向



---

# Step 6 分镜设计阶段



## 执行Agent


StoryboardAgent



## 输入

script.md



## 工作内容



将文字转换为：


- 时间轴
- 镜头编号
- 画面需求
- 素材关键词



## 输出

storyboard.json



示例：

镜头1

时间：

00:00-00:05

旁白：

美国航母进入中东地区

画面：

航母航行

素材关键词：

US aircraft carrier



---

# Step 7 素材准备阶段



## 执行Agent


MaterialAgent



## 输入

storyboard.json



## 工作流程

关键词分析

↓

素材搜索

↓

素材下载

↓

版权检查

↓

分类

↓

命名

↓

项目打包



## 输出

materials.json




状态：

WAIT_MATERIAL_CONFIRM



人工确认：


- 使用哪些素材
- 删除哪些素材



---

# Step 8 视频制作阶段



## 执行Agent


VideoAgent



## 输入

storyboard.json

materials.json

script.md



## 工作内容



生成：


- 视频时间线
- 镜头顺序
- 转场方案
- 特效方案
- BGM方案
- 字幕位置



## 输出

production.json




---

# Step 9 声音字幕阶段



## 执行Agent


AudioSubtitleAgent



## 输入

script.md



## 输出

voice.wav

subtitle.srt




---

# Step 10 审核阶段



## 执行Agent


ReviewAgent



## 检查内容



### 事实风险


检查：

- 是否存在未经证实信息
- 是否存在错误描述



### 标题风险


检查：

- 是否夸大
- 是否标题党



### 平台风险


检查：

- 敏感表达
- 违规内容



## 输出

review.json



---

# Step 11 发布阶段



## 执行Agent


PublishAgent



## 输入

review.json



## 输出

publish.json



内容：


- 发布标题
- 视频简介
- 标签
- 评论引导



状态：

WAIT_PUBLISH_CONFIRM



等待人工确认。



---

# 六、人工控制设计



系统原则：


AI负责执行。


人负责最终决策。



所有关键节点：



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


# 七、异常处理机制



任何Agent失败：


状态：
ERROR



记录：

error.log



支持：


- 重新执行
- 查看错误原因
- 人工修正输入



---

# 八、未来自动化方向



## 1. 自动任务队列



支持：

多个新闻项目同时运行。



---


## 2. Agent自动通信系统



实现：

Agent之间自动调用。



---


## 3. 数据反馈系统



根据视频表现优化：


- 标题
- 脚本
- 素材
- 发布时间



---


# 九、核心原则



## AI负责：


重复性工作。



包括：

- 搜索
- 整理
- 分析
- 生成



---


## 人负责：


关键决策。


包括：

- 选题方向
- 内容审核
- 发布决定



---


## 所有结果：


必须：


- 可追踪
- 可修改
- 可复用



---


# END
