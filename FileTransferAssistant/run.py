#!/usr/bin/env python3
"""Run the File Transfer Assistant application."""

import sys
import os

# Add the project root and src directories to the Python path
project_root = os.path.abspath(os.path.dirname(__file__))
src_dir = os.path.join(project_root, 'src')

# Add to path if not already there
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def main():
    """Run the application."""
    from PySide6.QtWidgets import QApplication, QMessageBox
    from src.ui.main_window import MainWindow
    from src.config import Config
    try:
        # Create the application
        app = QApplication(sys.argv)
        
        # Set application information
        app.setApplicationName("File Transfer Assistant")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("CodeX Computing Co.")
        
        # Use ConfigManager which handles the configuration file path automatically
        from src.config import ConfigManager
        config = ConfigManager()
        
        # Create and show the main window
        window = MainWindow(config)
        window.show()
        
        # Start the event loop
        return app.exec()
        
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Failed to start application: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
