# Claude Session Manager

Claude Code Session Manager - Web UI Version (No External Dependencies)

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📋 Introduction

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

### Requirements

- Python 3.7 or higher
- No additional dependencies required

### Running Steps

1. Download the project to your local machine
2. Open a terminal, navigate to the project directory
3. Run the following command:

```bash
python claude_session_manager.py
```

The program will automatically:
- Open the web interface in your browser
- Listen on port 18765 by default

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

Issues and Pull Requests are welcome!

## 📄 License

This project is licensed under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Uses [DM Sans](https://github.com/GoogleFonts/dm-fonts) and [JetBrains Mono](https://www.jetbrains.com/lp/mono/) fonts

---

**Note**: Make sure Claude Code is closed before using, to avoid data conflicts.

---

## Quick Links

- [中文 README](README.md)
- [English README](README_EN.md)