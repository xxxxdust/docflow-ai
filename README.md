# DocFlow AI · 文档整理与检索

**把 PDF、Word、Excel 变成可追溯的问答证据。支持 WorkBuddy、豆包文件及主流 AI 的分层适配：标准 Skill、通用文件、可复制提示词。**

本地程序负责读取、查重、检索与导出；你选择的 AI 负责根据证据回答。无需模型 API Key，程序不联网、不上传资料。

> 版本 0.1.0 · 早期可验证版本。支持范围不等于原生集成认证：WorkBuddy 有官方技能结构依据；豆包已核对官方文件入口；各平台端到端安装、解析和问答效果仍需实测。[查看兼容性证据](docs/compatibility.md)

## 先选适合你的用法

| 你正在用什么 | 从哪里开始 | 实际提供什么 |
| --- | --- | --- |
| 腾讯 WorkBuddy | [WorkBuddy 接入](docs/compatibility.md#workbuddy) | 按官方结构生成的技能包；需宿主能执行 Python |
| 豆包文件 / 豆包对话 | [通用提示词](prompts/ask-with-evidence.txt) | 上传原文件或 evidence.txt；也可直接粘贴文本 |
| ChatGPT / Claude / Gemini | [兼容性与操作方式](docs/compatibility.md) | 通用证据文本与提示词；不冒充平台连接器 |
| Codex 或支持 Agent Skills 的宿主 | [标准 Skill](skills/organize-search-documents/SKILL.md) | 独立技能目录、脚本及命令参考 |
| 不使用 AI | 下面的快速开始 | 仍可本地整理、关键词搜索、生成归档副本 |

## 五分钟跑通模拟资料

需要 Python 3.9+，推荐 3.12。以下命令在项目根目录执行。

```sh
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell 请改为：.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

python docflow.py doctor
python docflow.py sync --root examples/input --db index.sqlite3
python docflow.py search --db index.sqlite3 --query "付款"
python docflow.py export --db index.sqlite3 --query "付款" --dest exports/first-run
```

打开 `exports/first-run/evidence.txt`，将它和 [提示词](prompts/ask-with-evidence.txt) 一起交给 AI。如果平台不接受文件，就粘贴文本。再次导出时使用新目录，例如 `exports/second-run`，避免覆盖。

可直接试问：**“付款条件是什么？现在能确定付款到期日吗？”**

预期依据：模拟合同明确“验收通过后 30 天内支付尾款”，还列出发票条件；没有验收日期，不能算出确定到期日。程序只输出原文，AI 的回答质量要另行核对。[查看已生成的模拟证据包](examples/evidence/evidence.txt)

## 能做什么

`资料目录 → 内容哈希与解析 → SQLite 快照 → 关键词检索 → 带出处的 TXT / Markdown / JSON → AI 回答`

- PDF 定位到物理页；Word 定位到正文段落和表格；Excel 定位到工作表及单元格。
- 区分公式、保存的计算值和缺失缓存，不擅自重算。
- 内容变化后更新；完整扫描后不再返回已删除来源；相同内容保留多条来源。
- 损坏、不支持、超限和待 OCR 文件进入异常清单。
- 归档先预览，授权后复制；不删除原件，不覆盖冲突目标。
- Skill 脚本可独立运行；导出资料包可跨 AI 使用。

## 归档前先看清单

```sh
python docflow.py inventory --db index.sqlite3
python docflow.py copy-archive --db index.sqlite3 --dest archive
```

确认目标与清单后，在第二条命令末尾追加 `--apply` 才执行复制。按扩展名分组，文件名带完整内容哈希。业务分类（项目、客户、年份）尚未实现。

## 必须知道的边界

- **关键词检索，不是语义搜索。** 多个词在同一块内按 AND 匹配；`has_more=true` 时结果未列全。
- **索引是快照。** 需要最新结论时先重新 sync。程序不监控目录，也未配置定时任务。
- **扫描件需要 OCR。** 有可选调用入口，但本次缺少 Tesseract，成功识别尚未验证。无原生文本的页会明确提示，不能当作已读。
- **不是完整 Office 渲染器。** Word 文本框、批注等及 Excel 图表不在读取范围；混合 PDF 页的图片文字可能遗漏。
- **不是云端连接器。** 没有 WorkBuddy API、豆包 API、模型 SDK、账户同步或自动上传。AI 平台读取证据后的数据处理取决于该平台。
- **只用模拟数据验证。** 真实客户资料、大规模性能、Windows 和 Linux 实机、长期调度及各 AI 问答效果未验证。

完整参数、大小限制和退出码见 [命令参考](skills/organize-search-documents/references/commands.md)。

## 测试与项目文件

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python tools/build_skill.py --target standard
python tools/build_skill.py --target workbuddy
```

- [测试报告](docs/validation.md)：本版本实际执行结果与未验证项。
- [兼容性](docs/compatibility.md)：逐项官方来源与证据边界。
- [来源与版本差异](docs/provenance.md)：由搭建记录重建，不继承旧版测试结论。
- [数据与发布说明](docs/privacy.md)：原件、证据包、索引的处理方式。

发布包只包含程序、文档、提示词和虚构示例。不应把自己的文档、索引或密钥提交到仓库。
