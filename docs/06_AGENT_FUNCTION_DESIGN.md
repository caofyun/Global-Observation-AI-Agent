# 环球观察速递 AI Agent 工厂

# Agent功能与接口详细设计 V2.1


版本：

V2.1


更新时间：

2026-08-19


项目目标：

定义所有AI Agent的职责、接口、输入输出规范。

本文件作为 AI Coding Agent 开发依据。


---

# 一、Agent设计规范


## 1. Agent统一原则


所有Agent必须满足：


## （1）单一职责原则

每个Agent只负责一个明确任务。


## （2）标准输入输出

Agent之间通过标准数据文件通信。


统一采用：

JSON作为Agent通信标准。


辅助展示：

Markdown

Excel

PDF


用于人工阅读。


## （3）可独立测试


每个Agent必须拥有对应测试文件。


代码：

```text
src/agents/
测试：
tests/
（4）可追踪状态

每个Agent执行过程必须记录：

输入数据
输出数据
执行状态
错误信息
执行时间
二、Agent基础接口

所有Agent继承：

文件：
src/agents/base_agent.py
基础能力：

Agent初始化
参数管理
日志记录
状态管理
执行入口

标准执行方法：
run()
执行状态：
INIT

↓

RUNNING

↓

SUCCESS

↓

FAILED
三、AI生产总控模块
ProductionController

文件：
src/core/production_controller.py
定位：

整个AI内容生产系统的大脑。

职责：

创建项目
调度Agent
管理生产流程
控制人工确认节点
保存项目状态

输入：

用户创作需求

示例：
制作：

美国航母进入中东

90秒军事资讯视频
输出：
project.json
当前状态：

✅ 基础版本完成

代码：
src/core/production_controller.py
下一步：

接入完整Agent工作流状态管理。

四、NewsAgent

名称：

新闻发现Agent

文件：
src/agents/news_agent.py
定位：

AI新闻记者。

职责：

负责：

新闻搜索
新闻采集
信息整理
来源记录

输入：

新闻主题

示例：
霍尔木兹海峡局势
输出：

search_results.json

数据路径：

projects/{project_name}/01_新闻资料/

当前状态：

✅ V2.0基础完成
代码：

src/agents/news_agent.py

测试：

tests/test_news_agent.py
五、NewsVerifier

名称：

新闻真实性验证Agent

文件：

src/agents/news_verifier.py

定位：

AI事实核验员。

职责：

检查：

新闻完整性
来源可信度
信息一致性
缺失信息
风险提示

输入：

search_results.json

输出：
verification.json
数据路径：

projects/{project_name}/01_新闻资料/

输出内容包括：

verification_status
confidence_score
risk_notes
missing_information

当前状态：
✅ V2.0基础完成

代码：

src/agents/news_verifier.py

测试：

tests/test_news_verifier.py
六、SourceRanker

名称：

新闻来源评级Agent

文件：

src/agents/source_ranker.py

定位：

新闻来源分析专家。

职责：

评价：

来源权威性
来源可靠性
信息透明度

输入：
verification.json
输出：

source_rank.json

当前状态：

🚧 V2.0开发中

代码：

src/agents/source_ranker.py

测试：

tests/test_source_ranker.py
七、TopicScorer
名称：

热点价值评分Agent

状态：

规划

预计阶段：

Phase 2

定位：

判断新闻是否值得制作视频。

职责：

评分：

国际影响力
新闻热度
用户关注度
视频传播潜力

输入：

source_rank.json

输出：

topic_score.json
八、ScriptAgent

名称：
脚本编导Agent

状态：

规划

定位：

AI视频编导。

职责：

生成：

视频标题
开场钩子
旁白稿
视频结构

输入：

topic_score.json


verification.json


source_rank.json

输出：

script.md

数据内容：

标题
开场
旁白
节奏
时长
九、StoryboardAgent

名称：

分镜导演Agent

状态：

规划

定位：

AI导演。

职责：

根据脚本生成：

时间轴
镜头设计
画面需求
素材需求

输入：

script.md

输出：

主要通信文件：

storyboard.json

辅助展示文件：

storyboard.xlsx
十、MaterialAgent
名称：

素材管理Agent

状态：

规划

定位：

AI资料员。

职责：

素材搜索
素材分类
素材标签
素材审核
素材打包

输入：

storyboard.json

输出：

material_package/

包含：

materials.json


图片素材


视频素材


地图素材
十一、VideoAgent
名称：

视频制作Agent

状态：

规划

定位：

AI剪辑师。

职责：

生成：

剪辑方案
时间线
转场建议
特效建议
BGM方案

输入：

material_package


storyboard.json


script.md

输出：

主要通信文件：

production.json

辅助文件：

editing_plan.md
十二、AudioSubtitleAgent

名称：

声音字幕Agent
状态：

规划

职责：

生成：

AI配音
字幕文件
字幕样式

输入：

script.md

输出：

voice.wav


subtitle.srt
十三、ReviewAgent
名称：

审核优化Agent

状态：

规划

定位：

AI审核员。

职责：

审核：

内容
是否事实准确
是否存在未经证实信息
标题
是否夸张
是否标题党
平台
是否存在违规风险

输入：

production.json


verification.json


script.md

输出：

主要通信文件：

review.json

辅助文件：

review_report.md
十四、PublishAgent
名称：

发布助手Agent

状态：

规划

职责：

生成：

发布标题
视频简介
标签
评论引导

输入：

review.json

输出：

主要通信文件：

publish.json

辅助文件：

publish_info.md
十五、人工确认机制

所有关键节点支持：

人工确认。

状态：

WAIT_USER_CONFIRM

流程：

AI生成

↓

人工审核

↓

确认

↓

进入下一阶段

必须确认节点：

新闻选题确认
脚本确认
素材确认
成片确认
发布确认
十六、整体数据流

用户需求

↓

ProductionController

↓

NewsAgent

↓

search_results.json

↓

NewsVerifier

↓

verification.json

↓

SourceRanker

↓

source_rank.json

↓

TopicScorer

↓

topic_score.json

↓

ScriptAgent

↓

script.md

↓

StoryboardAgent

↓

storyboard.json

↓

MaterialAgent

↓

materials.json

↓

VideoAgent

↓

production.json

↓

AudioSubtitleAgent

↓

voice.wav + subtitle.srt

↓

ReviewAgent

↓

review.json

↓

PublishAgent

↓

publish.json

↓

人工确认

↓

发布
十七、开发规则

新增Agent必须同步创建：

代码
src/agents/
测试
tests/test_xxx_agent.py
设计文档
docs/

禁止：

未完成设计直接开发。

所有Agent开发流程：

设计

↓

接口定义

↓

代码实现

↓

测试

↓

Git提交

↓

更新PROJECT_STATUS
十八、当前Agent开发状态
| Agent                | 状态      |
| -------------------- | ------- |
| ProductionController | 基础完成    |
| BaseAgent            | 完成      |
| NewsAgent            | V2.0完成  |
| NewsVerifier         | V2.0完成  |
| SourceRanker         | V2.0开发中 |
| TopicScorer          | 规划      |
| ScriptAgent          | 规划      |
| StoryboardAgent      | 规划      |
| MaterialAgent        | 规划      |
| VideoAgent           | 规划      |
| AudioSubtitleAgent   | 规划      |
| ReviewAgent          | 规划      |
| PublishAgent         | 规划      |
十九、版本说明
V2.1

主要更新：

统一Agent通信标准为JSON
修正Agent输入输出接口
统一Storyboard、Production、Review、Publish数据格式
增加Agent状态管理规范
与PROJECT_STATUS V2.0同步
