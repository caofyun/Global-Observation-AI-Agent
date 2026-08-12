\# 环球观察速递 AI内容生产智能体



\# 系统数据结构设计 V1.0





\# 一、设计目标





为了实现多个AI Agent之间协同工作，



系统需要建立统一的数据标准。





所有Agent：



输入标准数据



↓



处理任务



↓



输出标准数据







避免：



\- 文件格式混乱

\- Agent之间无法通信

\- 项目管理困难







\---



\# 二、核心数据流





完整生产流程：

新闻选题



↓



project.json



↓



news.json



↓



script.json



↓



storyboard.json



↓



materials.json



↓



production.json



↓



review.json



↓



publish.json







\---



\# 三、项目核心文件





\## 1. project.json





作用：



管理整个视频项目。





示例：





```json

{

&#x20;   "project\_id": "20260812\_US\_Carrier",



&#x20;   "title": "美国航母进入中东",



&#x20;   "platform": \[

&#x20;       "抖音",

&#x20;       "B站"

&#x20;   ],



&#x20;   "duration": "60s",



&#x20;   "status": "script\_review",



&#x20;   "created\_time": "",



&#x20;   "agents\_status": {



&#x20;       "news\_agent": "completed",



&#x20;       "script\_agent": "waiting",



&#x20;       "material\_agent": "pending"



&#x20;   }



}



四、新闻数据结构



文件：



news.json



负责：



新闻研究Agent输出。



保存：

{



"topic":"美国航母进入中东",





"event\_time":"",





"summary":"",





"sources":\[



],



"key\_points":\[



],





"risk\_notes":\[



]





}



包含：



新闻标题

来源

背景

关键事实

风险提示



五、脚本数据结构



文件：



script.json



负责：



脚本Agent输出。



结构：

{



"title":"",



"hook":"",



"duration":"60s",





"voice\_script":\[





{



"time":"00:00-00:05",



"text":""



}





],





"tone":"新闻资讯"





}

保存：



标题

开场

旁白

时长

风格



六、分镜数据结构



文件：



storyboard.json



负责：



分镜导演Agent输出。



示例：

{



"scenes":\[





{



"id":1,





"time":"00:00-00:05",





"voice":"",





"visual":



"美国航母画面",





"material\_keywords":\[



"aircraft carrier",



"US Navy"



]





}



]



}

保存：



镜头编号

时间

旁白

画面

素材需求



七、素材数据结构



文件：



materials.json



负责：



素材管理Agent。



示例：

{





"materials":\[





{



"id":"001",





"type":"image",





"filename":"",



"path":"",





"category":"军事装备",





"source":"",





"license":"",





"used\_scene":1





}



]





}



八、视频制作数据结构



文件：



production.json



负责：



视频制作Agent。



示例：

{





"timeline":\[





{



"start":"00:00",



"end":"00:05",



"material":"001",



"effect":"zoom",



"subtitle":""



}





],





"music":"",



"transition":""



}



保存：



时间线

素材

特效

字幕

BGM



九、审核数据结构



文件：



review.json



负责：



审核Agent。



示例：

{





"fact\_check":"pass",





"title\_check":"pass",





"platform\_risk":"low",





"suggestions":\[



]





}

保存：



事实审核

标题审核

平台风险

修改建议



十、发布数据结构



文件：



publish.json



负责：



发布助手Agent。



保存：

{





"title":"",





"description":"",





"hashtags":\[



],





"status":"waiting\_user\_confirm"





}



十一、项目文件结构标准



每个视频项目：

20260812\_美国航母事件





│



├──project.json





├──01\_新闻资料



│   └──news.json





├──02\_脚本



│   └──script.json





├──03\_分镜



│   └──storyboard.json





├──04\_素材



│   ├──materials.json



│   ├──图片



│   └──视频





├──05\_制作



│   └──production.json





├──06\_审核



│   └──review.json





└──07\_发布



&#x20;   └──publish.json



十二、设计原则

1\. 数据独立



每个Agent只负责自己的数据。



2\. 数据可追溯



所有修改保存记录。



3\. 支持人工修改



用户可以：



修改JSON



↓



继续生产流程。



4\. 支持未来升级



未来可以接入：



数据库

云存储

工作流引擎

多Agent框架

十三、未来扩展



可能增加：



用户反馈数据



保存：



哪些视频表现好。



素材评分数据



保存：



哪些素材效果最好。



AI优化数据



用于：



持续提升生产质量。



\---



保存后：



GitHub Desktop：



Commit：



```text

Create system data structure design document



