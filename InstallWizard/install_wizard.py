import sys
import os
import platform
from PySide6.QtWidgets import (
    QApplication, QDialog, QLabel, QPushButton, QLineEdit, QFileDialog,
    QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QMessageBox, QMainWindow
)
from PySide6.QtCore import QDir
from PySide6.QtCore import Qt, QRect, QPoint
from Message.message import Message
from Styles.stylesheets import StyleSheets
from CloseDialog.close import CloseDialog


class InstallWizardDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Install Wizard")
        #self.setMinimumSize(750, 200)
        self.styles = StyleSheets()
        self.message = Message(self.styles)
        #self.setStyleSheet(self.styles.Modern_styles)
        self.flag = True
        self.setWindowFlag(Qt.Window)
        self.parent = parent
        #self.setFixedSize(250, 50)
        #self.offset = offset
        
        # Get top-left corner of main window in global coordinates
        #main_pos = parent.mapToGlobal(QPoint(0, 0))
        # Add offset to position the dialog
        #target_pos = main_pos + self.offset
        #self.move(target_pos)
        #self.show()

        self.init_ui()
    
    def showEvent(self, event):
        super().showEvent(event)
        self.center_over_parent()
    
    def center_over_parent(self):
        if self.parent:
            # Get parent's geometry in global coordinates
            parent_rect = self.parent.frameGeometry()
            parent_center = parent_rect.center()

            # Get dialog geometry
            dialog_rect = self.frameGeometry()
            dialog_rect.moveCenter(parent_center)

            # Move dialog to calculated top-left corner
            self.move(dialog_rect.topLeft())

            #print("Parent center:", parent_center)
            #print("Dialog top-left:", dialog_rect.topLeft())


    def init_ui(self):
        # Title and Description
        title = QLabel("<b>Image Saver</b>")
        description = QLabel("Choose a folder where images should be saved:")
        description.setWordWrap(True)

        # Directory path input
        self.path_edit1 = QLineEdit()
        self.path_edit1.setPlaceholderText("Select a directory to save images...")
        self.path_edit1.setReadOnly(True)

        # Name New Folder
        #self.path_edit2 = QLineEdit()
        #self.path_edit2.setPlaceholderText("Create new folder...")
        #self.path_edit2.setReadOnly(True)

        # Browse button
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.select_directory)

        # Layout for path + browse button
        path_layout = QHBoxLayout()
        input_layout = QVBoxLayout()
        input_layout.addWidget(self.path_edit1)
        #input_layout.addWidget(self.path_edit2)
        path_layout.addLayout(input_layout)
        path_layout.addWidget(browse_btn)

        # Bottom navigation buttons
        #back_btn = QPushButton("Back")
        submit_btn = QPushButton("Submit")
        cancel_btn = QPushButton("Cancel")

        #back_btn.clicked.connect(self.go_back)
        submit_btn.clicked.connect(self.submit_handler)  # For this example, "Next" accepts the dialog
        cancel_btn.clicked.connect(self.confirm_cancel)

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
            # self.path_edit1.setText(directory)
            self.create_dir(directory)
        else:
            # user no selection - default path
            self.create_dir(path)
            #self.message.show_message('Please select directory!')
    
    def join_path(self, dir):
        full_path = os.path.join(dir, 'Stat_Man_Images')
        ##print('full path', full_path)
        return full_path

    def create_dir(self, dir):
        full_path = self.join_path(dir)
        #print('full path', full_path)
        dir_creator = QDir()
        # new_dir = dir_creator.mkdir(full_path)
        if not QDir(full_path).exists():
            #new_dir = dir_creator.mkdir(full_path)
            self.path_edit1.setText(full_path)
            ##print(f'New folder {new_dir} at {full_path} created.')
        elif QDir(full_path).exists():
            self.message.show_message('Folder already exists!')
            #print(f'New folder at {full_path} already exists.')
        else:
            self.message.show_message(f'New folder creation: {full_path} not successful.')
            #print(f'New folder creation not successful.')

    # not in use
    def go_back(self):
        # In a real wizard, this would return to a previous step
        print("Back button pressed (no previous page in this example)")
    
    '''def closeEvent(self, event):
        dialog = CloseDialog(self)
        result = dialog.exec()

        if result == QDialog.Accepted:
            event.accept()  # Proceed with closing
            #print('accept close')
            self.flag = False
        else:
            event.ignore()  # Cancel close'''
   
    def confirm_cancel(self):
        system = platform.system()
        path = '/mnt/c/Users/' if system == 'Linux' else 'C:/Users'
        reply = QMessageBox.question(
            self,
            "Confirm Cancel",
            "Continue with default folder location?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            ##print('yes reply')
            self.create_dir(path)
            self.reject()
        else:
            ##print("no reply")
            pass

    def get_selected_path(self):
        return self.path_edit1.text()
    
    def submit_handler(self):
        #new_folder = self.path_edit2.text()
        dir = self.get_selected_path()
        full_path = None
        if dir:
            full_path = self.path_edit1.text()
            dir_creator = QDir()
            new_dir = dir_creator.mkdir(full_path)
            self.message.show_message(f'New Folder creation successful!')
            self.accept()
            ##print(dir)
        else:
            self.message.show_message(f'New folder {full_path} unsuccessful.')
            #print('New folder unsuccessful.')

        


# Test dialog
'''
if __name__ == "__main__":
    app = QApplication(sys.argv)
    wizard = InstallWizardDialog()
    wizard.exec()
'''
