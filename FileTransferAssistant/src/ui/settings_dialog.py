"""Settings dialog for File Transfer Assistant."""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
    QLabel, QLineEdit, QPushButton, QFileDialog, QCheckBox,
    QComboBox, QSpinBox, QDoubleSpinBox, QGroupBox, QListWidget,
    QListWidgetItem, QAbstractItemView, QDialogButtonBox, QMessageBox
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIcon
import json
import os
from pathlib import Path

class SettingsDialog(QDialog):
    """Settings dialog for the application."""
    
    settings_saved = Signal(dict)  # Signal emitted when settings are saved
    
    def __init__(self, current_settings, parent=None):
        """Initialize the settings dialog."""
        super().__init__(parent)
        self.current_settings = current_settings
        self.setWindowTitle("Settings")
        self.setMinimumSize(700, 600)
        
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        
        # Create tab widget
        self.tabs = QTabWidget()
        
        # Add tabs
        self.tabs.addTab(self.create_source_tab(), "Source Folders")
        self.tabs.addTab(self.create_filters_tab(), "File Filters")
        self.tabs.addTab(self.create_destination_tab(), "Destination")
        self.tabs.addTab(self.create_notifications_tab(), "Notifications")
        self.tabs.addTab(self.create_transfer_tab(), "Transfer")
        self.tabs.addTab(self.create_appearance_tab(), "Appearance")
        
        layout.addWidget(self.tabs)
        
        # Add buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.RestoreDefaults
        )
        button_box.accepted.connect(self.save_settings)
        button_box.rejected.connect(self.reject)
        button_box.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.confirm_restore_defaults)
        
        layout.addWidget(button_box)
    
    def create_source_tab(self):
        """Create the Source Folders tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Default source folders group
        group = QGroupBox("Default Source Folders")
        group_layout = QVBoxLayout()
        
        # List widget for folders
        self.folder_list = QListWidget()
        self.folder_list.setSelectionMode(QAbstractItemView.SingleSelection)
        
        # Buttons for managing folders
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add Folder")
        self.add_btn.clicked.connect(self.add_source_folder)
        self.remove_btn = QPushButton("Remove Selected")
        self.remove_btn.clicked.connect(self.remove_source_folder)
        
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.remove_btn)
        
        group_layout.addWidget(QLabel("Select folders to use as default sources:"))
        group_layout.addWidget(self.folder_list)
        group_layout.addLayout(btn_layout)
        group.setLayout(group_layout)
        
        layout.addWidget(group)
        layout.addStretch()
        
        return tab
    
    def create_filters_tab(self):
        """Create the File Filters tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # File types group
        type_group = QGroupBox("File Types")
        type_layout = QVBoxLayout()
        
        self.file_types_edit = QLineEdit()
        self.file_types_edit.setPlaceholderText("Example: .jpg, .pdf, .docx")
        type_layout.addWidget(QLabel("File extensions to include (comma-separated):"))
        type_layout.addWidget(self.file_types_edit)
        type_group.setLayout(type_layout)
        
        # File size group
        size_group = QGroupBox("File Size")
        size_layout = QVBoxLayout()
        
        size_hbox = QHBoxLayout()
        self.min_size_spin = QDoubleSpinBox()
        self.min_size_spin.setRange(0, 9999)
        self.min_size_spin.setSuffix(" MB")
        self.max_size_spin = QDoubleSpinBox()
        self.max_size_spin.setRange(0, 9999)
        self.max_size_spin.setSuffix(" MB")
        
        size_hbox.addWidget(QLabel("Min:"))
        size_hbox.addWidget(self.min_size_spin)
        size_hbox.addWidget(QLabel("Max:"))
        size_hbox.addWidget(self.max_size_spin)
        
        size_layout.addLayout(size_hbox)
        size_group.setLayout(size_layout)
        
        # Date modified group
        date_group = QGroupBox("Date Modified")
        date_layout = QVBoxLayout()
        
        self.date_filter_cb = QCheckBox("Only include files modified in the last")
        self.days_spin = QSpinBox()
        self.days_spin.setRange(1, 365)
        self.days_spin.setValue(30)
        
        date_hbox = QHBoxLayout()
        date_hbox.addWidget(self.date_filter_cb)
        date_hbox.addWidget(self.days_spin)
        date_hbox.addWidget(QLabel("days"))
        date_hbox.addStretch()
        
        date_layout.addLayout(date_hbox)
        date_group.setLayout(date_layout)
        
        layout.addWidget(type_group)
        layout.addWidget(size_group)
        layout.addWidget(date_group)
        layout.addStretch()
        
        return tab
    
    def create_destination_tab(self):
        """Create the Destination tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Default destination group
        group = QGroupBox("Default Destination")
        group_layout = QVBoxLayout()
        
        self.destination_edit = QLineEdit()
        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.clicked.connect(self.browse_destination)
        
        hbox = QHBoxLayout()
        hbox.addWidget(self.destination_edit)
        hbox.addWidget(self.browse_btn)
        
        self.auto_select_cb = QCheckBox("Auto-select this destination on startup if available")
        
        group_layout.addWidget(QLabel("Default destination folder:"))
        group_layout.addLayout(hbox)
        group_layout.addWidget(self.auto_select_cb)
        group.setLayout(group_layout)
        
        layout.addWidget(group)
        layout.addStretch()
        
        return tab
    
    def create_notifications_tab(self):
        """Create the Notifications tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Notifications group
        group = QGroupBox("Notifications")
        group_layout = QVBoxLayout()
        
        self.popup_cb = QCheckBox("Show popup alerts")
        self.tray_cb = QCheckBox("Show system tray notifications")
        self.sound_cb = QCheckBox("Play sound for completed transfers")
        
        group_layout.addWidget(self.popup_cb)
        group_layout.addWidget(self.tray_cb)
        group_layout.addWidget(self.sound_cb)
        group.setLayout(group_layout)
        
        layout.addWidget(group)
        layout.addStretch()
        
        return tab
    
    def create_transfer_tab(self):
        """Create the Transfer tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Transfer options group
        group = QGroupBox("Transfer Options")
        group_layout = QVBoxLayout()
        
        self.preserve_structure_cb = QCheckBox("Preserve folder structure")
        self.verify_checksum_cb = QCheckBox("Verify file integrity with checksum")
        
        # Conflict resolution
        conflict_group = QGroupBox("File Conflict Resolution")
        conflict_layout = QVBoxLayout()
        
        self.conflict_combo = QComboBox()
        self.conflict_combo.addItems(["Ask what to do", "Overwrite existing", "Skip", "Rename new file"])
        
        conflict_layout.addWidget(QLabel("When a file already exists:"))
        conflict_layout.addWidget(self.conflict_combo)
        conflict_group.setLayout(conflict_layout)
        
        group_layout.addWidget(self.preserve_structure_cb)
        group_layout.addWidget(self.verify_checksum_cb)
        group_layout.addWidget(conflict_group)
        group.setLayout(group_layout)
        
        layout.addWidget(group)
        layout.addStretch()
        
        return tab
    
    def create_appearance_tab(self):
        """Create the Appearance tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Theme group
        theme_group = QGroupBox("Theme")
        theme_layout = QVBoxLayout()
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["System", "Light", "Dark"])
        
        theme_layout.addWidget(QLabel("Select theme:"))
        theme_layout.addWidget(self.theme_combo)
        theme_group.setLayout(theme_layout)
        
        # Other appearance options can be added here
        
        layout.addWidget(theme_group)
        layout.addStretch()
        
        return tab
    
    def add_source_folder(self):
        """Add a folder to the source folders list."""
        folder = QFileDialog.getExistingDirectory(self, "Select Source Folder")
        if folder and folder not in [self.folder_list.item(i).text() for i in range(self.folder_list.count())]:
            self.folder_list.addItem(folder)
    
    def remove_source_folder(self):
        """Remove the selected folder from the list."""
        if self.folder_list.currentRow() >= 0:
            self.folder_list.takeItem(self.folder_list.currentRow())
    
    def browse_destination(self):
        """Open a dialog to select the default destination folder."""
        folder = QFileDialog.getExistingDirectory(self, "Select Default Destination Folder")
        if folder:
            self.destination_edit.setText(folder)
    
    def load_settings(self):
        """Load settings into the UI."""
        # Source folders
        self.folder_list.clear()
        for folder in self.current_settings.get('source_folders', []):
            self.folder_list.addItem(folder)
        
        # File filters
        self.file_types_edit.setText(', '.join(self.current_settings.get('file_types', [])))
        self.min_size_spin.setValue(self.current_settings.get('min_file_size_mb', 0))
        self.max_size_spin.setValue(self.current_settings.get('max_file_size_mb', 9999))
        
        date_filter = self.current_settings.get('date_filter_days', 0)
        self.date_filter_cb.setChecked(date_filter > 0)
        self.days_spin.setValue(date_filter if date_filter > 0 else 30)
        
        # Destination
        self.destination_edit.setText(self.current_settings.get('default_destination', ''))
        self.auto_select_cb.setChecked(self.current_settings.get('auto_select_destination', True))
        
        # Notifications
        self.popup_cb.setChecked(self.current_settings.get('notifications_popup', True))
        self.tray_cb.setChecked(self.current_settings.get('notifications_tray', True))
        self.sound_cb.setChecked(self.current_settings.get('notifications_sound', True))
        
        # Transfer options
        self.preserve_structure_cb.setChecked(self.current_settings.get('preserve_structure', True))
        self.verify_checksum_cb.setChecked(self.current_settings.get('verify_checksum', True))
        self.conflict_combo.setCurrentText(
            self.current_settings.get('conflict_resolution', 'Ask what to do'))
        
        # Appearance
        self.theme_combo.setCurrentText(
            self.current_settings.get('theme', 'System').capitalize())
    
    def get_settings(self):
        """Get the current settings from the UI."""
        settings = {}
        
        # Source folders
        settings['source_folders'] = [self.folder_list.item(i).text() 
                                    for i in range(self.folder_list.count())]
        
        # File filters
        file_types = [ft.strip() for ft in self.file_types_edit.text().split(',') 
                     if ft.strip()]
        settings['file_types'] = file_types
        
        settings['min_file_size_mb'] = self.min_size_spin.value()
        settings['max_file_size_mb'] = self.max_size_spin.value()
        
        settings['date_filter_days'] = self.days_spin.value() if self.date_filter_cb.isChecked() else 0
        
        # Destination
        settings['default_destination'] = self.destination_edit.text()
        settings['auto_select_destination'] = self.auto_select_cb.isChecked()
        
        # Notifications
        settings['notifications_popup'] = self.popup_cb.isChecked()
        settings['notifications_tray'] = self.tray_cb.isChecked()
        settings['notifications_sound'] = self.sound_cb.isChecked()
        
        # Transfer options
        settings['preserve_structure'] = self.preserve_structure_cb.isChecked()
        settings['verify_checksum'] = self.verify_checksum_cb.isChecked()
        settings['conflict_resolution'] = self.conflict_combo.currentText()
        
        # Appearance
        settings['theme'] = self.theme_combo.currentText().lower()
        
        return settings
    
    def save_settings(self):
        """Save the current settings and close the dialog."""
        self.current_settings = self.get_settings()
        self.settings_saved.emit(self.current_settings)
        self.accept()
    
    def confirm_restore_defaults(self):
        """Confirm before restoring default settings."""
        reply = QMessageBox.question(
            self,
            'Restore Defaults',
            'Are you sure you want to restore all settings to their default values?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.restore_defaults()
    
    def restore_defaults(self):
        """Restore all settings to their default values."""
        # Default settings
        default_settings = {
            'source_folders': [],
            'file_types': [],
            'min_file_size_mb': 0,
            'max_file_size_mb': 9999,
            'date_filter_days': 0,
            'default_destination': '',
            'auto_select_destination': True,
            'notifications_popup': True,
            'notifications_tray': True,
            'notifications_sound': True,
            'preserve_structure': True,
            'verify_checksum': True,
            'conflict_resolution': 'Ask what to do',
            'theme': 'system'
        }
        
        self.current_settings = default_settings
        self.load_settings()
