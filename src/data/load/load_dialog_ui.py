from PySide6.QtWidgets import QDialog, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import QMetaObject
from src.data.load.load import load_all_from_db
from src.data.load.load_csv import load_all_csv_to_db
import math 
import random

class Ui_LoadDialog:
    def __init__(self, league, message, file_dir, csv_path, parent: QDialog):
        self.league = league
        self.message = message
        self.file_dir = file_dir
        self.csv_path = csv_path
        self.parent = parent
        # Build DB path under file_dir/DB using league name when available
        league_name = self.league.admin['Name'] if self.league.admin['Name'] else None
        self.db = f"{self.file_dir}/DB/{league_name}.db" if league_name else None
        self.setupUi(parent)

    def setupUi(self, SaveDialog: QDialog):
        SaveDialog.setObjectName("SaveDialog")
        SaveDialog.resize(400, 300)

        # Layout
        if SaveDialog.layout() is None:
            self.layout = QVBoxLayout(SaveDialog)
        else:
            self.layout = SaveDialog.layout()

        # Label
        self.label = QLabel(SaveDialog)
        self.label.setObjectName("label")
        self.layout.addWidget(self.label)

        # Buttons
        self.button_layout = QHBoxLayout()
        self.button_ok = QPushButton("OK", SaveDialog)
        self.button_ok.setObjectName("button_ok")
        self.button_ok.clicked.connect(self.button_ok_handler)

        self.button_cancel = QPushButton("Cancel", SaveDialog)
        self.button_cancel.setObjectName("button_cancel")
        self.button_cancel.clicked.connect(self.button_cancel_handler)

        self.button_layout.addStretch()
        self.button_layout.addWidget(self.button_ok)
        self.button_layout.addWidget(self.button_cancel)
        self.layout.addLayout(self.button_layout)

        self.retranslateUi(SaveDialog)
        QMetaObject.connectSlotsByName(SaveDialog)

    def retranslateUi(self, SaveDialog):
        SaveDialog.setWindowTitle("Save Progress")
        self.label.setText("Do you want to save your progress?")

    def button_ok_handler(self):
        # Prefer CSV import to instantiate league/teams/players, then refresh UI
        csv_dir = f"{self.file_dir}/CSV"
        if self.db:
            load_all_csv_to_db(self.league, csv_dir, self.db, self.parent.stack, parent=self.parent)
        else:
            self.message.show_message("Please set a league name before loading from CSV.")
            return

        self.parent.accept()
        
    def button_cancel_handler(self):
        print("Save canceled.")
        self.parent.reject()
    