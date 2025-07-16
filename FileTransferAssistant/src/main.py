import sys
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMessageBox

# Import application modules
from .config import ConfigManager
from .ui.main_window import MainWindow

def main():
    """Main entry point for the application."""
    try:
        # Initialize QApplication
        app = QApplication(sys.argv)
        
        # Set application information
        app.setApplicationName("File Transfer Assistant")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("CodeX Computing Co.")
        
        # Initialize configuration
        config_dir = Path.home() / '.filetransferassistant'
        config_dir.mkdir(exist_ok=True, parents=True)
        config_file = config_dir / 'config.json'
        
        config = ConfigManager(str(config_file))
        
        # Create and show main window
        window = MainWindow(config)
        window.show()
        
        # Start the application event loop
        return app.exec()
        
    except Exception as e:
        QMessageBox.critical(None, "Error", f"An error occurred: {str(e)}")
        return 1

if __name__ == "__main__":
    # Add the src directory to the Python path
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.exit(main())
