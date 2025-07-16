#!/usr/bin/env python3
"""Main entry point for the File Transfer Assistant application."""

import sys
import traceback
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMessageBox

from config import Config
from ui.main_window import MainWindow


def handle_exception(exc_type, exc_value, exc_traceback):
    """Handle uncaught exceptions and display them in a message box."""
    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    print(f"Unhandled exception: {error_msg}", file=sys.stderr)
    
    # Only show message box if QApplication exists
    if QApplication.instance() is not None:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Unexpected Error")
        msg.setText("An unexpected error occurred.")
        msg.setDetailedText(error_msg)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()


def main():
    """Run the application."""
    # Set up exception handling
    sys.excepthook = handle_exception
    
    try:
        # Initialize application
        app = QApplication(sys.argv)
        
        # Set application information
        app.setApplicationName("File Transfer Assistant")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("CodeX Computing Co.")
        
        # Initialize configuration
        config_dir = Path.home() / '.filetransferassistant'
        config_dir.mkdir(exist_ok=True, parents=True)
        config_file = config_dir / 'config.json'
        
        config = Config(str(config_file))
        
        # Create and show the main window
        window = MainWindow(config)
        window.show()
        
        # Start the event loop
        sys.exit(app.exec())
        
    except Exception as e:
        handle_exception(type(e), e, e.__traceback__)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
