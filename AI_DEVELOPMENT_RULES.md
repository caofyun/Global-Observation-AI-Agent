# AI开发规则

版本：

V1.1


更新时间：

2026-08-18



---

# 1. 基本开发原则


## 原则1：先理解，再修改


任何代码修改前：

必须先了解：

- 项目当前状态
- 系统架构
- 当前任务目标
- 相关模块依赖



禁止：

不了解代码结构直接修改。



---

# 2. 修改代码前必须阅读


修改任何代码前：

必须阅读：


项目上下文：
docs/PROJECT_CONTEXT.md


项目状态：
docs/00_PROJECT_STATUS.md


当前任务：
docs/TASKS.md


相关设计文档：
docs/



如果涉及已有Agent：

必须阅读对应设计文档。



---

# 3. 架构保护规则


禁止：

- 擅自改变系统架构
- 删除已有功能
- 重复创建已有模块
- 修改无关文件



修改前必须：

分析：

- 输入
- 输出
- 数据流
- 模块依赖



---

# 4. Agent开发规范


新增或升级Agent：

必须包含：


## 1. 设计文档


说明：

- Agent目标
- 功能范围
- 输入数据
- 输出数据
- 工作流程



---


## 2. 代码实现


位置：
src/agents/



---


## 3. 数据结构


必须明确：

输入格式

输出格式



例如：
xxx_input.json

xxx_output.json



---


## 4. 测试文件


位置：
tests/



必须验证：

- 正常流程
- 异常情况
- 输出结果



---

# 5. 数据结构保护规则


已有数据结构：

不得随意修改。


例如：
search_results.json

verification.json

ai_verification.json



如果需要修改：

必须：

1. 更新设计文档

2. 更新相关代码

3. 更新测试

4. 记录CHANGELOG



---

# 6. AI模型调用规则


AI调用必须通过：
AIModelClient



禁止：

在Agent内部直接调用：

- Gemini API
- OpenAI API
- 其他模型接口



目的：

保持：

模型可替换。



---

# 7. 测试规则


任何代码修改后：

必须运行测试。



流程：
修改代码

↓

运行pytest

↓

确认结果

↓

提交Git



测试失败：

必须继续定位问题。


禁止：

忽略失败测试。



---

# 8. 文档同步规则


每完成一个功能：

必须更新：

CHANGELOG.md



每完成一个阶段：

必须更新：

docs/00_PROJECT_STATUS.md

docs/PROJECT_CONTEXT.md

docs/TASKS.md



---

# 9. Git管理规则


每完成一个功能：

执行：

git add

git commit

git push



Commit信息必须清晰。


例如：
Add NewsVerifier V2.0 AI analysis



禁止：

使用：
update

test

修改


等无法说明内容的信息。



---

# 10. 文件修改规则


修改代码时：

优先提供完整文件。


避免：

- 局部替换错误
- 缩进错误
- 遗漏代码



修改必须注明：

- 修改原因
- 修改位置
- 影响范围



---

# 11. 不确定处理规则


当需求不明确：

必须先确认。


禁止：

- 猜测需求
- 自行扩大功能范围
- 修改无关模块



---

# 12. 项目开发标准流程


所有功能遵循：

需求分析

↓

设计文档

↓

数据结构设计

↓

代码实现

↓

测试验证

↓

更新文档

↓

Git提交

↓

版本记录



---

# 13. 当前项目特殊原则


Global-Observation-AI-Agent：

采用：

AI辅助 + 人工审核模式。



AI负责：

- 信息整理
- 数据分析
- 内容生成
- 自动化执行



人工负责：

- 新闻真实性判断
- 内容审核
- 最终发布



---

# 当前版本


AI_DEVELOPMENT_RULES V1.1

状态：

Active Development
