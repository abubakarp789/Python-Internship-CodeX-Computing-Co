import os
import sys
import shutil
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QListWidget, QComboBox, QCheckBox,
    QProgressBar, QFileDialog, QMessageBox, QSplitter, QFrame,
    QSizePolicy, QMenuBar, QToolBar, QStyle, QListWidgetItem,
    QStatusBar, QFormLayout, QLineEdit, QInputDialog, QGroupBox
)
from PySide6.QtCore import Qt, QSize, QTimer, QThread, Signal, QObject
from PySide6.QtGui import QIcon, QFont, QAction

from src.config import Config, ConfigManager
from src.utils.drive_detector import DriveDetector

# Import TransferManager if it exists, otherwise define a dummy class
try:
    from src.transfer.manager import TransferManager
except ImportError:
    class TransferManager:
        def __init__(self):
            pass


class TransferSignals(QObject):
    """Signals for the transfer worker thread."""
    progress = Signal(int, int)  # current, total
    finished = Signal()
    error = Signal(str)
    file_started = Signal(str)
    file_completed = Signal(str)


class TransferWorker(QThread):
    """Worker thread for handling file transfers."""
    def __init__(self, files, destination):
        super().__init__()
        self.files = files  # List of (src, dest) tuples
        self.destination = destination
        self.signals = TransferSignals()
        self._is_paused = False
        self._is_canceled = False
        self._lock = False
    
    def run(self):
        """Run the file transfer process."""
        try:
            total_files = len(self.files)
            
            for i, (src, dest) in enumerate(self.files):
                if self._is_canceled:
                    break
                
                # Wait if paused
                while self._is_paused and not self._is_canceled:
                    self.msleep(100)
                
                if self._is_canceled:
                    break
                
                try:
                    # Emit file started signal
                    self.signals.file_started.emit(os.path.basename(src))
                    
                    # Ensure destination directory exists
                    os.makedirs(os.path.dirname(dest), exist_ok=True)
                    
                    # Copy file
                    shutil.copy2(src, dest)
                    
                    # Emit progress and completion signals
                    self.signals.progress.emit(100, 0)  # 100% for current file
                    self.signals.file_completed.emit(os.path.basename(src))
                    
                    # Update overall progress
                    progress = int((i + 1) / total_files * 100)
                    self.signals.progress.emit(progress, 1)  # 1 indicates overall progress
                    
                except Exception as e:
                    self.signals.error.emit(f"Error transferring {src}: {str(e)}")
            
            if not self._is_canceled:
                self.signals.finished.emit()
                
        except Exception as e:
            self.signals.error.emit(f"Transfer failed: {str(e)}")
    
    def pause(self):
        """Pause the transfer."""
        self._is_paused = True
    
    def resume(self):
        """Resume the transfer."""
        self._is_paused = False
    
    def stop(self):
        """Stop the transfer."""
        self._is_canceled = True

class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self, config=None):
        """Initialize the main window."""
        super().__init__()
        
        # Initialize config with a proper filename if not provided
        if config is None:
            self.config = ConfigManager()  # ConfigManager handles the default path
        else:
            self.config = config
            
        self.transfer_manager = TransferManager()  # Initialize the transfer manager
        self.drive_detector = DriveDetector()
        self.settings_dialog = None

        self.transfer_worker = None
        self.transfer_files = []
        
        # Apply theme before setting up UI
        self.apply_theme()
        
        self.setup_ui()
        self.setup_connections()
        self.update_drive_list()
        
        # Start drive monitoring
        self.drive_timer = QTimer(self)
        self.drive_timer.timeout.connect(self.update_drive_list)
        self.drive_timer.start(5000)  # Check every 5 seconds
        
        # Load saved settings
        self.load_settings()
        
        # Apply initial settings
        self.apply_initial_settings()
        
    def apply_theme(self, theme_name=None):
        """Apply the specified theme or use the one from config."""
        from PySide6.QtGui import QPalette, QColor
        from PySide6.QtCore import Qt
        
        theme = theme_name or self.config.get('appearance/theme', 'system')
        
        # Set the application style to Fusion for consistent theming
        QApplication.setStyle('Fusion')
        
        palette = QPalette()
        
        if theme == 'dark' or (theme == 'system' and QPalette().color(QPalette.Window).lightness() < 128):
            # Dark theme
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.HighlightedText, Qt.black)
        else:
            # Light theme (default)
            palette = QPalette()  # Reset to default palette
            
        QApplication.setPalette(palette)
    
    def setup_ui(self):
        """Set up the user interface."""
        self.setWindowTitle("File Transfer Assistant")
        self.setMinimumSize(800, 600)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create toolbar
        self.create_toolbar()
        
        # Create main content area
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)
        
        # Left panel - Source
        left_panel = QVBoxLayout()
        content_layout.addLayout(left_panel, stretch=2)
        
        # Initialize all UI elements
        self._init_source_ui(left_panel)
        self._init_destination_ui(content_layout)
        self._init_transfer_ui(main_layout)
        
        # Set up connections
        self._setup_ui_connections()
    
    def _init_source_ui(self, parent_layout):
        """Initialize source-related UI elements."""
        # Source group
        source_group = QGroupBox("Source")
        source_layout = QVBoxLayout()
        
        # Source path
        source_path_layout = QHBoxLayout()
        self.source_path_edit = QLineEdit()
        self.source_path_edit.setReadOnly(True)
        self.browse_source_btn = QPushButton("Browse...")
        
        source_path_layout.addWidget(QLabel("Folder:"))
        source_path_layout.addWidget(self.source_path_edit, 1)
        source_path_layout.addWidget(self.browse_source_btn)
        
        source_layout.addLayout(source_path_layout)
        
        # Quick access buttons
        self.quick_access_layout = QHBoxLayout()
        self.update_quick_access_buttons()
        
        source_layout.addLayout(self.quick_access_layout)
        
        # File actions
        file_actions = QHBoxLayout()
        
        self.add_files_btn = QPushButton("Add Files")
        self.add_folder_btn = QPushButton("Add Folder")
        self.remove_btn = QPushButton("Remove")
        self.clear_btn = QPushButton("Clear All")
        
        file_actions.addWidget(self.add_files_btn)
        file_actions.addWidget(self.add_folder_btn)
        file_actions.addWidget(self.remove_btn)
        file_actions.addWidget(self.clear_btn)
        
        source_layout.addLayout(file_actions)
        
        # File list
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.ExtendedSelection)
        source_layout.addWidget(self.file_list)
        
        source_group.setLayout(source_layout)
        parent_layout.addWidget(source_group)
    
    def _init_destination_ui(self, parent_layout):
        """Initialize destination-related UI elements."""
        # Right panel - Destination and options
        right_panel = QVBoxLayout()
        parent_layout.addLayout(right_panel, stretch=1)
        
        # Destination group
        dest_group = QGroupBox("Destination")
        dest_layout = QVBoxLayout()
        
        # Drive selection
        self.drive_combo = QComboBox()
        
        # Destination path
        dest_path_layout = QHBoxLayout()
        self.dest_path_edit = QLineEdit()
        self.dest_path_edit.setReadOnly(True)
        self.browse_dest_btn = QPushButton("Browse...")
        
        dest_path_layout.addWidget(QLabel("Path:"))
        dest_path_layout.addWidget(self.dest_path_edit, 1)
        dest_path_layout.addWidget(self.browse_dest_btn)
        
        dest_layout.addWidget(QLabel("Drive:"))
        dest_layout.addWidget(self.drive_combo)
        dest_layout.addLayout(dest_path_layout)
        
        # Refresh button
        self.refresh_drives_btn = QPushButton("Refresh Drives")
        dest_layout.addWidget(self.refresh_drives_btn)
        
        dest_group.setLayout(dest_layout)
        right_panel.addWidget(dest_group)
        
        # Transfer options group
        options_group = QGroupBox("Transfer Options")
        options_layout = QVBoxLayout()
        
        # Overwrite policy
        self.overwrite_combo = QComboBox()
        self.overwrite_combo.addItems(["Ask", "Overwrite", "Skip", "Rename"])
        
        # Checkboxes
        self.verify_cb = QCheckBox("Verify after transfer")
        self.preserve_cb = QCheckBox("Preserve folder structure")
        
        options_layout.addWidget(QLabel("If file exists:"))
        options_layout.addWidget(self.overwrite_combo)
        options_layout.addWidget(self.verify_cb)
        options_layout.addWidget(self.preserve_cb)
        options_group.setLayout(options_layout)
        right_panel.addWidget(options_group)
    
    def _init_transfer_ui(self, parent_layout):
        """Initialize transfer-related UI elements."""
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("Ready")
        parent_layout.addWidget(self.progress_bar)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.transfer_btn = QPushButton("Start Transfer")
        self.pause_btn = QPushButton("Pause")
        self.pause_btn.setEnabled(False)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setEnabled(False)
        
        button_layout.addWidget(self.transfer_btn)
        button_layout.addWidget(self.pause_btn)
        button_layout.addWidget(self.cancel_btn)
        
        parent_layout.addLayout(button_layout)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
    
    def _setup_ui_connections(self):
        """Set up all UI signal/slot connections."""
        # Source buttons
        self.browse_source_btn.clicked.connect(self.browse_source)
        self.add_files_btn.clicked.connect(self.add_files)
        self.add_folder_btn.clicked.connect(self.add_folder)
        self.remove_btn.clicked.connect(self.remove_selected)
        self.clear_btn.clicked.connect(self.clear_files)
        
        # Destination buttons
        self.browse_dest_btn.clicked.connect(self.browse_destination)
        self.refresh_drives_btn.clicked.connect(self.update_drive_list)
        self.drive_combo.currentIndexChanged.connect(self.update_destination_path)
        
        # Transfer buttons
        self.transfer_btn.clicked.connect(self.start_transfer)
        self.pause_btn.clicked.connect(self.toggle_pause)
        self.cancel_btn.clicked.connect(self.cancel_transfer)
    
    def create_menu_bar(self):
        """Create the menu bar."""
        menubar = self.menuBar()
            
        # File menu
        file_menu = menubar.addMenu("&File")
            
        new_action = QAction("&New Transfer", self)
        new_action.triggered.connect(self.new_transfer)
        new_action.setShortcut("Ctrl+N")
        file_menu.addAction(new_action)
            
        file_menu.addSeparator()
            
        # Recent sources submenu
        self.recent_sources_menu = file_menu.addMenu("Recent Sources")
        self.update_recent_sources_menu()
            
        # Recent destinations submenu
        self.recent_destinations_menu = file_menu.addMenu("Recent Destinations")
        self.update_recent_destinations_menu()
            
        file_menu.addSeparator()
            
        exit_action = QAction("E&xit", self)
        exit_action.triggered.connect(self.close)
        exit_action.setShortcut("Alt+F4")
        file_menu.addAction(exit_action)
            
        # Edit menu
        edit_menu = menubar.addMenu("&Edit")
            
        settings_action = QAction("&Settings...", self)
        settings_action.triggered.connect(self.show_settings)
        settings_action.setShortcut("Ctrl+,")
        edit_menu.addAction(settings_action)
            
        # View menu
        view_menu = menubar.addMenu("&View")
            
        self.toolbar_toggle = QAction("&Toolbar", self, checkable=True)
        self.toolbar_toggle.setChecked(True)
        self.toolbar_toggle.triggered.connect(self.toggle_toolbar)
        view_menu.addAction(self.toolbar_toggle)
            
        view_menu.addSeparator()
            
        self.statusbar_toggle = QAction("Status &Bar", self, checkable=True)
        self.statusbar_toggle.setChecked(True)
        self.statusbar_toggle.triggered.connect(self.toggle_statusbar)
        view_menu.addAction(self.statusbar_toggle)
            
        # Help menu
        help_menu = menubar.addMenu("&Help")
            
        docs_action = QAction("&Documentation", self)
        docs_action.triggered.connect(self.show_documentation)
        help_menu.addAction(docs_action)
            
        help_menu.addSeparator()
            
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_toolbar(self):
        """Create the toolbar."""
        toolbar = self.addToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(24, 24))
            
        # Add files action
        add_files_action = QAction(
            self.style().standardIcon(getattr(QStyle, 'SP_FileIcon')),
            "Add Files",
            self
        )
        add_files_action.triggered.connect(self.add_files)
        toolbar.addAction(add_files_action)
            
        # Add folder action
        add_folder_action = QAction(
            self.style().standardIcon(getattr(QStyle, 'SP_DirIcon')),
            "Add Folder",
            self
        )
        add_folder_action.triggered.connect(self.add_folder)
        toolbar.addAction(add_folder_action)
            
        toolbar.addSeparator()
            
        # Start transfer action
        self.start_action = QAction(
            self.style().standardIcon(getattr(QStyle, 'SP_MediaPlay')),
            "Start Transfer",
            self
        )
        self.start_action.triggered.connect(self.start_transfer)
        toolbar.addAction(self.start_action)
            
        # Pause transfer action
        self.pause_action = QAction(
            self.style().standardIcon(getattr(QStyle, 'SP_MediaPause')),
            "Pause",
            self
        )
        self.pause_action.triggered.connect(self.toggle_pause)
        self.pause_action.setEnabled(False)
        toolbar.addAction(self.pause_action)
            
        # Cancel transfer action
        self.cancel_action = QAction(
            self.style().standardIcon(getattr(QStyle, 'SP_DialogCancelButton')),
            "Cancel",
            self
        )
        self.cancel_action.triggered.connect(self.cancel_transfer)
        self.cancel_action.setEnabled(False)
        toolbar.addAction(self.cancel_action)
    
    def load_settings(self):
        """Load application settings."""
        # Load window geometry and state from base64 strings
        geometry_data = self.config.get('window/geometry')
        if geometry_data:
            try:
                from PySide6.QtCore import QByteArray
                geometry_bytes = QByteArray.fromBase64(geometry_data.encode())
                if not geometry_bytes.isEmpty():
                    self.restoreGeometry(geometry_bytes)
            except Exception as e:
                print(f"Error restoring window geometry: {e}")
            
        # Load transfer options
        self.overwrite_combo.setCurrentText(
            self.config.get('transfer/overwrite_policy', 'Ask'))
        self.verify_cb.setChecked(
            self.config.get('transfer/verify', False))
        self.preserve_cb.setChecked(
            self.config.get('transfer/preserve_structure', True))
        
        # Update recent sources and destinations
        self.update_recent_sources_menu()
        self.update_recent_destinations_menu()
    
    def create_toolbar(self):
        """Create the toolbar."""
        toolbar = self.addToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(24, 24))
        
        # Add files action
        add_files_action = QAction(
            self.style().standardIcon(getattr(QStyle, 'SP_FileIcon')),
            "Add Files",
            self
        )
        add_files_action.triggered.connect(self.add_files)
        toolbar.addAction(add_files_action)
        
        # Add folder action
        add_folder_action = QAction(
            self.style().standardIcon(getattr(QStyle, 'SP_DirIcon')),
            "Add Folder",
            self
        )
        add_folder_action.triggered.connect(self.add_folder)
        toolbar.addAction(add_folder_action)
        
        toolbar.addSeparator()
        
        # Start transfer action
        self.start_action = QAction(
            self.style().standardIcon(getattr(QStyle, 'SP_MediaPlay')),
            "Start Transfer",
            self
        )
        self.start_action.triggered.connect(self.start_transfer)
        toolbar.addAction(self.start_action)
        
        # Pause transfer action
        self.pause_action = QAction(
            self.style().standardIcon(getattr(QStyle, 'SP_MediaPause')),
            "Pause",
            self
        )
        self.pause_action.triggered.connect(self.toggle_pause)
        self.pause_action.setEnabled(False)
        toolbar.addAction(self.pause_action)
        
        # Cancel transfer action
        self.cancel_action = QAction(
            self.style().standardIcon(getattr(QStyle, 'SP_DialogCancelButton')),
            "Cancel",
            self
        )
        self.cancel_action.triggered.connect(self.cancel_transfer)
        self.cancel_action.setEnabled(False)
        toolbar.addAction(self.cancel_action)
    
    def setup_connections(self):
        """Set up signal/slot connections."""
        # Setup will be done in the setup_ui method
        pass
    
    def load_settings(self):
        """Load application settings."""
        # Load window geometry and state from base64 strings
        geometry_data = self.config.get('window/geometry')
        if geometry_data:
            from PySide6.QtCore import QByteArray
            geometry = QByteArray.fromBase64(geometry_data.encode())
            self.restoreGeometry(geometry)
        
        # Load transfer options
        self.overwrite_combo.setCurrentText(
            self.config.get('transfer/overwrite_policy', 'Ask'))
        self.verify_cb.setChecked(
            self.config.get('transfer/verify', False))
        self.preserve_cb.setChecked(
            self.config.get('transfer/preserve_structure', True))
            
        # Apply theme from settings
        self.apply_theme()
    
    def save_settings(self):
        """Save application settings."""
        # Save window geometry and state as base64 strings
        geometry = self.saveGeometry()
        if geometry:
            self.config.set('window/geometry', geometry.toBase64().data().decode())
        
        # Save transfer options
        self.config.set('transfer/overwrite_policy', 
                       self.overwrite_combo.currentText())
        self.config.set('transfer/verify', 
                       self.verify_cb.isChecked())
        self.config.set('transfer/preserve_structure', 
                       self.preserve_cb.isChecked())
    
    def closeEvent(self, event):
        """Handle window close event."""
        if self.transfer_worker and self.transfer_worker.isRunning():
            reply = QMessageBox.question(
                self, 'Transfer in Progress',
                'A file transfer is in progress. Are you sure you want to quit?',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            if reply == QMessageBox.No:
                event.ignore()
                return
        
        self.save_settings()
        event.accept()
    
    def update_drive_list(self):
        """Update the list of available drives."""
        current_drive = self.drive_combo.currentText()
        self.drive_combo.clear()
        
        # Get all external drives using the drive detector
        drives = self.drive_detector.get_external_drives()
        
        # Add drives to combo box
        for drive in drives:
            # Get the drive letter from the device path (e.g., 'C:' from 'C:\\')
            drive_letter = drive['device'][:2]  # Gets the first two characters (e.g., 'C:')
            self.drive_combo.addItem(drive_letter)
        
        # Restore previous selection if still available
        index = self.drive_combo.findText(current_drive)
        if index >= 0:
            self.drive_combo.setCurrentIndex(index)
    
    def update_destination_path(self):
        """Update the destination path when drive changes."""
        drive = self.drive_combo.currentText()
        if drive:
            self.dest_path_edit.setText(drive)
    
    def set_source_folder(self, folder_name):
        """Set the source folder from quick selection."""
        if folder_name == "Desktop":
            path = str(Path.home() / "Desktop")
        elif folder_name == "Documents":
            path = str(Path.home() / "Documents")
        elif folder_name == "Downloads":
            path = str(Path.home() / "Downloads")
        else:
            path = str(Path.home())
        
        self.source_path_edit.setText(path)
    
    def browse_source(self):
        """Open a file dialog to select source files."""
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select Files", "", "All Files (*.*)")
        
        if files:
            self.source_path_edit.setText(", ".join(files))
            self.add_files_to_list(files)
    
    def add_files(self):
        """Add files to the transfer list."""
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select Files", "", "All Files (*.*)")
        
        if files:
            self.add_files_to_list(files)
    
    def add_folder(self):
        """Add a folder to the transfer list."""
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        
        if folder:
            self.source_path_edit.setText(folder)
            self.add_folder_to_list(folder)
    
    def add_files_to_list(self, files):
        """Add files to the file list."""
        for file in files:
            if not self.is_file_in_list(file):
                item = QListWidgetItem(file)
                item.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_FileIcon')))
                self.file_list.addItem(item)
                self.transfer_files.append((file, ''))  # Destination will be set later
    
    def add_folder_to_list(self, folder):
        """Add a folder and its contents to the file list."""
        if not self.is_file_in_list(folder):
            item = QListWidgetItem(folder)
            item.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_DirIcon')))
            self.file_list.addItem(item)
            
            # Add all files in the folder
            for root, _, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    self.transfer_files.append((file_path, ''))  # Destination will be set later
    
    def is_file_in_list(self, file_path):
        """Check if a file is already in the transfer list."""
        for i in range(self.file_list.count()):
            if self.file_list.item(i).text() == file_path:
                return True
        return False
    
    def remove_selected(self):
        """Remove selected items from the file list."""
        for item in self.file_list.selectedItems():
            row = self.file_list.row(item)
            self.file_list.takeItem(row)
            if row < len(self.transfer_files):
                self.transfer_files.pop(row)
    
    def clear_files(self):
        """Clear all files from the transfer list."""
        self.file_list.clear()
        self.transfer_files.clear()
    
    def browse_destination(self):
        """Open a directory dialog to select destination."""
        directory = QFileDialog.getExistingDirectory(self, "Select Destination")
        
        if directory:
            self.dest_path_edit.setText(directory)
    
    def start_transfer(self):
        """Start the file transfer process."""
        if not self.transfer_files:
            QMessageBox.warning(self, "No Files", "No files selected for transfer.")
            return
        
        dest_dir = self.dest_path_edit.text()
        if not dest_dir:
            QMessageBox.warning(self, "No Destination", "Please select a destination directory.")
            return
        
        # Update transfer files with destination paths
        for i, (src, _) in enumerate(self.transfer_files):
            rel_path = os.path.relpath(src, os.path.dirname(src)) if self.preserve_cb.isChecked() else os.path.basename(src)
            dest_path = os.path.join(dest_dir, rel_path)
            self.transfer_files[i] = (src, dest_path)
        
        # Disable UI elements
        self.set_transfer_ui_state(False)
        
        # Start transfer in a worker thread
        self.transfer_worker = TransferWorker(self.transfer_files, dest_dir)
        self.transfer_worker.signals.progress.connect(self.update_progress)
        self.transfer_worker.signals.finished.connect(self.transfer_finished)
        self.transfer_worker.signals.error.connect(self.transfer_error)
        self.transfer_worker.signals.file_started.connect(self.file_started)
        self.transfer_worker.signals.file_completed.connect(self.file_completed)
        
        self.transfer_worker.start()
    
    def toggle_pause(self):
        """Toggle pause state of the transfer."""
        if not self.transfer_worker:
            return
            
        if self.transfer_worker._is_paused:
            self.transfer_worker.resume()
            self.pause_btn.setText("Pause")
            self.pause_action.setText("Pause")
            self.statusBar().showMessage("Resuming transfer...")
        else:
            self.transfer_worker.pause()
            self.pause_btn.setText("Resume")
            self.pause_action.setText("Resume")
            self.statusBar().showMessage("Transfer paused")
    
    def cancel_transfer(self):
        """Cancel the current transfer."""
        if self.transfer_worker and self.transfer_worker.isRunning():
            reply = QMessageBox.question(
                self, 'Cancel Transfer',
                'Are you sure you want to cancel the transfer?',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                self.transfer_worker.stop()
                self.statusBar().showMessage("Transfer cancelled")
                self.set_transfer_ui_state(True)
    
    def set_transfer_ui_state(self, enabled):
        """Enable or disable UI elements during transfer."""
        self.transfer_btn.setEnabled(enabled)
        self.pause_btn.setEnabled(not enabled)
        self.cancel_btn.setEnabled(not enabled)
        self.start_action.setEnabled(enabled)
        self.pause_action.setEnabled(not enabled)
        self.cancel_action.setEnabled(not enabled)
        
        # Disable other controls during transfer
        self.browse_source_btn.setEnabled(enabled)
        self.add_files_btn.setEnabled(enabled)
        self.add_folder_btn.setEnabled(enabled)
        self.remove_btn.setEnabled(enabled)
        self.clear_btn.setEnabled(enabled)
        self.browse_dest_btn.setEnabled(enabled)
        self.refresh_drives_btn.setEnabled(enabled)
    
    def update_progress(self, current, total):
        """Update the progress bars."""
        if total > 0:  # File progress
            self.file_progress.setValue(current)
        else:  # Overall progress
            self.overall_progress.setValue(current)
    
    def file_started(self, filename):
        """Update UI when a file transfer starts."""
        self.current_file.setText(f"Transferring: {filename}")
        self.file_progress.setValue(0)
        self.statusBar().showMessage(f"Transferring {filename}...")
    
    def file_completed(self, filename):
        """Update UI when a file transfer completes."""
        self.statusBar().showMessage(f"Completed: {filename}")
    
    def transfer_finished(self):
        """Handle transfer completion."""
        self.set_transfer_ui_state(True)
        self.overall_progress.setValue(100)
        self.current_file.setText("Transfer complete")
        self.statusBar().showMessage("Transfer completed successfully")
        
        # Reset progress bars
        QTimer.singleShot(3000, lambda: self.overall_progress.setValue(0))
        QTimer.singleShot(3000, lambda: self.file_progress.setValue(0))
    
    def transfer_error(self, error_msg):
        """Handle transfer errors."""
        self.set_transfer_ui_state(True)
        QMessageBox.critical(self, "Transfer Error", error_msg)
        self.statusBar().showMessage("Transfer failed")
    
    def new_transfer(self):
        """Start a new transfer session."""
        if self.transfer_worker and self.transfer_worker.isRunning():
            QMessageBox.warning(self, "Transfer in Progress", 
                              "Please wait for the current transfer to complete.")
            return
        
        reply = QMessageBox.question(
            self, 'New Transfer',
            'Clear all files and start a new transfer?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.clear_files()
            self.source_path_edit.clear()
            self.dest_path_edit.clear()
            self.overall_progress.setValue(0)
            self.file_progress.setValue(0)
            self.current_file.setText("Ready")
            self.statusBar().showMessage("New transfer started")
    
    def show_settings(self):
        """Show the settings dialog."""
        if self.settings_dialog is None:
            from .settings_dialog import SettingsDialog
            self.settings_dialog = SettingsDialog(self.current_settings(), self)
            self.settings_dialog.settings_saved.connect(self.apply_settings)
        
        self.settings_dialog.show()
        self.settings_dialog.raise_()
        self.settings_dialog.activateWindow()
    
    def current_settings(self):
        """Get the current settings from the UI."""
        return {
            'source_folders': self.config.get('source_folders', []),
            'file_types': self.config.get('file_types', []),
            'min_file_size_mb': self.config.get('min_file_size_mb', 0),
            'max_file_size_mb': self.config.get('max_file_size_mb', 0),
            'date_filter_days': self.config.get('date_filter_days', 0),
            'default_destination': self.config.get('default_destination', ''),
            'auto_select_destination': self.config.get('auto_select_destination', True),
            'notifications': {
                'popup': self.config.get('notifications/popup', True),
                'tray': self.config.get('notifications/tray', True),
                'sound': self.config.get('notifications/sound', True)
            },
            'transfer': {
                'preserve_structure': self.preserve_cb.isChecked(),
                'verify_checksum': self.verify_cb.isChecked(),
                'conflict_resolution': self.overwrite_combo.currentText().lower(),
                'overwrite_policy': self.overwrite_combo.currentText().lower(),
                'verify': self.verify_cb.isChecked(),
            },
            'appearance': {
                'theme': self.config.get('appearance/theme', 'system'),
                'font_size': self.config.get('appearance/font_size', 9),
                'icon_theme': self.config.get('appearance/icon_theme', 'default')
            },
            'recent_destinations': self.config.get('recent_destinations', []),
            'recent_sources': self.config.get('recent_sources', [])
        }
    
    def show_about(self):
        """Show the about dialog."""
        about_text = """
        <h2>File Transfer Assistant</h2>
        <p>Version 1.0.0</p>
        <p>A simple application for transferring files between devices.</p>
        <p>© 2025 CodeX Computing Co. All rights reserved.</p>
        """
        QMessageBox.about(self, "About File Transfer Assistant", about_text)
    
    def show_documentation(self):
        """Open the documentation in the default web browser."""
        from PySide6.QtCore import QUrl
        from PySide6.QtGui import QDesktopServices
        QDesktopServices.openUrl(QUrl("https://github.com/abubakarp789/Python-Internship-CodeX-Computing-Co/FileTransferAssistant/README.md"))
    
    def toggle_toolbar(self, visible):
        """Toggle the visibility of the toolbar."""
        if hasattr(self, 'toolbar'):
            self.toolbar.setVisible(visible)
            self.config.set('window/toolbar_visible', visible)
    
    def toggle_statusbar(self, visible):
        """Toggle the visibility of the status bar."""
        self.statusBar().setVisible(visible)
        self.config.set('window/statusbar_visible', visible)
    
    def update_quick_access_buttons(self):
        """Update the quick access buttons with user's source folders."""
        if not hasattr(self, 'quick_access_layout'):
            return
            
        # Clear existing buttons
        while self.quick_access_layout.count() > 0:
            item = self.quick_access_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Add default folders
        default_folders = [
            ("Desktop", str(Path.home() / "Desktop")),
            ("Documents", str(Path.home() / "Documents")),
            ("Downloads", str(Path.home() / "Downloads"))
        ]
        
        # Add user's source folders
        source_folders = self.config.get('source_folders', [])
        for i, folder in enumerate(source_folders):
            if i < 3:  # Show max 3 folders
                btn = QPushButton(Path(folder).name)
                btn.setToolTip(folder)
                btn.setProperty('path', folder)
                btn.clicked.connect(lambda checked, p=folder: self.set_source_folder(p))
                self.quick_access_layout.addWidget(btn)
        
        # Add default folders if we have space
        for name, path in default_folders:
            if self.quick_access_layout.count() < 3 and path not in source_folders:
                btn = QPushButton(name)
                btn.setToolTip(path)
                btn.setProperty('path', path)
                btn.clicked.connect(lambda checked, p=path: self.set_source_folder(p))
                self.quick_access_layout.addWidget(btn)
        
        # Add a button to open settings if we have more folders
        if len(source_folders) > 3:
            more_btn = QPushButton("More...")
            more_btn.clicked.connect(self.show_settings)
            self.quick_access_layout.addWidget(more_btn)
    
    def update_recent_sources_menu(self):
        """Update the recent sources menu."""
        if not hasattr(self, 'recent_sources_menu'):
            return
            
        self.recent_sources_menu.clear()
        recent_sources = self.config.get('recent_sources', [])
        
        for i, source in enumerate(recent_sources):
            action = QAction(f"{i+1}. {source}", self)
            action.triggered.connect(lambda checked, s=source: self.set_source_folder(s))
            self.recent_sources_menu.addAction(action)
        
        self.recent_sources_menu.setEnabled(bool(recent_sources))
    
    def update_recent_destinations_menu(self):
        """Update the recent destinations menu."""
        if not hasattr(self, 'recent_destinations_menu'):
            return
            
        self.recent_destinations_menu.clear()
        recent_dests = self.config.get('recent_destinations', [])
        
        for i, dest in enumerate(recent_dests):
            action = QAction(f"{i+1}. {dest}", self)
            action.triggered.connect(lambda checked, d=dest: self.set_destination(d))
            self.recent_destinations_menu.addAction(action)
        
        self.recent_destinations_menu.setEnabled(bool(recent_dests))
    
    def apply_initial_settings(self):
        """Apply settings when the application starts."""
        # Apply window settings
        from PySide6.QtCore import QByteArray
        
        # Restore window geometry
        geometry_data = self.config.get('window/geometry')
        if geometry_data:
            try:
                geometry = QByteArray.fromBase64(geometry_data.encode())
                if not geometry.isEmpty():
                    self.restoreGeometry(geometry)
            except Exception as e:
                print(f"Error restoring window geometry: {e}")
        
        # Restore window state (maximized, minimized, etc.)
        state_data = self.config.get('window/state')
        if state_data:
            try:
                state = QByteArray.fromBase64(state_data.encode())
                if not state.isEmpty():
                    self.restoreState(state)
            except Exception as e:
                print(f"Error restoring window state: {e}")
        
        # Show maximized if needed
        if self.config.get('window/maximized', False):
            self.showMaximized()
        
        # Apply toolbar and statusbar visibility
        toolbar_visible = self.config.get('window/toolbar_visible', True)
        if hasattr(self, 'toolbar'):
            self.toolbar.setVisible(toolbar_visible)
        if hasattr(self, 'toolbar_toggle'):
            self.toolbar_toggle.setChecked(toolbar_visible)
        
        statusbar_visible = self.config.get('window/statusbar_visible', True)
        self.statusBar().setVisible(statusbar_visible)
        if hasattr(self, 'statusbar_toggle'):
            self.statusbar_toggle.setChecked(statusbar_visible)
        
        # Apply transfer settings
        if hasattr(self, 'overwrite_combo') and hasattr(self, 'verify_cb') and hasattr(self, 'preserve_cb'):
            self.overwrite_combo.setCurrentText(
                self.config.get('transfer/overwrite_policy', 'Ask').capitalize())
            self.verify_cb.setChecked(self.config.get('transfer/verify', False))
            self.preserve_cb.setChecked(self.config.get('transfer/preserve_structure', True))
        
        # Set default destination if auto-select is enabled
        if self.config.get('auto_select_destination', True):
            default_dest = self.config.get('default_destination')
            if default_dest and os.path.exists(default_dest):
                self.set_destination(default_dest)
    
    def apply_settings(self, settings):
        """Apply settings from the settings dialog."""
        # Save settings to config
        for key, value in settings.items():
            if key in ['notifications', 'transfer', 'appearance']:
                for subkey, subvalue in value.items():
                    self.config.set(f"{key}/{subkey}", subvalue)
            else:
                self.config.set(key, value)
        
        # Apply theme
        self.apply_theme(settings.get('appearance', {}).get('theme', 'system'))
        
        # Update UI
        self.update_quick_access_buttons()
        self.update_recent_sources_menu()
        self.update_recent_destinations_menu()
        
        # Apply transfer settings
        if 'transfer' in settings:
            transfer = settings['transfer']
            if hasattr(self, 'overwrite_combo') and 'overwrite_policy' in transfer:
                self.overwrite_combo.setCurrentText(transfer['overwrite_policy'].capitalize())
            if hasattr(self, 'verify_cb') and 'verify' in transfer:
                self.verify_cb.setChecked(transfer['verify'])
            if hasattr(self, 'preserve_cb') and 'preserve_structure' in transfer:
                self.preserve_cb.setChecked(transfer['preserve_structure'])
        
        # Save config
        self.config.save()
    
    def set_destination(self, path):
        """Set the destination path and update the UI."""
        if not path or not os.path.isdir(path):
            return
            
        if hasattr(self, 'dest_path_edit'):
            self.dest_path_edit.setText(path)
        
        self.config.add_recent_destination(path)
        self.update_recent_destinations_menu()
    
    def save_settings(self):
        """Save application settings."""
        # Save window geometry and state as base64 strings
        geometry = self.saveGeometry()
        if not geometry.isEmpty():
            self.config.set('window/geometry', geometry.toBase64().data().decode())
        
        # Save window state
        state = self.saveState()
        if not state.isEmpty():
            self.config.set('window/state', state.toBase64().data().decode())
        
        # Save window visibility settings
        if hasattr(self, 'toolbar') and hasattr(self, 'toolbar_toggle'):
            self.config.set('window/toolbar_visible', self.toolbar.isVisible())
        if hasattr(self, 'statusbar_toggle'):
            self.config.set('window/statusbar_visible', self.statusBar().isVisible())
        
        # Save transfer settings
        if hasattr(self, 'overwrite_combo') and hasattr(self, 'verify_cb') and hasattr(self, 'preserve_cb'):
            self.config.set('transfer/overwrite_policy', 
                          self.overwrite_combo.currentText().lower())
            self.config.set('transfer/verify', 
                          self.verify_cb.isChecked())
            self.config.set('transfer/preserve_structure', 
                          self.preserve_cb.isChecked())
        
        # Save the config
        self.config.save()
    
    def closeEvent(self, event):
        """Handle window close event."""
        self.save_settings()
        event.accept()
