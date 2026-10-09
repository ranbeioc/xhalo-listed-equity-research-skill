# 安装说明 | Listed Equity Research v1.0.1

## 问题说明

`README.md` 和 `SKILL.md` 不是完整技能包。完整目录还需要 `references/`、`assets/`、`scripts/`、`examples/`。**不要单独上传两个 Markdown 并要求 Agent 安装**，要保留整个 `listed-equity-research/` 目录。

## 方法 A：上传 ZIP + 解压（推荐）

将 `listed-equity-research-skill-v1.0.1.zip` 上传到具有文件操作能力的 Agent 环境，让它：

1. 解压 ZIP，保留最外层目录名 `listed-equity-research`。
2. 把整个目录移动到**目标 Agent 实际扫描的 skills 根目录**，不能只复制 `SKILL.md`。
3. 在目标目录下执行：`python scripts/verify_install.py .`。
4. 选做：`python scripts/self_test.py`，绘图测试需要 `matplotlib`。
5. 重启 Agent 会话或刷新技能索引（如果宿主需要）。

常见（不保证所有版本一致）的技能根目录：

| 宿主环境 | 常见安装位置 | 说明 |
| --- | --- | --- |
| Codex/Agent Skills | `~/.agents/skills/` 或项目下 `.agents/skills/` | 以当前宿主真实加载路径为准 |
| Claude Code | `~/.claude/skills/` 或项目下 `.claude/skills/` | 以宿主版本为准 |
| 其他兼容 Agent | 其配置指定的 skills 目录 | 不能盲猜路径 |

最终目录必须为：

```text
<SKILLS_ROOT>/
└── listed-equity-research/
    ├── SKILL.md
    ├── README.md
    ├── INSTALL.md
    ├── MANIFEST.json
    ├── references/  # 8 篇
    ├── assets/      # 数据和报告模板
    ├── scripts/     # 初始化、验证、图表、DCF/SOTP、自测
    └── examples/    # 研究案例
```

## 方法 B：一份单文件安装器

如果平台**只允许上传单个文件**，上传 `install_listed_equity_research.py`（独立文件，内嵌全部安装包），在目标 Agent 的本地终端运行：

```bash
python install_listed_equity_research.py --root ~/.agents/skills
# Claude Code 常见写法：
python install_listed_equity_research.py --root ~/.claude/skills
# 或安装到当前项目目录：
python install_listed_equity_research.py --root .agents/skills
```

Windows PowerShell 示例：

```powershell
py .\install_listed_equity_research.py --root "$HOME\.agents\skills"
```

安装器不会从互联网下载内容；会校验嵌入归档的 SHA-256、验证每个发行文件的 SHA-256；已存在的同名目录先做备份（不会直接删除）。

若宿主无 Python 或无法执行本地文件，应让有文件权限的管理员/用户将完整目录复制过去，不能靠语言模型声称已安装。

## 验证

```bash
cd <SKILLS_ROOT>/listed-equity-research
python scripts/verify_install.py .
python scripts/self_test.py
```

`self_test` 使用虚构演示数据，仅验证执行链路；不证明证券数据实时、投行报告可访问或模型决策级准确。

## 安装后调用

“使用 `listed-equity-research` 技能，分析港股 3690.HK，核查最近三年年报、最新中报、市场竞争、宏观传导、现金流并生成有原始出处链接和图表的研究报告；所有自建估值假设独立标记。”

## 依赖说明

`verify_install.py`、新建项目、来源核验和基础 DCF 计算仅需 Python 标准库；`render_charts.py` 需要 `matplotlib`；生成 DOCX/PDF/Excel 需要宿主具备对应工具。安装成功**不等于自动具备实时证券行情、付费研报或 Office 导出能力**。
