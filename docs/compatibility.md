# 主流 AI 支持范围与核验记录

核验日期：2026-10-27。这里的“支持”分三层：**官方产品具备入口、项目提供对应适配、实际端到端运行通过**。三者不能互相替代。

| 平台 | 本次核实的官方能力 | 本项目的适配方式 | 本项目在平台内实测 |
| --- | --- | --- | --- |
| 腾讯 WorkBuddy | 官方开放平台定义 SKILL.md、scripts、references 及市场元数据 | 标准源 Skill + WorkBuddy 专用元数据 ZIP | 未安装、未运行、未上架市场 |
| 豆包文件 / 对话 | 官方已登录网页存在“上传文件或图片”，文件选择器声明 PDF、DOCX、XLSX、CSV、TXT、MD 等 | 上传证据 TXT/MD 或原文件，复制提示词 | 只核验入口及格式声明；未上传、未验证解析与回答 |
| ChatGPT / Codex | 官方 Build skills 说明 SKILL.md 技能结构及产品入口差异 | 标准 Skill；不能执行本地脚本时粘贴证据和提示词 | 本地脚本在 Codex 工具环境运行；未完成新 Skill 安装与自动触发验收 |
| Claude | 官方支持 PDF、DOCX、CSV、TXT、JSON 等；XLSX 需开启代码执行与文件创建 | evidence.txt + 提示词 | 未在 Claude 内上传或验收 |
| Gemini Apps | 官方支持上传文档、表格等，受账户与配额限制 | evidence.txt + 提示词；不接受时粘贴文本 | 未在 Gemini 内上传或验收 |
| 其他文本对话 AI | 未逐个核验具体产品 | 复制少量证据文本和提示词；属于通用方案 | 不声称官方认证、原生集成或已实测 |

## WorkBuddy

1. 在项目根目录运行 `python tools/build_skill.py --target workbuddy`。
2. 得到 `dist/docflow-workbuddy-0.1.0.zip`，内有单一 `organize-search-documents/` 目录，包含脚本、参考说明和 requirements.txt。
3. 官方文档介绍的入口为“专家·技能·连接器 → 技能”，并提供“添加技能 → 创建技能”。在当前客户端提供的自定义技能流程中使用该包；若客户端没有导入入口，不猜测安装目录，可让 WorkBuddy 根据目录内 SKILL.md 创建技能，或回到文本模式。
4. 首次调用先确认执行环境能访问指定资料并运行 Python；安装依赖后执行 doctor 和模拟案例。ZIP 结构正确并不等于宿主已安装成功。

WorkBuddy 开放平台要求的展示名称、双语描述、版本和作者由构建器补齐。通用源 SKILL.md 只保留标准必需字段，避免把平台专属字段强塞给其他宿主。两份包由同一脚本生成，不独立维护两份代码。

官方依据：[WorkBuddy 开放平台技能结构](https://open.workbuddy.cn/docs/skill)、[WorkBuddy 技能管理](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)。这不是 CodeBuddy CLI 安装路径的推断，也未申请市场上架。

## 豆包文件

本次在 [豆包官方网页](https://www.doubao.com/chat/) 观察到“上传文件或图片”和“选择云盘文件”。网页文件选择器声明的相关扩展名包含 `.pdf,.txt,.csv,.docx,.doc,.xlsx,.xls,.pptx,.ppt,.md`；这里只证明当前页面的格式声明，不能证明服务端完整读取、OCR 准确率或账户上传配额。

推荐先使用已生成的 `examples/evidence/evidence.txt`，配合 `prompts/ask-with-evidence.txt`。普通聊天不能替代本地 Python 执行；不能说上传 Python 脚本后豆包就会运行整个资料库工作流。

网页中虽可见“插件·技能·伙伴”，本次没有核验自定义技能安装规范，**不据此宣称这份 Skill 可在豆包原生安装**。也未将火山引擎 API 的文件能力当作豆包消费端的能力。

## ChatGPT / Codex

[官方 Build skills](https://learn.chatgpt.com/docs/build-skills) 定义技能目录和 name、description。宿主入口、独立技能与插件分发有所区别，以当前产品支持的安装入口为准。上传一份 Markdown 到普通对话只是提供内容，不能等同安装或获得本地文件权限。

需要标准格式详情时参考 [Agent Skills specification](https://agentskills.io/specification)。本项目没有开发 MCP 服务或 OpenAI API 集成。

## Claude 与 Gemini

- [Claude 文件上传文档](https://support.claude.com/en/articles/8241126-upload-files-to-claude)：支持 TXT 等文档；XLSX 有能力开关条件，非 PDF 文件主要提取文字。这里仅提供文件模式，不声称 Claude Skills 已验收。
- [Gemini 文件上传文档](https://support.google.com/gemini/answer/14903178?hl=en)：支持文档和表格上传；账户、大小与数量限制应以当前页面为准。这里不涉及 Gemini CLI 的技能机制。

## 如何完成一次平台验收

使用虚构示例，记录日期、客户端/账户能力、提交的文件、原始回答及可核对的出处。检查“30 天”是否正确、有无编造验收日期、是否保留发票条件。安装、脚本运行、文件读取、引用正确、回答合理是五个独立检查项；失败时保留结果，不改写成成功。
