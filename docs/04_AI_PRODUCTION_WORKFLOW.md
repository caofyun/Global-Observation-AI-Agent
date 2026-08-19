\# 环球观察速递 AI内容生产智能体



\# AI生产工作流设计 V1.0



这份文档是整个系统的运行规则。

前面的文档解决：

做什么（愿景）

有哪些角色（Agent）

怎么存数据（数据结构）

这一份解决：

这些Agent按照什么顺序工作，什么时候自动运行，什么时候等待你确认。



\# 一、设计目标





建立一套：



AI自动执行



\+



人工关键审核





的视频生产流程。





目标：



从新闻选题开始，



最终生成：



\- 视频文件

\- 发布文案

\- 封面方案

\- 审核报告





\---



\# 二、整体工作流程





完整流程：

用户提出选题



↓



新闻研究Agent



↓



人工确认



↓



脚本编导Agent



↓



人工确认



↓



分镜导演Agent



↓



素材管理Agent



↓



人工确认素材



↓



视频制作Agent



↓



声音字幕Agent



↓



审核优化Agent



↓



人工确认发布



↓



发布助手Agent





\---



\# 三、项目状态管理





每个项目都有状态。





状态：

CREATED



项目创建



↓



NEWS\_ANALYSIS



新闻分析中



↓



WAIT\_NEWS\_CONFIRM



等待用户确认新闻



↓



SCRIPT\_GENERATING



脚本生成中



↓



WAIT\_SCRIPT\_CONFIRM



等待脚本确认



↓



STORYBOARD\_CREATING



生成分镜



↓



MATERIAL\_PREPARING



准备素材



↓



WAIT\_MATERIAL\_CONFIRM



等待素材确认



↓



VIDEO\_CREATING



视频制作



↓



REVIEWING



审核



↓



WAIT\_PUBLISH\_CONFIRM



等待发布确认



↓



COMPLETED



完成





\---



\# 四、详细流程设计





\# Step 1 新闻选题阶段





\## 输入：



用户输入：



例如：美国航母进入中东





\## 新闻研究Agent执行：





任务：



\- 搜索新闻

\- 整理背景

\- 收集来源

\- 判断新闻价值





输出：

news.json





状态：

WAIT\_NEWS\_CONFIRM





等待用户：



确认：



继续



或者：



修改主题。







\---



\# Step 2 脚本生成阶段





用户确认新闻后。





脚本Agent启动。





生成：

script.json





内容：



\- 标题

\- 开场

\- 旁白

\- 节奏

\- 时长







状态：WAIT\_SCRIPT\_CONFIRM





用户可以：



修改：



\- 标题

\- 表达方式

\- 内容长度







\---



\# Step 3 分镜设计阶段





脚本确认后。





分镜Agent启动。





生成：storyboard.json







内容：

镜头编号



时间



旁白



画面需求



素材关键词

例如：







镜头1



时间：

00:00-00:05



画面：



美国航母航行



素材：



aircraft carrier





\---



\# Step 4 素材准备阶段





素材Agent读取：storyboard.json





执行：

关键词分析



↓



素材搜索



↓



素材下载



↓



素材审核



↓



分类



↓



命名



↓



项目打包

输出：

materials.json

状态：

WAIT\_MATERIAL\_CONFIRM





用户确认：



哪些素材使用。







\---



\# Step 5 视频制作阶段





视频Agent读取：

storyboard.json



materials.json



script.json



生成：

production.json





包含：





\- 时间轴

\- 转场

\- 特效

\- BGM方案

\- 字幕位置







\---



\# Step 6 声音字幕阶段





声音字幕Agent执行：





输入：



script.json





输出：

voice.wav



subtitle.srt







\---



\# Step 7 审核阶段





审核Agent检查：





\## 内容审核





检查：



\- 是否符合事实



\- 是否存在未经证实信息







\## 标题审核





检查：



\- 是否夸大



\- 是否标题党







\## 平台审核





检查：



\- 敏感表达



\- 风险内容







输出：

review.json



\---



\# Step 8 发布阶段





发布助手生成：

publish.json





内容：



\- 标题

\- 简介

\- 标签

\- 发布时间建议





状态：

WAIT\_PUBLISH\_CONFIRM





最终由用户决定：



发布或修改。







\---



\# 五、人工控制设计





系统原则：



AI不能直接发布。





所有关键节点：





\## 节点1



新闻确认





\## 节点2



脚本确认





\## 节点3



素材确认





\## 节点4



成片确认





\## 节点5



发布确认







\---



\# 六、异常处理机制





如果某个Agent失败：



例如：



素材搜索失败。





状态：ERROR

记录：error.log







允许：



重新执行。





\---



\# 七、未来自动化方向





未来可以增加：





\## 自动任务队列





例如：



同时处理多个新闻项目。





\## Agent通信系统





实现：



Agent自动调用。





\## 数据反馈系统





根据视频表现：



优化：



标题



脚本



素材选择。







\---



\# 八、核心原则





\## AI负责：



重复劳动。





\## 人负责：



方向判断和最终决策。





\## 所有结果：



必须可追溯。





\## 所有阶段：



可以人工修改。







