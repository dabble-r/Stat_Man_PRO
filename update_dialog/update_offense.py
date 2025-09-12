from PySide6.QtWidgets import QWidget, QDialog, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QRadioButton, QButtonGroup, QHBoxLayout, QSizePolicy, QTreeWidgetItem
from PySide6.QtGui import QIntValidator
from PySide6.QtCore import QCoreApplication, Qt, QTimer
from start_page.league_view_teams import LeagueViewTeams

from Styles.stylesheets import StyleSheets
from League.node import NodeStack
from stat_dialog.stat_dialog_ui import Ui_StatDialog
import random

class UpdateOffenseDialog(QDialog):
    def __init__(self, league, selected, leaderboard, lv_teams, stack, undo, styles, message, parent=None):
        super().__init__(parent)
        self.league = league
        self.selected = selected
        self.leaderboard = leaderboard
        self.lv_teams = lv_teams
        self.leaderboard_AVG = []
        self.stack = stack
        self.undo = undo
        self.styles = styles
        self.message = message
        #print('update msg isnt', self.message)
        self.setWindowTitle("Update Offense")
        self.resize(400, 300)
        #self.setStyleSheet(self.styles.modern_styles)
        
        # Widgets
        self.int_label = QLabel("Enter value:")
        self.int_label.setAlignment(Qt.AlignCenter)
        self.int_input = QLineEdit()
        self.int_input.setValidator(QIntValidator())
        self.int_input.setAlignment(Qt.AlignCenter)

        # button layout 
        self.button_layout = QVBoxLayout()

        # ----- Submit Button -----
        self.submit_button = QPushButton("Submit")
        self.submit_button.setFixedWidth(125)
        self.submit_button.clicked.connect(self.update_stats)

        # -------- Undo Button -------
        self.undo_button = QPushButton("Undo")
        self.undo_button.setFixedWidth(100)
        self.undo_button.clicked.connect(self.undo_stat)

        # --------curr stat snapshot ------- 
        self.view_player_button = QPushButton("Current\nView")
        self.view_player_button.setFixedWidth(150)
        self.view_player_button.clicked.connect(self.view_player_stats)

        self.button_layout.addWidget(self.submit_button, alignment=Qt.AlignCenter)
        self.button_layout.addWidget(self.undo_button, alignment=Qt.AlignCenter)
        self.button_layout.addWidget(self.view_player_button, alignment=Qt.AlignCenter)

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

        #options = ["at bat", "hit", "bb", "so", "hr", "rbi", "runs", "singles", "doubles", "triples", "sac fly"]

        self.radio_buttons_layout = QVBoxLayout()
        self.radio_buttons_layout.setAlignment(Qt.AlignTop)

        '''for i in range(len(options)):
            radio = QRadioButton(f"{options[i]}")
            if options[i] == 'at bat':
                radio.setChecked(True) 
            else:
                radio.setEnabled(False)
            self.radio_group.addButton(radio, i)
            self.radio_buttons.append(radio)
            self.radio_buttons_layout.addWidget(radio)'''
        
        self.radio_btns_setup()

        # Container widget for the radio buttons (optional)
        self.radio_buttons_widget = QWidget()
        self.radio_buttons_widget.setLayout(self.radio_buttons_layout)

                                # ---------------------------------------------------------------------------------------------------------------------#
                                                                # stat UI and widget setup #
        self.stat_widget = QDialog(self)
        self.stat_widget.setWindowTitle(f"Stats")
        self.stat_widget.setModal(True)
        self.stat_layout = QVBoxLayout(self.stat_widget)
        #self.stat_ui = Ui_StatDialog(self.league, self.message, self.selected, self.stat_widget)
        #self.stat_widget.setStyleSheet(self.styles.main_styles)

                                # ---------------------------------------------------------------------------------------------------------------------#

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
        main_layout.addLayout(self.button_layout, stretch=5)
        main_layout.addStretch()

        self.setLayout(main_layout)

                        #----------------------------------------------------------------------------------------------------------------#
    # experimental
    # check for existing stats
    # enable/disable radio btns according to existing stats
    def radio_btns_stat_check(self):
        player, team, num = self.selected
        find_team = self.league.find_team(team)
        if find_team:
            find_player = find_team.get_player(player)
            if find_player:
                at_bat = find_player.at_bat 
                if at_bat > 0:
                    print('stats exist')
                    self.enable_buttons()
    
    def radio_btns_setup(self):
        options = ["default"]
        options = ["hit", "bb", "hbp", "so", "hr", "rbi", "runs", "singles", "doubles", "triples", "sac fly", "fielder's choice"]

        for i in range(len(options)):
            radio = QRadioButton(f"{options[i]}")
            if options[i] == 'hit':
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
    
    def set_new_stat_player(self, stat, val, player):
        
        match stat:
            case 'hit':
                player.set_hit(val)
                self.enable_buttons()
            case 'bb':
                player.set_bb(val)
            case 'hbp':
                player.set_hbp(val)
            case 'so':
                player.set_so(val)
            case 'hr':
                player.set_hr(val)
            case 'rbi':
                player.set_rbi(val)
            case 'runs':
                player.set_runs(val)
            case 'singles':
                player.set_singles(val)
            case 'doubles':
                player.set_doubles(val)
            case 'triples':
                player.set_triples(val)
            case 'sac_fly':
                player.set_sac_fly(val)
            case "fielder's choice": 
                player.set_fielder_choice(val)

    def update_stats(self):
        stat = None
        val = None

        try:
            stat = self.get_player_stat()
        except:
            self.message.show_message("Must select a player stat to update.")
            #QMessageBox.warning(self, "Input Error", "Must select a player stat to update.")
            return

        if not stat or not self.int_input.text():
            self.message.show_message("Please enter value and select stat.")
            #QMessageBox.warning(self, "Input Error", "Please enter value and select stat.")
            return
        
        val = int(self.int_input.text())

        player, team, avg = self.selected
        find_team = self.league.find_team(team)
        find_player = find_team.get_player(player)

        #print('player msg inst - update', find_player.message)

        ##print("stat:", stat)
        #print('before:', find_player, "\n")

        '''if stat == 'sac fly' or stat == 'at bat':
            stat = stat.replace(" ", "_")
        elif stat == 'plate appearance':
            stat = 'pa'
        elif stat == "fielder's choice":
            stat = "fielder_choice"'''

        # new_node = NodeStack(obj, team, stat, prev, func, flag, player=None)
        # stat hierarchy:  
            # radio buttons options 
            # radio selection 
            # exact player attr/stat passed to stack node 
            # stat passed to set new stat 
            # stat updated on player instance
        stat = self.stat_lst(stat, val)
        statType = stat[-1] if type(stat) == list else stat
        

        # add to stack node 
        # player obj, team obj, stat list (pa or ab and stat), curr attr/state of stat, bound method called, player string flag
        self.stack.add_node(find_player, team, stat, getattr(find_player, statType), self.set_new_stat_player, 'player')

        #print('set new stat:', stat)
        self.set_new_stat_player(statType, int(val), find_player)

        self.refresh_player(find_player)

        #print('after:', find_player, "\n")

        self.leaderboard.refresh_leaderboard(find_player)
        
        find_team.set_bat_avg()

        self.refresh_leaderboard(find_team, self.lv_teams.tree2_bottom)
        #self.insert_end_avg(find_team)

    def refresh_player(self, player):
        player.set_AVG()
        player.set_BABIP()
        player.set_SLG()
        player.set_ISO()
        player.set_OBP()
    
    def refresh_team(self, team):
        '''self.wins = 0 
        self.losses = 0
        self.games_played = 0
        self.wl_avg = 0
        self.bat_avg = 0'''
        team.set_wl_avg()
        team.set_bat_avg()
    
    def refresh_leaderboard(self, team_upd, view): # new player type -> tuple or list
        ##print('new team:', new_team)
        self.leaderboard_AVG = self.league.get_all_avg()
        self.no_dups(team_upd)
        self.add_leaderboard_list(team_upd, self.leaderboard_AVG)
        ##print("leaderboard:", self.leaderboard_list)
        self.sort_leaderboard(self.leaderboard_AVG)
        self.insert_widget(view, self.leaderboard_AVG)
    
    # deprecated
    def rand_avg(self):
        rand = random.randint(100, 1000)
        rand /= 1000 
        rand_str = str(rand)
        ##print('rand avg:', rand)
        return rand_str

    # deprecated
    def rand_wl(self):
        w = random.randint(0,100)
        l = 100 - w
        wl = w / 100
        ret = (w, l, wl)
        ##print("wl str:", wl_str, type(wl_str))
        return str(ret)
    
    def no_dups(self, team):
        for el in self.leaderboard_AVG:
            if el[0] == team.name:
                indx = self.leaderboard_AVG.index(el)
                self.leaderboard_AVG.pop(indx)
    
    def add_leaderboard_list(self, team_upd, lst):
        name = team_upd.name 
        roster = team_upd.max_roster
        avg = team_upd.get_bat_avg()
        lst.append((name, roster, avg))

    def sort_leaderboard(self, lst):
        lst.sort(key=self.my_sort)
        return lst
        
    def my_sort(self, x):
        return x[2]
    
    def insert_widget(self, view, lst):
        ##print(self.leaderboard_list, type(self.leaderboard_list))
        view.clear()
        #print('avg leaders:', self.leaderboard_AVG)
        for el in lst:
            #print("list el:", el)
            item = QTreeWidgetItem([el[0], str(el[2])])
            item.setTextAlignment(0, Qt.AlignCenter)
            item.setTextAlignment(1, Qt.AlignCenter)
            item.setTextAlignment(2, Qt.AlignCenter)
            view.insertTopLevelItem(0, item)
    
    def stat_lst(self, stat, val):
        """
        if stat == 'sac fly' or stat == 'at bat':
            stat = stat.replace(" ", "_")
        elif stat == 'plate appearance':
            stat = 'pa'
        elif stat == "fielder's choice":
            stat = "fielder_choice"
        """
        def check(str):
            lst = ["hit", "bb", "hbp", "so", "sac fly", "fielder's choice"]
            if str in lst:
                return True 
            return False
        
        one = ["pa"]
        two = ["pa", "at_bat"]
        if check(stat):
            if stat == "hit":
                two += [val, "hit"]
                return two
            elif stat == "bb":
                one += [val, "bb"]
                return one
            elif stat == "hbp":
                one += [val, "hbp"]
                return one
            elif stat == "so":
                one += [val, "so"]
                return one 
            elif stat == "sac fly":
                one += [val, "sac_fly"]
                return one
            elif stat == "fielder's choice":
                one += [val, "fielder_choice"]
                return one
            
        else:
            return stat

    def undo_stat(self):
        player, team, avg = self.selected
        find_team = self.league.find_team(team)
        find_player = find_team.get_player(player)

        self.undo.undo_exp()

        self.refresh_player(find_player)
        self.refresh_team(find_team)
        self.leaderboard.refresh_leaderboard(find_player)
        self.refresh_leaderboard(find_team, self.lv_teams.tree2_bottom)

    def view_player_stats(self):
        #print("view stats")
        ##print('selected:', self.selected)
        
        #self.stat_ui.populate_stats(self.selected)
        # last attmept - not functional for player
        #self.stat_ui.get_stats(self.selected)
        self.stat_ui = Ui_StatDialog(self.league, self.message, self.selected, self.styles, self.stat_widget)
        self.stat_ui.get_stats(self.selected)
        self.stat_ui.exec()
