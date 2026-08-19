# Global-Observation-AI-Agent

# TASKS

版本：

V1.0


更新时间：

2026-08-18


项目状态：

Active Development



---

# 1. Current Sprint


当前阶段：

Phase 1


Sprint目标：

完成 NewsVerifier V2.0 升级



目标：

将基础新闻验证能力升级为 AI 辅助事实核验系统。



---

# 2. 当前进行任务


## NewsVerifier V2.0 Upgrade


状态：

进行中



目标：

增加：

- AI事实分析
- 新闻事实主张提取
- 多来源冲突检测
- 可信度评分
- 风险提示



输出：
ai_verification.json




任务：


- [x] NewsVerifier V1.0基础功能完成

- [x] AIModelClient接入完成

- [ ] AI事实分析模块开发

- [ ] Claim Extraction开发

- [ ] 来源冲突检测开发

- [ ] 可信度评分开发

- [ ] ai_verification.json生成

- [ ] 单元测试更新

- [ ] Git提交



---


# 3. Next Sprint


## HotspotScore Agent


状态：

计划



目标：

根据新闻热度：

- 时间
- 来源数量
- 传播范围
- 国际影响


生成新闻热度评分。


预计输出：
hotspot_score.json




---


# 4. Future Roadmap


## ScriptAgent


状态：

计划



功能：

根据核验后的新闻：

自动生成：

- 视频标题
- 口播稿
- 分镜脚本



---


## StoryboardAgent


状态：

计划



功能：

生成：

- 镜头规划
- 素材需求
- 时间轴设计



---


## MaterialAgent


状态：

计划



功能：

- 素材搜索
- 素材下载
- 素材分类
- 素材匹配



---


## VideoAgent


状态：

计划



功能：

- 视频生成
- 字幕
- 转场
- BGM
- 自动剪辑



---


# 5. Development Workflow


所有任务遵循：

需求

↓

设计文档

↓

代码实现

↓

测试

↓

更新docs

↓

Git commit

↓

Git push




---


# 6. Task Rules


## 新功能开发


必须：

1. 创建设计文档

2. 编写代码

3. 编写测试

4. 更新状态文档

5. 提交Git



---


## Agent开发原则


每个Agent必须包含：
Agent文件

↓

输入数据结构

↓

处理逻辑

↓

输出数据结构

↓

测试文件



---


# 当前最高优先级


Priority 1:

完成：
NewsVerifier V2.0



Priority 2:

建立：
HotspotScore Agent



Priority 3:

开发：
ScriptAgent



---


# 当前版本


TASKS V1.0
