from PySide6.QtWidgets import QWidget, QDialog, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QRadioButton, QButtonGroup, QHBoxLayout, QSizePolicy, QTreeWidgetItem
from PySide6.QtGui import QIntValidator
from PySide6.QtCore import QCoreApplication, Qt, QTimer
from src.ui.views.league_view_teams import LeagueViewTeams

from src.ui.styles.stylesheets import StyleSheets
from src.ui.dialogs.stat_dialog_ui import Ui_StatDialog
import random

class UpdatePitchingDialog(QDialog):
    def __init__(self, league, selected, leaderboard, lv_teams, stack, undo, message, parent=None):
        super().__init__(parent)
        self.league = league
        self.selected = selected
        self.leaderboard = leaderboard
        self.lv_teams = lv_teams
        self.leaderboard_AVG = []
        self.stack = stack
        self.undo = undo
        self.message = message
        self.setWindowTitle("Update Pitching")
        self.resize(400, 300)
        self.styles = StyleSheets()
        #self.setStyleSheet(self.styles.modern_styles)
        
        # Widgets
        self.int_label = QLabel("Enter value:")
        self.int_label.setAlignment(Qt.AlignCenter)
        self.int_input = QLineEdit()
        self.int_input.setValidator(QIntValidator())
        self.int_input.setAlignment(Qt.AlignCenter)

        # submit / undo buttons layout 
        self.button_layout = QHBoxLayout()    

        # ----- Submit Button -----
        self.submit_button = QPushButton("Submit")
        self.submit_button.setFixedWidth(100)
        self.submit_button.clicked.connect(self.update_stats)

        # ----- Undo Button ------
        self.undo_button = QPushButton("Undo")
        self.undo_button.setFixedWidth(100)
        self.undo_button.clicked.connect(self.undo_stat)

        # ----- current view team -------- 
        self.view_team_button = QPushButton("Current\nView")
        self.view_team_button.setFixedWidth(150)
        self.view_team_button.clicked.connect(self.view_player_stats)

        self.button_layout.addWidget(self.submit_button, alignment=Qt.AlignCenter)
        self.button_layout.addWidget(self.undo_button, alignment=Qt.AlignCenter)
        self.button_layout.addWidget(self.view_team_button, alignment=Qt.AlignCenter)

        form_layout = QVBoxLayout()
        form_layout.addWidget(self.int_label)
        form_layout.addWidget(self.int_input)

        form_widget = QWidget()
        form_widget.setLayout(form_layout)
        form_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

                            # -----------------------------------------------------------------------------------------------------# 

        # Right side: Radio Buttons in a group
        self.radio_group = QButtonGroup(self)
        self.radio_buttons = []

        #options = ["default"]

        #options = ["games played", "wins", "losses", "games started", "games completed", "shutouts", "saves", "save opportunities", "IP", "at bats", "hits", "runs", "ER", "HR", "HB", "walks", "SO"]

        self.radio_buttons_layout = QVBoxLayout()
        self.radio_buttons_layout.setAlignment(Qt.AlignTop)

        '''for i in range(len(options)):
            radio = QRadioButton(f"{options[i]}")
            if options[i] == 'games played':
                radio.setChecked(True)
            else:
                radio.setEnabled(False)
            self.radio_group.addButton(radio, i)
            self.radio_buttons.append(radio)
            self.radio_buttons_layout.addWidget(radio)'''

        # setup buttons - stat check 
        self.radio_btns_setup()
        
        # Container widget for the radio buttons (optional)
        self.radio_buttons_widget = QWidget()
        self.radio_buttons_widget.setLayout(self.radio_buttons_layout)

                                # --------------------------------------------------------------------------------------------------------------------- #
        
                                # --------------------------------------------------------------------------------------------------------------------- #


        # Horizontal layout: form on the left, radios on the right
        content_layout = QHBoxLayout()
        content_layout.addStretch()
        content_layout.addWidget(form_widget)
        content_layout.addSpacing(40)  # spacing between form and radios
        content_layout.addWidget(self.radio_buttons_widget)
        content_layout.addStretch()

         # ----- Main Layout -----
        main_layout = QVBoxLayout()
        main_layout.addStretch()
        main_layout.addLayout(content_layout)
        main_layout.addSpacing(20)
        main_layout.addLayout(self.button_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)
    
    # experimental
    # check for existing stats
    # enable/disable radio btns according to existing stats
    def radio_btns_stat_check(self):
        player, team, num = self.selected
        find_team = self.league.find_team(team)
        if find_team:
            find_player = find_team.get_player(player)
            if find_player:
                games_played = find_player.games_played 
                if games_played > 0:
                    #print('stats exist')
                    self.enable_buttons()
    
    def radio_btns_setup(self):
        options = ["default"]
        options = ["games played", "wins", "losses", "games started", "games completed", "shutouts", "saves", "save opportunities", "IP", "at bats", "hits", "runs", "ER", "HR", "HB", "walks", "SO"]
        for i in range(len(options)):
            radio = QRadioButton(f"{options[i]}")
            if options[i] == 'games played':
                radio.setChecked(True)
            else:
                radio.setEnabled(False)
            self.radio_group.addButton(radio, i)
            self.radio_buttons.append(radio)
            self.radio_buttons_layout.addWidget(radio)
        self.radio_btns_stat_check()

    
    def enable_buttons(self):
        for el in self.radio_buttons:
            el.setEnabled(True)

    def get_player_stat(self):
        # radio button selection 
        selection = self.radio_group.checkedButton().text()
        return selection
    
    def set_new_stat_pitcher(self, stat, val, player):
        match stat:
            case 'wins':
                player.set_wins(val)
            case 'losses':
                player.set_losses(val)
            case 'games started':
                player.set_games_started(val) 
            case 'games completed':
                player.set_games_completed(val)
            case 'games played':
                player.set_games_played(val)
                self.enable_buttons()
            case 'shutouts':
                player.set_shutouts(val) 
            case 'saves':
                player.set_saves(val) 
            case 'save opportunities':
                player.set_save_ops(val) 
            case 'at bats':
                player.set_p_at_bats(val)
            case 'IP':
                player.set_ip(val) 
            case 'hits':
                player.set_p_hits(val) 
            case 'runs':
                player.set_p_runs(val) 
            case 'ER':
                player.set_er(val) 
            case 'HR':
                player.set_p_hr(val)
            case 'HB':
                player.set_p_hb(val) 
            case 'walks':
                player.set_p_bb(val) 
            case 'SO':
                player.set_p_so(val)

    def reformat_stack_stat(self, stat):
        match stat:
            case 'wins':
                return 'wins'
            case 'losses':
                return 'losses'
            case 'games started':
                return 'games_started' 
            case 'games completed':
                return 'games_completed' 
            case 'games played':
                return 'games_played'
            case 'shutouts':
                return 'shutouts' 
            case 'saves':
                return 'saves'
            case 'save opportunities':
                return 'save_ops'
            case 'at bats':
                return 'p_at_bats'
            case 'IP':
                return 'ip' 
            case 'hits':
                return 'p_hits'
            case 'runs':
                return 'p_runs' 
            case 'ER':
                return 'er'
            case 'HR':
                return 'p_hr'
            case 'HB':
                return 'p_hb' 
            case 'walks':
                return 'p_bb' 
            case 'SO':
                return 'p_so'

    def update_stats(self):
        stat = None
        val = None

        try:
            stat = self.get_player_stat()
            val = int(self.int_input.text())
            if not stat or not val:
                self.message.show_message("Must select a stat and enter value.")
                #QMessageBox.warning(self, "Input Error", "Must select a stat and enter value.")
                return
        except:
            self.message.show_message("Must enter a number value to update stat.")
            #QMessageBox.warning(self, "Input Error", "Must enter a number value to update stat.")
            return

        player, team, num = self.selected
        find_team = self.league.find_team(team)
        find_player = find_team.get_player(player)
        
        ###print(stat, val, find_player)

        ##print('before:', find_player, "\n")
        stat_stack = self.reformat_stack_stat(stat)
        # new_node = NodeStack(obj, team, stat, prev, func, flag, player=None)
        # stat hierarchy:  
            # radio buttons options 
            # radio selection 
            # exact player attr/stat passed to stack node 
            # stat passed to set new stat 
            # stat updated on player instance
        self.stack.add_node(find_player, team, stat_stack, getattr(find_player, stat_stack), self.set_new_stat_pitcher, 'player')
        ##print(self.stack)
        self.set_new_stat_pitcher(stat, val, find_player)

        self.refresh_player_pitching(find_player, find_team)

        ##print('after:', find_player, "\n")

        #self.leaderboard.refresh_leaderboard(find_player)
        #find_team.set_bat_avg()

        #self.refresh_leaderboard(find_team, self.lv_teams.tree2_bottom)
        #self.insert_end_avg(find_team)
        
    def refresh_player_pitching(self, player, team):
        player.set_era()
        player.set_WHIP()
        player.set_p_avg()
        player.set_k_9() 
        player.set_bb_9()
        team.set_team_era()
        
    # deprecated
    def rand_avg(self):
        rand = random.randint(100, 1000)
        rand /= 1000 
        rand_str = str(rand)
        ###print('rand avg:', rand)
        return rand_str

    # deprecated
    def rand_wl(self):
        w = random.randint(0,100)
        l = 100 - w
        wl = w / 100
        ret = (w, l, wl)
        ###print("wl str:", wl_str, type(wl_str))
        return str(ret)
    
    def undo_stat(self):
        player, team, avg = self.selected

        find_team = self.league.find_team(team)
        find_player = find_team.get_player(player)

        self.undo.undo_exp()

        self.refresh_player_pitching(find_player, find_team)
    
    # deprecated
    def view_player_stats_1(self):
        ##print("view stats")
        ###print('selected:', self.selected)
        #self.stat_ui.setupUi(self.stat_widget)
        self.stat_ui = Ui_StatDialog(self.league, self.message, self.selected, self.styles, parent=self.stat_widget)
        #self.stat_ui.populate_stats(self.selected)
        self.stat_ui.get_stats(self.selected)
        self.stat_widget.exec()
    
    def view_player_stats(self):
        self.stat_widget = QDialog(self)
        self.stat_widget.setWindowTitle("Stats")
        self.stat_widget.setModal(True)
        self.stat_layout = QVBoxLayout(self.stat_widget)
       
        #print('selected pitching:', self.selected)

        self.stat_ui = Ui_StatDialog(self.league, self.message, self.selected, self.styles, parent=self.stat_widget)
        
        self.stat_ui.get_stats(self.selected)

        self.stat_ui.exec()



    
