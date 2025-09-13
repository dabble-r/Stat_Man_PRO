from MainWindow.main_window import MainWindow
from PySide6.QtWidgets import QApplication
from Files.img_repo import CreateDir
from InstallWizard.install_wizard import InstallWizardDialog
from Styles.stylesheets import StyleSheets
import sys 
import os

if __name__ == "__main__":
    app = QApplication(sys.argv)
    styles = StyleSheets()
    app.setStyleSheet(styles.get_monochrome_1_style())

    window = MainWindow(app)

    sys.exit(app.exec())




