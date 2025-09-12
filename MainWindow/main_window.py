import sys 
#from PySide6.QtWidgets import QWidget, QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout, QSizePolicy
from start_page.league_view_players import LeagueViewPlayers
from start_page.league_view_teams import LeagueViewTeams
from Add_Save.add_save_ui import Ui_Add_Save
from start_page.selection import Selection
from Mouse_Events.tree_event_filter import TreeEventFilter
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QPushButton, QDialog, QGroupBox, QButtonGroup, QMessageBox, QMainWindow
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import QIntValidator, QCloseEvent
from stat_dialog.stat_dialog_ui import Ui_StatDialog
from update_dialog.update_dialog_ui import UpdateDialog
from update_dialog.update_league import UpdateLeagueDialog
from League.linked_list import LinkedList
from remove.remove import RemoveDialog
from refresh.refresh import Refresh
from Styles.stylesheets import StyleSheets
from League.stack import Stack
from Undo.undo import Undo
from Message.message import Message
from InstallWizard.install_wizard import InstallWizardDialog
from CloseDialog.close import CloseDialog

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.selected = None
        self.league = LinkedList()
        self.styles = StyleSheets()
        self.stack = Stack()
        self.undo = Undo(self.stack, self.league)
        #self.file_dir = None
        self.message = Message(self.styles, parent=self)
        self.setStyleSheet(self.styles.main_styles)
        self.theme = None
        
        self.title = "Welcome to the league"
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 800, 600)  # Set window size
        self.setObjectName("Main Window") 
         
         # ---------------------------------------- install wizard setup ----------------------------------- #

        self.exec_wizard() 
        dir_path = self.wizard.get_selected_path()
        self.file_dir = dir_path 

        self.league_view_teams = LeagueViewTeams(self.league, self.styles, self.stack, self.file_dir, self.message, parent=self)
        self.league_view_players = LeagueViewPlayers(self.league_view_teams, self.selected, self.league, self.styles, self.undo, self.file_dir, self.message, parent=self)

        self.leaderboard = self.league_view_players.leaderboard

        # refresh main view after removal from league view
        # restores all league items to main view
        self.refresh = Refresh(self.league, self.league_view_teams, self.league_view_players, self.leaderboard)

        self.tree_widgets = [self.league_view_players.tree1_top, self.league_view_players.tree2_top, self.league_view_teams.tree1_bottom, self.league_view_teams.tree2_bottom]
        self.event_filter = TreeEventFilter(self.tree_widgets, self)
        self.set_event_filter()

        # exp stlying 
        # deprecated, style inherited through parents
        #for el in self.tree_widgets:
            #el.setStyleSheet(self.styles.modern_styles)

        # ------------------------------------------------------------- #

        # button group box - all buttons
        self.button_group_bottom = QGroupBox('Modify', self)
        #self.button_group_bottom.setGeometry(QRect(1,1,50,75))

        # list buttons 
        self.buttons_bottom = []
        self.v_layout_buttons_bottom = QVBoxLayout()

         # ------------------------------------------------------------- #

        # Stat button to the right of second tree widget at the bottom
        self.btn_stat = QPushButton("Stat")
        self.btn_stat.clicked.connect(lambda: self.get_item(self.setup_stat_ui))
        self.v_layout_buttons_bottom.addWidget(self.btn_stat)
        self.buttons_bottom.append(self.btn_stat)
        #self.button_group_bottom.addButton(self.btn_stat)

        #self.stat_ui = Ui_StatDialog(self.league, self.message, self.selected, self)
        self.stat_widget = QDialog(self)
        self.stat_layout = QVBoxLayout(self.stat_widget)
        #self.stat_widget.setStyleSheet(self.styles.main_styles)
        
         # ------------------------------------------------------------- #
        
        # update button to the right of the second tree widget at the bottom
        self.btn_update = QPushButton("Update")
        self.v_layout_buttons_bottom.addWidget(self.btn_update)
        self.buttons_bottom.append(self.btn_update)
        #self.button_group_bottom.addButton(self.btn_update)
        self.btn_update.clicked.connect(lambda: self.get_item(self.setup_update_ui))

         # ------------------------------------------------------------- #

        # remove button to the right of the second tree widget at the bottom
        self.btn_remove = QPushButton("Remove")
        self.v_layout_buttons_bottom.addWidget(self.btn_remove)
        self.buttons_bottom.append(self.btn_remove)
        self.btn_remove.clicked.connect(lambda: self.get_item(self.setup_remove_ui))

         # ------------------------------------------------------------- #

        # refresh button to the right of the second tree widget at the bottom
        self.btn_refresh = QPushButton("Refresh")
        self.v_layout_buttons_bottom.addWidget(self.btn_refresh)
        self.buttons_bottom.append(self.btn_refresh)
        #self.button_group_bottom.addButton(self.btn_refresh)
        self.btn_refresh.clicked.connect(self.refresh_view)

         # ------------------------------------------------------------- #

        # buttons

        self.button_group_bottom.setLayout(self.v_layout_buttons_bottom)


        self.main_button_layout = QVBoxLayout()

        self.main_button_layout.addWidget(self.league_view_players.button_group)
        self.main_button_layout.addWidget(self.button_group_bottom)

         # -------------------------------------------------------------- # 

        self.main_lv_layout = QVBoxLayout()

        self.main_lv_layout.addLayout(self.league_view_players.top_layout)
        self.main_lv_layout.addLayout(self.league_view_teams.bottom_layout)

         # -------------------------------------------------------------- #

        self.main_h_layout = QHBoxLayout()

        self.main_h_layout.addLayout(self.main_lv_layout)
        self.main_h_layout.addLayout(self.main_button_layout)

        self.setLayout(self.main_h_layout) 


        # setup league basics on program start
        self.setup_league_ui()
        self.title = f"Welcome to {self.league.get_name()}" if self.league.get_name() else "Welcome to the league"
        self.setWindowTitle(self.title)

        # ----------------------------------------------------------------------------- #

        #self.close_dialog.custom_close()

        # ----------------------------------------------------------------------------- #
    def closeEvent(self, event=QCloseEvent):
        reply = QMessageBox.question(
                self,
                "Confirm Close",
                "Are you sure you want to quit?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
            
        if reply == QMessageBox.StandardButton.No:
            event.ignore()
            self.show()
            #self.show()

    
    def exec_wizard(self):
        #self.wizard.center_over_parent()
        self.showMaximized()
        #self.setStyleSheet(self.styles.modern_styles)
        self.show()
        
        self.wizard = InstallWizardDialog(parent=self)
        self.wizard.resize(self.wizard.sizeHint())  # Ensure layout is applied
        self.wizard.center_over_parent() 
        self.wizard.exec()      # Now center it

        if self.wizard.flag == False:
            QApplication.quit()
            sys.exit()
        #dir_path = self.wizard.get_selected_path()
        #self.file_dir = dir_path
        ##print(f'file dir-main window: {self.file_dir}')

    def set_event_filter(self):
        for tree in self.tree_widgets:
            tree.viewport().installEventFilter(self.event_filter)
            tree.setSelectionMode(QTreeWidget.SingleSelection)
    
    def selected_is_none(self):
        locs = [self.league_view_players.tree1_top, self.league_view_players.tree2_top, self.league_view_teams.tree1_bottom, self.league_view_teams.tree2_bottom]
        ret = None
        curr = None
        for el in locs:
            curr = el.currentItem()
            if curr: 
                return (curr, el)
        return None
    
    def get_item(self, func):
        locs = [self.league_view_players.tree1_top, self.league_view_players.tree2_top, self.league_view_teams.tree1_bottom, self.league_view_teams.tree2_bottom]
        name = None
        team = None 
        avg = None
        
        if not self.selected_is_none():
            ##print('league')
            ##print('func:', func.__name__)
            func_name = func.__name__
            
            if func_name == 'setup_update_ui':
                self.setup_league_ui()

            elif func_name == 'setup_stat_ui':
                self.setup_stat_ui()
            
        elif self.selected_is_none():
            curr = self.selected_is_none()[0]
            obj_name = self.selected_is_none()[1].objectName()
            # ##print('obj name:', obj_name)
            
            if "top" in obj_name:
                name = curr.text(0)
                team = curr.text(1)
                avg = curr.text(2)
                self.selected = [name, team, avg]
            else:
                team = curr.text(0)
                avg = curr.text(1)
                ###print('avg', avg, len(avg))
                if len(avg) > 5:
                    avg = avg[8:-1]
                self.selected = [team, avg]
            ###print(self.selected)
            #self.setup_stat_ui()
            func()
        ##print("nothing selected")
    
    def setup_stat_ui(self):
        ##print("view stats")
        
        #print('selected before:', self.selected)
        self.stat_ui = Ui_StatDialog(self.league, self.message, self.selected, self.styles, parent=self.stat_widget)
        self.stat_ui.get_stats(self.selected)
        self.stat_ui.exec()
        #print('selected after:', self.selected)
        
        #self.stat_widget.setWindowTitle(f"Stats")
        #self.stat_widget.setModal(True)

        #self.stat_layout = QVBoxLayout()
        #self.stat_layout.addWidget(self.stat_ui)

        #self.stat_widget.setLayout(self.stat_layout)
        #self.stat_ui.populate_stats(self.selected)
        
        #self.stat_widget.show()
    
    def setup_update_ui(self):
        ##print("view update")
        dialog = UpdateDialog(self.league, self.selected, self.leaderboard, self.league_view_teams, self.stack, self.undo, self.file_dir, self.styles, self.message, parent=self)
        dialog.exec()
    
    def setup_remove_ui(self):
        ##print("remove item")
        dialog = RemoveDialog(self.league, self.selected, self.leaderboard, self.league_view_teams, self.league_view_players, parent=self)
        dialog.exec()
    
    def setup_league_ui(self):
        dialog = UpdateLeagueDialog(self.league, self.selected, self.message, self.leaderboard, self.league_view_teams, self.stack, self.undo, self.styles, parent=self)
        dialog.exec()

    def refresh_view(self):
        self.refresh.restore_all()
    
    