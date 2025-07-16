# File Transfer Assistant

A professional desktop application for Windows that simplifies file transfers to external storage devices with advanced features and robust error handling. Built with Python and PySide6, this application provides a modern, user-friendly interface for managing file transfers efficiently.

## ✨ Features

### Core Functionality
- 🚀 **Automatic Drive Detection**: Automatically detects and lists available external drives
- 📁 **Intelligent File Selection**: Add individual files or entire folders with recursive directory support
- ⚡ **Background Processing**: Multi-threaded transfers to keep the UI responsive
- 📊 **Real-time Progress Tracking**: Visual feedback with progress bars and transfer statistics
- ⏯️ **Transfer Control**: Pause, resume, or cancel transfers at any time

### Safety & Reliability
- 🛡️ **Data Integrity**: Optional checksum verification to ensure file integrity
- 🔄 **Conflict Resolution**: Smart handling of file name conflicts
- 📝 **Logging**: Detailed transfer logs for troubleshooting
- 🔒 **Error Recovery**: Resume interrupted transfers from the point of failure

### User Experience
- 🎨 **Themes**: Built-in light and dark mode support
- ⚙️ **Customizable Settings**: Configure transfer behavior and UI preferences
- 🔍 **Advanced Filtering**: Filter files by type, size, or modification date
- 📁 **Preserve Structure**: Maintain folder hierarchy during transfers
- 🗂️ **Quick Access**: Save frequently used source and destination folders

## 🛠️ System Requirements

- **Operating System**: Windows 10/11 (64-bit)
- **Python**: 3.9 or higher
- **Disk Space**: 50MB free space
- **Memory**: 4GB RAM recommended

## 🚀 Getting Started

### Prerequisites

1. Install Python 3.9 or higher from [python.org](https://www.python.org/downloads/)
2. Ensure pip is up to date:
   ```bash
   python -m pip install --upgrade pip
   ```

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/abubakarp789/Python-Internship-CodeX-Computing-Co.git
   cd Python-Internship-CodeX-Computing-Co/FileTransferAssistant
   ```

2. **Set up a virtual environment** (recommended):
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **From source**:
   ```bash
   python -m src
   ```

2. **Or using the entry point**:
   ```bash
   python run.py
   ```

## 🖥️ User Guide

### Main Interface

1. **Source Panel** (Left)
   - Add files/folders using the toolbar buttons
   - View and manage files in the transfer queue
   - Remove items or clear the entire list

2. **Destination Panel** (Right)
   - Select target drive from the dropdown
   - Browse to a specific folder
   - View available space information

3. **Transfer Controls** (Bottom)
   - Start/Pause/Resume/Cancel transfers
   - View progress and transfer speed
   - Access transfer history and logs

### Common Operations

#### Adding Files/Folders
1. Click the "Add Files" or "Add Folder" button
2. Select the items you want to transfer
3. Use filters to include/exclude specific file types if needed

#### Starting a Transfer
1. Select the destination drive/folder
2. Review the file list
3. Click the "Start Transfer" button
4. Monitor progress in the transfer log

#### Pausing/Resuming
- Click the pause button to temporarily stop transfers
- Click resume to continue from where you left off

## ⚙️ Configuration

### Settings Dialog
Access the settings dialog from the menu: `Settings > Preferences`

#### Transfer Settings
- **Verify Transfers**: Enable checksum verification
- **Preserve Timestamps**: Keep original file timestamps
- **Conflict Resolution**: Choose what to do when files exist

#### Interface Settings
- **Theme**: Light/Dark mode
- **Language**: Application language
- **Notifications**: Configure desktop notifications

### Keyboard Shortcuts
- `Ctrl+O`: Add files
- `Ctrl+D`: Add folder
- `Delete`: Remove selected items
- `F5`: Refresh drive list
- `F1`: Show help

## 🐛 Troubleshooting

### Common Issues

#### Application won't start
- Ensure all dependencies are installed
- Check Python version (3.9+ required)
- Run as administrator if experiencing permission issues

#### Transfers are slow
- Try disabling checksum verification for large transfers
- Check for disk I/O bottlenecks
- Close other disk-intensive applications

### Viewing Logs
Application logs are stored in:
```
%APPDATA%\FileTransferAssistant\file_transfer.log
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Abu Bakar**  
Python Developer | CodeX Computing Co. Intern  
[GitHub](https://github.com/abubakarp789) | [LinkedIn](https://www.linkedin.com/in/abubakar56/) | [Portfolio](https://abubakar056.netlify.app/)

---
*Part of the Python Internship Program at CodeX Computing Co.*