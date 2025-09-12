from MainWindow.main_window import MainWindow
from PySide6.QtWidgets import QApplication
from Files.img_repo import CreateDir
from InstallWizard.install_wizard import InstallWizardDialog
import sys 
import os

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    #window.setGeometry(250, 250, 1500, 1250)
    window.showMaximized()
    
    window.show()

    sys.exit(app.exec())




