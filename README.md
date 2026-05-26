# Claude Session Manager

Claude Code 会话管理器 - Web UI 版本（无需任何外部依赖）

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📋 简介

这是一个为 Claude Code 用户设计的会话管理工具，提供直观的 Web 界面来浏览、搜索和管理你的会话历史。它直接读取本地 Claude Code 的会话数据，无需任何外部依赖。

## ✨ 功能特性

- 📊 **数据可视化**：以卡片和表格的形式展示所有会话
- 🔍 **实时搜索**：按标题和首条消息内容搜索会话
- 🏷️ **状态筛选**：按活跃/已归档状态过滤
- ✅ **批量操作**：支持批量删除会话
- 🔄 **一键刷新**：实时更新会话列表
- 🚀 **自动重启**：删除会话后自动重启 Claude Code

## 🛠️ 技术栈

- Python 3.7+
- 原生 HTTP 服务器（无外部依赖）
- 纯 HTML/CSS/JavaScript（无前端框架）

## 📦 安装与运行

### 环境要求

- Python 3.7 或更高版本
- 无需安装任何额外依赖

### 运行步骤

1. 下载项目到本地
2. 打开终端，进入项目目录
3. 运行以下命令：

```bash
python claude_session_manager.py
```

程序会自动：
- 在浏览器中打开 Web 界面
- 默认监听端口：18765

## 💻 使用说明

### 界面导航

- **侧边栏**：
  - 查看会话统计（全部/活跃/已归档）
  - 刷新列表
  - 删除选中/全部会话

- **主区域**：
  - 搜索会话
  - 选择要删除的会话
  - 查看会话详情

### 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| `Delete` | 删除选中的会话 |
| `F5` | 刷新会话列表 |
| `Ctrl+A` | 全选所有会话 |
| `Esc` | 关闭弹窗 |

### 操作说明

1. **删除单个会话**：点击会话行前的复选框，然后点击"删除选中"按钮
2. **删除多个会话**：按住 `Ctrl` 键点击多个复选框，然后点击"删除选中"
3. **清空全部**：点击"清空全部"按钮删除所有可见的会话

## 🗂️ 项目结构

```
.
├── claude_session_manager.py  # 主程序文件
├── LICENSE                    # MIT 许可证
└── README.md                  # 项目说明
```

## 🔧 工作原理

程序读取本地 Claude Code 会话数据目录：
```
C:\Users\Administrator\AppData\Local\Claude-3p\local-agent-mode-sessions\
{project-id}\{session-id}\
```

从每个会话的 JSON 文件和 audit.jsonl 中提取以下信息：
- 会话标题
- 首条消息内容
- 最后活动时间
- 使用的模型
- 用户/助手消息数量

## ⚠️ 注意事项

1. **数据安全**：本工具直接读取本地数据，不会上传任何信息到网络
2. **不可逆操作**：删除操作将同时删除 JSON 文件和对应文件夹，无法恢复
3. **路径配置**：当前配置针对特定的 Claude Code 安装路径

## 📝 开发说明

### 修改会话路径

如需修改会话数据路径，请编辑 `claude_session_manager.py` 文件第 9-14 行的 `SESSION_DIR` 变量。

### 添加新功能

项目采用模块化设计：
- 数据层：`load_sessions()`, `delete_sessions()`, `restart_claude()`
- 服务器层：`Handler` 类
- 展示层：内嵌的 HTML/JavaScript

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE)。

## 🙏 致谢

- 使用了 [DM Sans](https://github.com/GoogleFonts/dm-fonts) 和 [JetBrains Mono](https://www.jetbrains.com/lp/mono/) 字体

---

**提示**：使用前请确保已关闭 Claude Code，以免数据冲突。