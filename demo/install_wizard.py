import sys
import os
import platform
from PySide6.QtWidgets import (
    QApplication, QDialog, QLabel, QPushButton, QLineEdit, QFileDialog,
    QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import QDir
from PySide6.QtCore import Qt

class InstallWizardDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ImageSaver Setup Wizard")
        self.setMinimumSize(500, 200)

        self.init_ui()

    def init_ui(self):
        # Title and Description
        title = QLabel("<b>ImageSaver Installation Wizard</b>")
        description = QLabel("Choose a folder where images should be saved:")
        description.setWordWrap(True)

        # Directory path input
        self.path_edit1 = QLineEdit()
        self.path_edit1.setPlaceholderText("Select a directory to save images...")
        self.path_edit1.setReadOnly(True)

        # Name New Folder
        self.path_edit2 = QLineEdit()
        self.path_edit2.setPlaceholderText("Create new folder...")
        #self.path_edit2.setReadOnly(True)

        # Browse button
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.select_directory)

        # Layout for path + browse button
        path_layout = QHBoxLayout()
        input_layout = QVBoxLayout()
        input_layout.addWidget(self.path_edit1)
        input_layout.addWidget(self.path_edit2)
        path_layout.addLayout(input_layout)
        path_layout.addWidget(browse_btn)

        # Bottom navigation buttons
        #back_btn = QPushButton("Back")
        submit_btn = QPushButton("Submit")
        cancel_btn = QPushButton("Cancel")

        #back_btn.clicked.connect(self.go_back)
        submit_btn.clicked.connect(self.submit_handler)  # For this example, "Next" accepts the dialog
        cancel_btn.clicked.connect(self.reject)

        nav_layout = QHBoxLayout()
        nav_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        #nav_layout.addWidget(back_btn)
        nav_layout.addWidget(submit_btn)
        nav_layout.addWidget(cancel_btn)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addLayout(path_layout)
        layout.addStretch()
        layout.addLayout(nav_layout)
        self.setLayout(layout)

    def select_directory(self):
        system = platform.system()
        path = '/mnt/c/Users/' if system == 'Linux' else 'C:/Users'
        directory = QFileDialog.getExistingDirectory(self, "Choose Save Location", dir=f'{path}')
        if directory:
            self.path_edit1.setText(directory)
    
    def create_dir(self, dir, new_folder):
        full_path = os.path.join(dir, new_folder)
        dir_creator = QDir()
        new_dir = dir_creator.mkdir(full_path)
        if new_dir:
            print(f'New folder {new_folder} created at {full_path}.')
        else:
            print(f'New folder creation not successful.')

    # not in use
    def go_back(self):
        # In a real wizard, this would return to a previous step
        print("Back button pressed (no previous page in this example)")

    def get_selected_path(self):
        return self.path_edit1.text()
    
    def submit_handler(self):
        new_folder = self.path_edit2.text()
        dir = self.get_selected_path()
        if dir and new_folder:
            self.create_dir(dir, new_folder)
            #print(dir)
        else:
            print('New folder unsuccessful.')
        self.accept()


# Test dialog
if __name__ == "__main__":
    app = QApplication(sys.argv)
    wizard = InstallWizardDialog()
    wizard.exec()
    
