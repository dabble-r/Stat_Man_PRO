from PySide6.QtWidgets import QDialog, QFileDialog, QApplication, QWidget

import os 
import sys
import platform

class FileDialog(QWidget):
    def __init__(self, message, parent=None, flag=None):
        super().__init__()
        self.setWindowTitle("File Dialog Example")
        self.setGeometry(100, 100, 400, 200)
        self.os_type = platform.system()
        self.cwd = self.get_cwd()
        self.file_dir = self.get_file_dir()
        self.message = message
        self.parent = parent
        self.file_path = None
        self.flag = flag

    # deprecated
    def open_file_dialog(self):
        print("open dialog")
        filter_str = None
        if self.flag == 'save':
            filter_str = "Images (*.png *.jpg *.jpeg *.gif);;All Files (*.*)"
        elif self.flag == 'load':
            filter_str = "CSV Files (*.csv);;All Files (*.*)"
        filename, _ = QFileDialog.getOpenFileName(
            parent=self.parent,
            caption="Select a file",
            dir=f"{self.file_dir}",  # Initial directory
            #filter="Images (*.png *.jpg *.jpeg *.gif);;All Files (*.*)" # File filters
            filter = filter_str
        )
        if filename:
            print(f"Selected file: {filename}")
            #print(f'file dir-file dialog: {self.dir_path}')
            try:
                #full_path = os.path.join(self.file_dir, filename)
                isFile = os.path.isfile(filename)
                if isFile:
                    self.file_path = filename  # ← Use the absolute path directly
            except Exception as e:
                #print(f'error joining file:\n {e}')
                self.message.show_message(f'Error:\n{e}')
                return
        else:
            print("No file selected.")
            self.message.show_message("No file selected!")
           
    def get_file_dir(self):
        if self.os_type == 'Windows':
            print('Windows')
            new_dir = os.path.join(self.cwd, "Saved")
            if not os.path.exists(new_dir):
                os.mkdir(new_dir)
            return new_dir

        elif self.os_type == 'Linux':
            print('Linux')
            new_dir = f"{self.cwd}/Saved"
            isExist = os.path.exists(new_dir)
            if not isExist:
                os.mkdir(new_dir)
            return new_dir

        else:
            print('Other')
            return 
        
    def get_cwd(self):
        cwd = os.getcwd()
        return cwd
    
    def get_file_path(self):
        return self.file_path
        
    
   







