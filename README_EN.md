# Claudex (Claude Session Manager)

Claude Code Session Manager - Web UI Version (No External Dependencies)

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🚀 Quick Links

- [中文 README](README.md)
- [English README](# Claudex (Claude Session Manager))

##  Introduction

A session management tool designed for Claude Code users, providing an intuitive web interface to browse, search, and manage your conversation history. It directly reads local Claude Code session data without any external dependencies.

## ✨ Features

- 📊 **Data Visualization**: Display all sessions with cards and tables
- 🔍 **Real-time Search**: Search by title and first message content
- 🏷️ **Status Filtering**: Filter by active/archived status
- ✅ **Batch Operations**: Support batch deletion of sessions
- 🔄 **One-click Refresh**: Update session list in real-time
- 🚀 **Auto Restart**: Automatically restart Claude Code after deletion

## 🛠️ Tech Stack

- Python 3.7+
- Built-in HTTP Server (No External Dependencies)
- Pure HTML/CSS/JavaScript (No Frontend Framework)

## 📦 Installation & Running

### Supported Platforms

| Platform | Support Status | Notes |
|----------|----------------|-------|
| Windows | ✅ Full Support | Recommended for release installation |
| macOS | ✅ Full Support | Requires building from source |
| Linux | ✅ Full Support | Requires building from source |

### Method 1: Install from Release (Recommended, Windows)

1. Visit the [Releases page](https://github.com/jasper552/claude-session-manager/releases)
2. Download the latest executable
3. Double-click `Claudex.exe` to launch

### Method 2: Install from Source (All Platforms)

#### Windows

1. Install Python 3.7 or higher
2. Download the project locally
3. Open a terminal and navigate to the project directory
4. Run the following command:

```bash
python claude_session_manager.py
```

#### macOS

1. Install Python 3.7 or higher:
```bash
brew install python
```

2. Download the project locally
3. Open a terminal and navigate to the project directory
4. Run the following command:

```bash
python3 claude_session_manager.py
```

#### Linux

1. Install Python 3.7 or higher:
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install python3

# CentOS/RHEL
sudo yum install python3
```

2. Download the project locally
3. Open a terminal and navigate to the project directory
4. Run the following command:

```bash
python3 claude_session_manager.py
```

### Compile to Executable (Optional)

If you want to package the project into a standalone executable, you can use PyInstaller.

#### Install PyInstaller

```bash
pip install pyinstaller
```

#### Windows Packaging Steps

1. Install PyInstaller
2. Open a terminal and navigate to the project directory
3. Run the following command:

```bash
pyinstaller --onefile --windowed --name "Claudex" claude_session_manager.py
```

4. After packaging, the executable will be in `dist/Claudex.exe`

#### macOS Packaging Steps

1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Open a terminal and navigate to the project directory
3. Run the following command:

```bash
pyinstaller --onefile --windowed --name "Claudex" claude_session_manager.py
```

4. After packaging, the executable will be in `dist/Claudex`

#### Linux Packaging Steps

1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Open a terminal and navigate to the project directory
3. Run the following command:

```bash
pyinstaller --onefile --windowed --name "Claudex" claude_session_manager.py
```

4. After packaging, the executable will be in `dist/Claudex`

## 💻 Usage Instructions

### Interface Navigation

- **Sidebar**:
  - View session statistics (All/Active/Archived)
  - Refresh list
  - Delete selected/all sessions

- **Main Area**:
  - Search sessions
  - Select sessions to delete
  - View session details

### Keyboard Shortcuts

| Shortcut | Function |
|----------|----------|
| `Delete` | Delete selected sessions |
| `F5` | Refresh session list |
| `Ctrl+A` | Select all sessions |
| `Esc` | Close modal |

### Operations

1. **Delete single session**: Click the checkbox before the session row, then click "Delete Selected"
2. **Delete multiple sessions**: Hold `Ctrl` key and click multiple checkboxes, then click "Delete Selected"
3. **Clear all**: Click "Clear All" button to delete all visible sessions

## 🗂️ Project Structure

```
.
├── claude_session_manager.py  # Main program file
├── LICENSE                    # MIT License
├── README.md                  # Project README (Chinese)
└── README_EN.md               # Project README (English)
```

## 🔧 How It Works

The program reads local Claude Code session data from:
```
C:\Users\Administrator\AppData\Local\Claude-3p\local-agent-mode-sessions\
{project-id}\{session-id}\
```

Extracts the following information from each session's JSON file and audit.jsonl:
- Session title
- First message content
- Last activity time
- Model used
- User/Assistant message count

## ⚠️ Notes

1. **Data Security**: This tool reads local data only, no information is uploaded to the network
2. **Irreversible Operations**: Deletion will permanently remove JSON files and associated folders
3. **Path Configuration**: Current configuration targets a specific Claude Code installation path

## 📝 Development Notes

### Modifying Session Path

To modify the session data path, edit the `SESSION_DIR` variable in `claude_session_manager.py` lines 9-14.

### Adding New Features

The project uses a modular design:
- Data Layer: `load_sessions()`, `delete_sessions()`, `restart_claude()`
- Server Layer: `Handler` class
- Presentation Layer: Embedded HTML/JavaScript

## 🤝 Contributing

This project is AI-assisted, with Claude Code as the primary code contributor.
Issues and Pull Requests are welcome!

## 📄 License

This project is licensed under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Uses [DM Sans](https://github.com/GoogleFonts/dm-fonts) and [JetBrains Mono](https://www.jetbrains.com/lp/mono/) fonts
- Primary code generated by Claude Code.

---

**Note**: Make sure Claude Code is closed before using, to avoid data conflicts.


