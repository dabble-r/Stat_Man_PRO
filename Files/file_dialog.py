from PySide6.QtWidgets import QDialog, QFileDialog, QApplication, QWidget

import os 
import sys
import platform

class FileDialog(QWidget):
    def __init__(self, dir_path, message, parent):
        super().__init__()
        self.setWindowTitle("File Dialog Example")
        self.setGeometry(100, 100, 400, 200)
        self.dir_path = dir_path
        self.file_path = None
        self.message = message
        self.parent = parent

    def open_file_dialog(self):
        filename, _ = QFileDialog.getOpenFileName(
            parent=self.parent,
            caption="Select a file",
            dir=f"{self.dir_path}",  # Initial directory
            filter="Images (*.png *.jpg *.jpeg *.gif);;All Files (*.*)" # File filters
        )
        if filename:
            #print(f"Selected file: {filename}")
            #print(f'file dir-file dialog: {self.dir_path}')
            try:
                self.file_path = filename  # ← Use the absolute path directly
                #full_path = os.path.join(self.dir_path, filename)
                #self.file_path = full_path 
            except Exception as e:
                #print(f'error joining file:\n {e}')
                self.message.show_message(f'Error:\n{e}')
                return
        else:
            print("No file selected.")
           
    def get_file_path(self):
        #print(f'get file path: {self.file_path}')
        return self.file_path
    
    def get_cwd(self):
        pass
        







