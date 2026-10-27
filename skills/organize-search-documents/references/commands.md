# 命令与运行条件

在技能目录执行；Python 3.9+，推荐 3.12。完整文件解析依赖：`pypdf>=6,<7`、`python-docx>=1.2,<2`、`openpyxl>=3.1.5,<4`。TXT/Markdown/CSV 和 SQLite 使用 Python 标准库。

```sh
python scripts/docflow.py doctor
python scripts/docflow.py sync --root /authorized/documents --db /separate/state/index.sqlite3
python scripts/docflow.py inventory --db /separate/state/index.sqlite3
python scripts/docflow.py search --db /separate/state/index.sqlite3 --query "付款" --limit 20 --offset 0
python scripts/docflow.py export --db /separate/state/index.sqlite3 --query "付款" --dest /separate/new-bundle
python scripts/docflow.py copy-archive --db /separate/state/index.sqlite3 --dest /separate/archive
```

Windows 使用实际盘符路径并加引号。索引的父目录须已存在；一份索引绑定一个源目录。导出目录必须是新目录，不覆盖前次导出。归档执行在同一命令追加 `--apply`，复制文件保留内容但不保证原文件权限/时间属性。

扫描 PDF 可在 sync 后追加 `--ocr --lang chi_sim+eng`。需要系统安装 Poppler 的 pdftoppm、Tesseract 和对应语言包。`doctor` 仅检查可执行文件是否可找到，不证明语言包可用。OCR 仅处理没有原生文字的页，最多前 20 页；混合页里的图片文字可能遗漏。当前版本未完成真实 OCR 成功识别验证。

## 数据与限制

- SHA-256 检测内容变化，缓存键含扩展名与脚本配置；成功结果可复用，失败结果重试。OCR 模式每次重新解析。
- 完整目录枚举失败时不提交新快照。正常完成的完整扫描会移除已删除文件的旧检索内容。检索是上次 sync 的快照，不实时读取原件。
- 状态 `ok` 仅指声明的解析范围完成，不表示完整覆盖文档所有对象；`partial` 表示有空白/待 OCR 页或无文本；`error` 不返回该文件的部分片段；`unsupported` 需先转换副本。
- 默认 50 MiB/文件、100 万提取字符/文件、1000 PDF 页、100 万遍历单元格/工作表、200 MiB Office 解压声明大小、240 秒/文件解析。超限报错，不静默当作完整成功。
- 中文/英文大小写及全半角规范化匹配。每块 2000 字符，重叠 200 字符；不跨 PDF 页或 Word 段落匹配。重叠块可能产生重复证据。
- Word 仅正文段落与顶层表格单元格，不覆盖页眉页脚、嵌套表格、文本框、修订、批注。Excel 读取可见及隐藏表格；公式不重算，缺失缓存为 MISSING，已存缓存新鲜度未知。
- UTF-8 优先，失败再尝试 GB18030，并标记推断。没有任意编码自动识别承诺。
- 隐藏文件和符号链接被排除；工具用于可信本地资料，不是恶意文件隔离沙箱。处理期间勿并发修改目录。SQLite 保证写事务串行，未做高并发或大型资料库压力验证。

退出码：0 正常；2 sync 已完成但存在文件异常；1 全局失败。归档的冲突、排除项需读取 JSON 清单，不能只看退出码。
