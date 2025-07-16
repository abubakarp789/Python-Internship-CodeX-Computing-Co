# File Transfer Assistant

A professional-grade file transfer application for Windows that simplifies file transfers to external storage devices with advanced features and safeguards.

![File Transfer Assistant Screenshot](screenshot.png)

## ✨ Features

- 🚀 Automatic external drive detection
- 📁 Smart file and folder selection with filtering
- ⚡ Background file transfers with threading
- 📊 Real-time progress tracking
- ⏯️ Pause/Resume transfers
- 🛡️ Safety features (overwrite protection, checksum verification)
- 🎨 Modern, user-friendly interface with light/dark theme support
- ⚙️ Comprehensive settings and preferences
- 🔔 Customizable notifications
- 📁 Preserve folder structure during transfers
- 🔍 Advanced file filtering (type, size, date)

## 🛠️ Requirements

- **Operating System**: Windows 10/11
- **Python**: 3.9 or higher
- **Dependencies**: See [requirements.txt](requirements.txt)

## 🚀 Installation Guide

### Method 1: Using Git (Recommended)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/FileTransferAssistant.git
   cd FileTransferAssistant
   ```

2. **Create and activate a virtual environment** (recommended):
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # Windows Command Prompt:
   venv\Scripts\activate
   # Windows PowerShell:
   # .\venv\Scripts\Activate.ps1
   # Linux/macOS:
   # source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Method 2: Direct Installation

1. **Download the latest release** from the [Releases](https://github.com/yourusername/FileTransferAssistant/releases) page.
2. **Extract the ZIP file** to your preferred location.
3. **Run the application**:
   - Double-click `FileTransferAssistant.exe` (if using the pre-built executable)
   - Or run `python -m src` from the command line

## ⚙️ Settings & Configuration

The application includes a comprehensive settings dialog where you can customize various aspects:

### Source Folders
- Set default source folders for quick access
- Manage up to 3 frequently used folders

### File Filters
- Filter by file types (extensions)
- Set size limits for transfers
- Filter files by modification date

### Transfer Behavior
- Choose whether to preserve folder structure
- Set conflict resolution preferences
- Enable/disable checksum verification

### Notifications
- Toggle popup notifications
- Enable/disable system tray notifications
- Sound alerts for completed transfers

### Appearance
- Toggle between light and dark themes
- Customize UI scaling (coming soon)

## 📝 Usage

1. **Select Source**: Choose files/folders to transfer
2. **Select Destination**: Pick the target external device
3. **Configure Transfer Options** (optional):
   - Apply filters
   - Set transfer speed limits (coming soon)
   - Choose conflict resolution method
4. **Start Transfer**: Click the transfer button
5. **Monitor Progress**: View real-time transfer statistics

## 🛠️ Development

### Running Tests
```bash
pytest tests/
```

### Code Style
We use Black for code formatting and Flake8 for linting:
```bash
black .
flake8
```

### Building Executable
To create a standalone executable:
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=assets/icon.ico src/__main__.py --name FileTransferAssistant
```

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

4. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Method 2: Direct Download

1. Download the source code as a ZIP file and extract it
2. Open a command prompt in the extracted folder
3. Follow steps 2-4 from Method 1

## 🖥️ Running the Application

### Option 1: Using run.py (Recommended)

```bash
python run.py
```

### Option 2: Using Python module

```bash
python -m src.main
```

### Option 3: Install and Run (Development Mode)

1. Install the package in development mode:
   ```bash
   pip install -e .
   ```

2. Run the application:
   ```bash
   file-transfer-assistant
   ```

## 📦 Building a Standalone Executable

To create a single executable file for distribution:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Build the executable:
   ```bash
   pyinstaller --onefile --windowed --name FileTransferAssistant run.py
   ```

3. The executable will be created in the `dist` directory.

## 🎮 How to Use

1. **Select Source Files/Folders**:
   - Click "Add Files" to select individual files
   - Click "Add Folder" to add an entire folder
   - Use the quick access panel for common locations

2. **Choose Destination**:
   - Select the destination drive from the dropdown
   - Click "Browse" to choose a specific folder

3. **Start Transfer**:
   - Click "Start" to begin the transfer
   - Use "Pause/Resume" to control the transfer
   - Click "Cancel" to stop the transfer

## 🔧 Troubleshooting

- **Missing Dependencies**:
  ```bash
  pip install -r requirements.txt
  ```

- **Permission Errors**:
  - Run the application as Administrator
  - Ensure you have write permissions to the destination

- **External Drives Not Detected**:
  - Ensure the drive is properly connected
  - Try refreshing the drive list

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
   .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python src/main.py
```

## Configuration

Application settings are stored in `config/settings.json`. The file will be created automatically with default values on first run.

## License

MIT License - Feel free to use and modify as needed.
