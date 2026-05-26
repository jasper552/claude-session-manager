# Claudex (Claude Session Manager)

Claude Code 会话管理器 - Web UI 版本（无需任何外部依赖）

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 为什么创建这个项目?
事情的起因是我把Claude Code 接入了第三方模型然后我发现会话就删不掉的问题
然后我就用Claude Code 做了这个项目就是这样

## 📋 简介
这是一个为 Claude Code 用户设计的会话管理工具，提供直观的 Web 界面来浏览、搜索和管理你的会话历史。它直接读取本地 Claude Code 的会话数据，无需任何外部依赖。

## 🚀 快速链接

- [中文 README](# Claude Session Manager)
- [English README](README_EN.md)

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

### 支持平台

| 平台 | 支持状态 | 备注 |
|------|----------|------|
| Windows | ✅ 完全支持 | 推荐使用发行版安装 |
| macOS | ✅ 完全支持 | 需要从源码构建 |
| Linux | ✅ 完全支持 | 需要从源码构建 |

### 方法一：从发行版安装（推荐，Windows）

1. 访问 [Releases 页面](https://github.com/jasper552/claude-session-manager/releases)
2. 下载最新版本的可执行文件
3. 双击运行 `Claudex.exe` 即可启动

### 方法二：从源码安装（所有平台）

#### Windows

1. 安装 Python 3.7 或更高版本
2. 下载项目到本地
3. 打开终端，进入项目目录
4. 运行以下命令：

```bash
python claude_session_manager.py
```

#### macOS

1. 安装 Python 3.7 或更高版本：
```bash
brew install python
```

2. 下载项目到本地
3. 打开终端，进入项目目录
4. 运行以下命令：

```bash
python3 claude_session_manager.py
```

#### Linux

1. 安装 Python 3.7 或更高版本：
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install python3

# CentOS/RHEL
sudo yum install python3
```

2. 下载项目到本地
3. 打开终端，进入项目目录
4. 运行以下命令：

```bash
python3 claude_session_manager.py
```

### 编译成可执行文件（可选）

如果你想将项目打包成独立的可执行文件，可以使用 PyInstaller。

#### 安装 PyInstaller

```bash
pip install pyinstaller
```

#### Windows 打包步骤

1. 安装 PyInstaller
2. 打开终端，进入项目目录
3. 运行以下命令：

```bash
pyinstaller --onefile --windowed --name "Claudex" claude_session_manager.py
```

4. 打包完成后，可执行文件位于 `dist/Claudex.exe`

#### macOS 打包步骤

1. 安装 PyInstaller：
```bash
pip install pyinstaller
```

2. 打开终端，进入项目目录
3. 运行以下命令：

```bash
pyinstaller --onefile --windowed --name "Claudex" claude_session_manager.py
```

4. 打包完成后，可执行文件位于 `dist/Claudex`

#### Linux 打包步骤

1. 安装 PyInstaller：
```bash
pip install pyinstaller
```

2. 打开终端，进入项目目录
3. 运行以下命令：

```bash
pyinstaller --onefile --windowed --name "Claudex" claude_session_manager.py
```

4. 打包完成后，可执行文件位于 `dist/Claudex`

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
├── README.md                  # 中文项目说明
└── README_EN.md               # English README
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

本项目由 AI 辅助生成，主要代码贡献者为 Claude Code。
欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE)。

## 🙏 致谢

- 使用了 [DM Sans](https://github.com/GoogleFonts/dm-fonts) 和 [JetBrains Mono](https://www.jetbrains.com/lp/mono/) 字体
- 主要代码由 Claude Code 生成。

---

**提示**：使用前请确保已关闭 Claude Code，以免数据冲突。
