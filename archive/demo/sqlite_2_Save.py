from PySide6.QtWidgets import QMessageBox, QDialog
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFontMetrics
import csv
import os

class StyleSheets():
    def __init__(self):
        #self.main_styles = self.get_monochrome_style()
        self.main_styles = self.get_monochrome_style() 
    
    def get_monochrome_style(self):
        return''' 
        * {
            font-family: "Segoe UI", sans-serif;
            font-size: 20px;
            color: #1a1a1a;
            background-color: #eeeeee;
        }

        QDialog {
            border: 2px solid #444444;
        }

        QGroupBox {
            border: 2px solid #444444;
            border-radius: 10px;
            margin-top: 10px;
            padding: 10px;
            background-color: #f0f0f0;
        }

        QLabel {
            font-size: 20px;
            font-weight: bold;
            color: #000000;
        }

        
        QLineEdit {
            background-color: #ffffff;
            border: 1px solid #666666;
            border-radius: 4px;
            padding: 6px;
            color: #1a1a1a;
            font-size: 16px;
        }

        QCheckBox {
            font-size: 18px;
        }

        
        QPushButton {
            background-color: rgba(50, 50, 50, 0.9);
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
        }

        
        QPushButton:hover {
            background-color: rgba(30, 30, 30, 0.5);
        }

        
        QPushButton:pressed {
            background-color: rgba(90, 90, 90, 1.0);
        }'''
   
class Message():
  def __init__(self, styles, parent=None):
    self.parent = parent
    self.box = QMessageBox(parent=self.parent)
    self.styles = styles
    self.box.setWindowTitle('Update Message')
    self.box.setStandardButtons(QMessageBox.Ok)
    #self.box.setStyleSheet(self.styles.modern_styles)

  def set_box_text(self, text):
    self.box.setText(text)

  def show_message(self, text):
    self.set_box_text(text)
    self._resize_to_fit_text(text)

    # show not functional - non-modal
    #self.box.show()

    # message exec - modal
    self.box.exec()
  
  def _resize_to_fit_text(self, text):
        # Use font metrics to calculate text size
        font_metrics = QFontMetrics(self.box.font())
        text_width = font_metrics.horizontalAdvance(text)
        text_height = font_metrics.height()

        # Add padding and set minimum size
        padding = 100  # Adjust as needed
        min_width = max(250, text_width + padding)
        min_height = 150  # You can also adjust based on line count

        self.box.setMinimumSize(min_width, min_height)

# there is no update functionality 
# there is only save and create new teams and players from linked list 


# iterate over league linked list 
# create new team for each node 
  # create and save to db

# create new player for each player in team players list 
  # create and save to db 

import sqlite3
from PySide6.QtWidgets import QMessageBox, QDialog
import math
import json
import hashlib

#from team import beef, rougarou

class LinkedList():
  COUNT = 0

  @classmethod
  def get_count(cls):
    return cls.COUNT 
  
  @classmethod
  def set_count(cls):
    cls.COUNT += 1
  
  def __init__(self, message=None, head=None, name=None, ):
    self.admin = {
      "League Name": None,
      "Commissioner": None,
      "Treasurer": None,
      "Communications": None,
      "Historian": None,
      "Recruitment": None,
      "Season Start": None,
      "Season End": None
    }

    self.date = None
    self.season = None
    self.location = None
    self.head = head 
    self.name = name
    self.leagueID = self.get_hash()

    self.message = message

    # --------------------------------------------------------------- # 

  def format_decimal(self, num):
    return "{:.3f}".format(num)

  def __str__(self):
    ret = ''
    if LinkedList.COUNT == 0:
      ###print('No teams in league')
      return ret
    else:
      ret = "League\n"
      traverser = self.head
      while traverser is not None:
        tmp = f'Team: {traverser.team.name}\n'
        ret += tmp
        tmp = ''
        if traverser.next is not None:
          traverser = traverser.next
        else:
          return ret
      #ret += f'Team: {traverser.team.name}\n'
      return ret
  
  def get_hash(self):
    def indx(a, b):
        index = a.index(b)
        if index == 0:
            return 2 
        return index
    ord_lst = [sum(ord(x)*indx(self.name, x) for x in self.name)]
    return ord_lst.pop()
  
  def get_team_objs_barset(self):
    '''
    example temp: ('team1', 'Beef Sliders', [1,2,3,4,5])
    '''

    if self.COUNT == 0:
      return False
    
    traverser = self.head
    ret = []
    c_ret = [] 
    t_ret = []
    stat_ret = []

    while traverser is not None:
      indx = 1
      count = "team" + str(indx)
      team = traverser.team.name 
      hits = int(traverser.team.get_team_hits())
      so = int(traverser.team.get_team_so())
      runs = int(traverser.team.get_team_runs())
      era = float(traverser.team.get_team_era())
      k = int(traverser.team.get_team_k())
      avg = float(traverser.team.get_bat_avg())
      stats = [hits, so, runs, era, k, avg]

      if hits == 0:
        ##print('hits:', hits)
        return False

      c_ret.append(count)
      t_ret.append(team)
      stat_ret.append(stats)

      indx += 1

      if traverser.next is not None:
        traverser = traverser.next
      else:
        ret.append(t_ret)
        ret.append(stat_ret)
        return ret
      
    ret.append(t_ret) 
    ret.append(stat_ret)
    return ret
  
  def get_team_objs_barset_spec(self, lst):
    traverser = self.head
    ret = []
    c_ret = [] 
    t_ret = []
    stat_ret = []
    check_team = lst

    while traverser is not None:
      indx = 1
      count = "team" + str(indx)
      team = traverser.team.name 

      if team in check_team:
        hits = int(traverser.team.get_team_hits())
        so = int(traverser.team.get_team_so())
        runs = int(traverser.team.get_team_runs())
        era = float(traverser.team.get_team_era())
        k = int(traverser.team.get_team_k())
        avg = float(traverser.team.get_bat_avg())
        stats = [hits, so, runs, era, k, avg]

        if hits == 0:
          ###print('hits:', hits)
          return False

        c_ret.append(count)
        t_ret.append(team)
        stat_ret.append(stats)
        indx += 1

        if traverser.next is not None:
          traverser = traverser.next

        else:
          ret.append(t_ret)
          ret.append(stat_ret)
          return ret
        
      else:
        if traverser.next is not None:
          traverser = traverser.next
          
        else:
          ret.append(t_ret)
          ret.append(stat_ret)
          return ret

    ret.append(t_ret) 
    ret.append(stat_ret)
    return ret
  

  # deprecated
  def get_team_objs_lineseries(self):
    '''example temp: 
      ('team1', 'Beef Sliders', 0.432)
    '''
    if self.COUNT == 0:
      return None
    traverser = self.head
    ret = [(),(),()]
    while traverser is not None:
      indx = 1
      count = "team" + str(indx)
      team = traverser.team.name 
      avg = traverser.team.get_bat_avg()
      #temp = (count, team, avg)
      ret[0].append(count)
      ret[1].append(team)
      ret[2].append(avg)
      indx += 1
      if traverser.next is not None:
        traverser = traverser.next
      else:
        return ret
    #ret += f'Team: {traverser.team.name}\n'
    return ret
    
  def get_admin(self):
    ret = 'League Admin\n'
    ret += f" League Name: {self.admin['League Name']}\n"
    ret += f" Commissioner: {self.admin['Commissioner']}\n"
    ret += f" Historian: {self.admin['Historian']}\n"
    ret += f" Treasurer: {self.admin['Treasurer']}\n"
    ret += f" Recruitment: {self.admin['Recruitment']}\n"
    ret += f" Communications: {self.admin['Communications']}\n"
    ret += f" Season Start: {self.admin['Season Start']}\n"
    ret += f" Season End: {self.admin['Season End']}"
    return ret
  
  def return_dict(self, dict):
        ret = "" 
        ####print('return dict:', dict)
        for el in dict:
            ###print('return dict:', el)
            ret += f"{el}:{dict[el]}\n"
        return ret
          
  # team lineup 
  # list of tuples
  def format_dict(self, dict):
        ret = []
        ret_dict = self.return_dict(dict).split("\n")
        ####print(ret_dict)
        for el in ret_dict:
            # not necessary
            indx = el.find(":")
            el = el.replace(":", " ")
            val = el[:indx].strip()
            name = el[indx::].strip()
            ret.append((val, name))
            #temp = None
        ret.pop()
        return ret
        
  # team stats 
  # list of all team stats plus lineup as tuples
  def return_admin(self):
        admin = self.format_dict(self.admin)
        #admin.pop()
        ###print('return stats:', admin)
        return admin

  def ques_replace(self, attr, stat, parent):
    ###print("admin:\n", attr, stat)
    existing_val = getattr(self, attr)[stat]
    if existing_val:
      reply = QMessageBox.question(parent, "Input Error", f"Would you like to replace {existing_val} at {stat}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
      return reply 
    return None
    
    # --------------------------------------------------------------- # 
  

    # --------------------------------------------------------------- #
  
  def add_team(self, val):
    new_node = Node(val)
    if self.head == None:
      self.head = new_node 
      self.head.next = None
      LinkedList.set_count()
      return
    curr = self.head
    while curr.next != None:
      curr = curr.next
    curr.next = new_node
    new_node.next = None
    LinkedList.set_count()
    return
  
  def remove_team(self, target): 
      if self.head.team.name == target and LinkedList.COUNT == 1:
        self.head = None
        LinkedList.COUNT -= 1
        ####print(f'Removing {target}')
        return
      
      elif self.head.team.name != target and LinkedList.COUNT == 1:
        return
      
      if self.head.team.name == target and LinkedList.COUNT > 1:
        curr = self.head
        self.head = curr.next
        curr = None
        LinkedList.COUNT -= 1
        ####print(f'Removing {target}')
        return
      traverser = self.head
      prev = None
      while traverser is not None:
        if traverser.team.name == target:
            if prev is not None:
                prev.next = traverser.next
            else:
                self.head = traverser.next
                traverser = None
            LinkedList.COUNT -= 1
            return
        prev = traverser
        traverser = traverser.next
      return
      ####print('end of list')
  
  def find_team(self, target):
    traverser = self.head
    if traverser == None:
      ####print('No teams in league\n')
      return None
    if traverser.team.name == target:
      return traverser.team
    else:
      while traverser.next != None:
        if traverser.next.team.name == target:
          return traverser.next.team
        traverser = traverser.next 
    ####print('Team not found')
    return None
  
  def find_player(self, target):
    traverser = self.head 
    if traverser == None:
      return 
    if len(traverser.team.players) == 0:
      return 
    while traverser.next != None:
      for el in traverser.team.players:
        if el.name == target:
          return el 
        traverser = traverser.next
    return

  def view_all(self):
    if LinkedList.COUNT == 0:
      ###print('No teams in league')
      return ''
    else:
      ret = ''
      traverser = self.head 
      while traverser != None:
        ret += f'\nTeam: {traverser.team.name}\nPlayers: {[{x.name: x.positions[0]} for x in traverser.team.players]}'
        traverser = traverser.next
      return ret
    
    # --------------------------------------------------------------------- #

  def set_admin(self, attr, stat, val, parent):
    ###print('attr:', attr)
    ###print('stat:', stat)
    ###print('val:', val)
    if 'Season' in stat:
      self.admin[stat] = val
      return
    
    reply = self.ques_replace(attr, stat, parent)
    if reply == QMessageBox.StandardButton.No: 
      return
    self.admin[stat] = val

    ##print("admin:\n", stat, val)

    # --------------------------------------------------------------------- #
  def get_name(self):
    return self.admin['League Name']
  
  def get_all_players_num(self):
    ret = []
    if LinkedList.COUNT == 0:
      ###print('No teams in league')
      return ret
    else:
      traverser = self.head 
      while traverser != None:
        players = traverser.team.players
        for el in players:
          temp = (el.name, el.team, str(el.number))
          ret.append(temp)
          temp = None
        traverser = traverser.next
      return ret
  
  def get_all_players_avg(self):
    ret = []
    if LinkedList.COUNT == 0:
      ###print('No teams in league')
      return ret
    else:
      traverser = self.head 
      while traverser != None:
        players = traverser.team.players
        for el in players:
          temp = (el.name, el.team, el.AVG)
          ret.append(temp)
          temp = None
        traverser = traverser.next
      return ret
  
  def get_all_avg(self):
    ret = []
    if LinkedList.COUNT == 0:
      ###print("no team sin league")
      return ret 
    traverser = self.head 
    while traverser != None:
      name = traverser.team.name 
      roster = traverser.team.max_roster
      avg = self.format_decimal(float(traverser.team.get_bat_avg()))
      ret.append((name, roster, avg))
      traverser = traverser.next 
    return ret

  def get_all_wl(self):
    ret = []
    if LinkedList.COUNT == 0:
      ###print("no team sin league")
      return ret 
    traverser = self.head 
    while traverser != None:
      name = traverser.team.name 
      roster = traverser.team.max_roster
      avg = self.format_decimal(float(traverser.team.get_wl_avg()))
      ret.append((name, roster, avg))
      traverser = traverser.next 
    return ret
  
  def get_all_team_names(self):
    ret = []
    if LinkedList.COUNT == 0:
      ###print("no team sin league")
      return None
    traverser = self.head
    while traverser != None:
      name = traverser.team.name 
      ret.append(name)
      traverser = traverser.next 
    return ret
  
  def get_team_era(self):
    '''
    team = all players
    players = [a,b,c,d,e,f,g]
    a.positions = [a,b,c,d,pitcher,e,f,g]
    if 'pitcher' in a.positions:
      temp = a.era
      total += temp 
      temp = 0
    '''
    ret = []
    total = 0 
    if LinkedList.COUNT == 0:
      ###print('No teams in league')
      return self.format_decimal(ret)
    else:
      traverser = self.head 
      while traverser != None:
        players = traverser.team.players
        for el in players:
          pos = el.positions
          if 'pitcher' in pos:
            temp = float(el.era) 
            total += temp
            temp = 0
        ret.append((traverser.team.name, str(total)))
        total = 0
        traverser = traverser.next
      return ret
    
  def get_all_objs(self):
    ret = []
    if self.COUNT == 0:
      return ret
    traverser = self.head
    while traverser is not None:
      objTeam = traverser.team 
      ret.append(objTeam)
      traverser = traverser.next 
    return ret

class Node():
  def __init__(self, team, next=None):
    self.team = team
    self.next = next

class NodeStack():
  def __init__(self, obj, name, stat, prev, func, flag, player=None):
    self.obj = obj
    self.name = name 
    self.stat = stat 
    self.prev = prev 
    self.func = func
    self.flag = flag
    self.player = player
  
  def __iter__(self):
    yield self.obj
    yield self.name 
    yield self.stat 
    yield self.prev
    yield self.func
    yield self.flag
    yield self.player

class Team():
  def __init__(self, league, name, manager, message=None, max_roster=math.inf):
    self.name = name  
    self.league = league
    self.leagueID = self.league.leagueID
    self.teamID = self.get_hash()
    self.logo = None
    self.manager = manager
    self.players = []
    self.lineup = { # generate empty list/dict of length determined by max_roster roster value
      "1": None, 
      "2": None,
      "3": None, 
      "4": None, 
      "5": None, 
      "6": None, 
      "7": None, 
      "8": None, 
      "9": None
      } 
    self.positions = {
        'pitcher': None,
        'catcher': None,
        'first base': None,
        'second base': None,
        'third base': None,
        'shortstop': None,
        'left field': None,
        'center field': None,
        'right field': None
        }
    self.wins = 0 
    self.losses = 0
    self.games_played = 0
    self.wl_avg = 0
    self.bat_avg = 0
    self.team_era = 0
    self.max_roster = max_roster

    # message instance 
    self.message = message
  
  # ------------------------------------------------------------------------ #
  # utilities


  def __str__(self): 
    ret = ''
    ####print(self.players)
    ret += f'Team: {self.name}\nManager: {self.manager}\nRoster: {self.get_size()} / {self.max_roster}\nPlayers: {[x.name for x in self.players]}\nG: {self.games_played}\nWins: {self.wins}\nLosses: {self.losses}\nW-L: {self.wl_avg}\nAVG: {self.bat_avg}\nTeam Era: {self.team_era}'
    return ret
  
  def get_hash(self):
    def indx(a, b):
        index = a.index(b)
        if index == 0:
            return 2 
        return index
    ord_lst = [sum(ord(x)*indx(self.name, x) for x in self.name)]
    return ord_lst.pop()

  
  def less_zero(self, stat, val):       return stat + val < 0
  
  def ques_replace(self, attr, stat, parent):
    existing_val = getattr(self, attr)[stat]
    if existing_val:
      reply = QMessageBox.question(parent, "Input Error", f"Would you like to replace {existing_val} at {stat}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
      return reply 
    return None
  
  def format_decimal(self, num):        return "{:.3f}".format(num)

  def populate_lineup(self):
    for indx in range(10, self.max_roster+1): 
      self.lineup[str(indx)] = None
  
  def _get_attrs(self):
      directory = dir(self)
      ret = []
      for el in directory:
        temp = getattr(self, el)
        if isinstance(temp, (int)):
            ####print(temp, el)
            ret.append((el, temp))
      return ret
  
  def format_attrs_players(self):
    ret = []
    for el in self.players:
      directory = dir(el)
      temp = getattr()
        
  
  def check_graph_min(self):
    if self.games_played == 0:
      return None
  
  def set_min(self):
    self.games_played = 10 
    self.wins = 7 
    self.losses = 3
  
  def graph_view_format_team(self):
        sample_team = None
        '''data_test_player = [
          {
            'Stat': 'On Base',
            'Amount': [{"Hit": 177}, {"BB": 111},{"HBP": 6}, {"Error": 3}],
          },
          {
            'Stat': 'Outs',
            'Amount': [{"SO": 175}, {"Sac Fly": 5}, {"GIDP": 14}],
          }
        ]'''
        check = self.check_graph_min()
        if not check:
           sample_team = Team('Sample Team', "Sample Manager", self.message, 10)
           sample_team.set_min()
        ret = [
            {
            'Stat_1': None, 
            'Amount_1': [] 
            },
            {
            'Stat_2': None, 
            'Amount_2': [] 
            }
        ]
        # refactor to match individual pplayer stats
        team = ['games_played', 'wins', 'losses']
        individual = ['BABIP', 'SLG', 'AVG', 'ISO', 'ERA', 'WHIP', 'k_9', 'bb_9']
        attrs = self._get_attrs()
        if sample_team:
           attrs = sample_team._get_attrs()
        ###print(attrs)
        for el in attrs:
            ###print(el)
            stat = el[0]
            val = el[1]
            ###print(stat, val)
            stat_1 = ret[0]['Stat_1']
            stat_2 = ret[1]['Stat_2']
            if stat in team:
                ###print(stat)
                if not stat_1:
                    ret[0]['Stat_1'] = 'Team' 
                    temp = {stat:val}
                    amt_lst_1 = ret[0]['Amount_1']
                    amt_lst_1.append(temp) 
                else:
                    temp = {stat:val}
                    amt_lst_1 = ret[0]['Amount_1']
                    amt_lst_1.append(temp) 
            elif stat in individual:
                ###print(stat)
                if not stat_2:
                    ret[1]['Stat_2'] = 'Individual'
                    temp = {stat:val}
                    amt_lst_1 = ret[1]['Amount_2']
                    amt_lst_1.append(temp) 
                else:
                    temp = {stat:val}
                    ###print(temp)
                    amt_lst_2 = ret[1]['Amount_2']
                    amt_lst_2.append(temp)
        return ret
  
  # string
  def return_dict(self, dict):
        ret = "" 
        ####print('return dict:', dict)
        for el in dict:
            ###print('return dict:', el)
            ret += f"{el}:{dict[el]}\n"
        return ret
          
  # team lineup 
  # list of tuples
  def format_dict(self, dict):
        ret = []
        ret_dict = self.return_dict(dict).split("\n")
        ####print(ret_dict)
        for el in ret_dict:
            # not necessary
            indx = el.find(":")
            el = el.replace(":", " ")
            val = el[:indx].strip()
            name = el[indx::].strip()
            ret.append((val, name))
            #temp = None
        ret.pop()
        return ret
        
  # team stats 
  # list of all stats as tuples (exclude lineup) 
  def all_stats(self):
        ret_raw = self.__str__().split("\n")
        temp = None
        ret = []
        for el in ret_raw:
            temp = el.split(": ")
            stat = temp[0]
            val = temp[1]
            ret.append((stat,val))
            temp = None
        return ret

  # team stats 
  # list of all team stats plus lineup as tuples
  def return_stats(self):
        ret = []
        all = self.all_stats()
        lineup = self.format_dict(self.lineup)
        positions = self.format_dict(self.positions)
        ####print('formatted positions:', positions)
        ####print('formatted linuep:', lineup)
        ret += all
        ret.append(('Lineup', '----- -----'))
        ret += lineup
        ret.append(('Positions', '----- -----'))
        ret += positions
        ret.pop()
        ####print('return stats:', ret)
        return ret
  
  # ------------------------------------------------------------------------ #
  # getters 

  def get_max_roster(self):                    return self.max_roster

  def get_size(self):                   return len(self.players)

  def get_lineup(self):
    ret = ''
    for el in self.lineup:
      ret += f'{el}: {self.lineup[el]}\n' 
    return ret

  def get_positions(self):
    ret = ''
    for el in self.positions:
      ret += f'{el}: {self.positions[el]}\n'
    return ret 
  
  def get_games_played(self):           return self.games_played 
  
  def get_wins(self):                   return self.wins
  
  def get_losses(self):                 return self.losses
  
  def get_wl_avg(self):                 return self.wl_avg
  
  def get_bat_avg(self):                return self.bat_avg

  def get_player(self, target):
    for el in self.players:
      if el.name == target:
        ####print(el)
        return el
    ####print('Player not found')
    return

  def get_manager(self):                return self.manager 

  def get_team_era(self):
    return self.team_era 
  
  def get_team_hits(self):
    if len(self.players) == 0:
      return 0 
    total = 0 
    for player in self.players:
      total += player.hit 
    return total
  
  def get_team_so(self):
    if len(self.players) == 0:
      return 0 
    total = 0 
    for player in self.players:
      total += player.so 
    return total
  
  def get_team_runs(self):
    if len(self.players) == 0:
      return 0 
    total = 0 
    for player in self.players:
      total += player.runs 
    return total
  
  def get_team_era(self):
    if len(self.players) == 0:
      return 0 
    total = 0 
    for player in self.players:
      pos = player.positions
      if "pitcher" in pos:
        era_float = float(player.era)
        total += era_float
    return total
  
  def get_team_k(self):
    if len(self.players) == 0:
      return 0 
    total = 0 
    for player in self.players:
      pos = player.positions
      if "pitcher" in pos:
        total += player.p_so
    return total

     
     

  # -------------------------------------------------------------------------------------- # 
  # setters

  def set_max_roster(self, val):        
    if self.max_roster + val < len(self.players):
      new_total = self.max_roster + val
      self.message.show_message(f"Roster max_roster {new_total} cannot be less than current roster {self.max_roster}.")
      #QMessageBox.warning(self, "Input Error", f"Roster max_roster {new_total} cannot be less than current roster {self.max_roster}.")  
      return     
    self.max_roster = val
  
  # not in use
  def not_set_lineup(self, order, name):
    if order > self.get_size():
      ###print(f'No position {order} in batting order. Try number less than {self.get_size() + 1}\n')
      return
    if order in self.lineup:
      flag_action = input(f'Would you like to replace {self.lineup[order]} at spot {order}? y/n ').lower() == 'y'
      if not flag_action:
        return 
      self.lineup[order] = name 
    else:
      self.lineup[order] = name
     
  def set_pos(self, attr, stat, player, parent):
    reply = self.ques_replace(attr, stat, parent)
    if reply == QMessageBox.StandardButton.No: 
      return
    self.positions[stat] = player
    ###print("positions:\n", self.get_positions())
  
  def set_wl_avg(self):                 self.wl_avg = self.calc_wl_avg()

  def set_bat_avg(self):                self.bat_avg = self.calc_bat_avg()

  def set_manager(self, val):           self.manager = val
  
  def set_lineup(self, attr, stat, player, parent):      
    reply = self.ques_replace(attr, stat, parent)
    if reply == QMessageBox.StandardButton.No: 
      return
    self.lineup[stat] = player
    ###print("positions:\n", self.get_positions())
  
  def set_games_played(self, val, parent):
    if self.less_zero(self.games_played, val):
      return
    if isinstance(val, int):
      self.games_played += val 
      return
    #QMessageBox.warning(parent, "Input Error", "Enter a value greater than zero.")
    self.message.show_message("Enter a value greater than zero.")
  
  def set_wins(self, val, parent):
    if self.less_zero(self.wins, val):
      return
    if self.games_played > 0: 
      if (self.wins + val + self.losses) <= self.games_played:
        self.wins += val 
        return 
    #QMessageBox.warning(parent, "Input Error", f"Wins-Losses cannot exceed games played\n\n          W:{self.wins} L:{self.losses} G:{self.games_played}.")
    self.message.show_message(f"Wins-Losses cannot exceed games played\n\n          W:{self.wins} L:{self.losses} G:{self.games_played}.")
  
  def set_losses(self, val, parent):
    if self.less_zero(self.losses, val):
      return
    if self.games_played > 0:
      if (self.losses + val) + self.wins <= self.games_played:
        self.losses += val
        return 
    #QMessageBox.warning(parent, "Input Error", f"Wins-Losses cannot exceed games played\n\n          W:{self.wins} L:{self.losses} G:{self.games_played}.")
    self.message.show_message(f"Wins-Losses cannot exceed games played\n\n          W:{self.wins} L:{self.losses} G:{self.games_played}.")
  
  def set_team_era(self):
    self.team_era = self.calc_team_era()

# -------------------------------------------------------------------------- # 
# calculators 

  def calc_wl_avg(self):
    ret = 0
    if self.games_played > 0 and self.wins > 0:
      ret = self.wins / self.games_played
    return self.format_decimal(ret) 
  
  def calc_bat_avg(self):
    num = len(self.players)
    ret = 0
    if num > 0:
      total = 0
      for player in self.players:
        total += float(player.AVG)
      ret = total / num 
    return self.format_decimal(ret)
  
  def calc_team_era(self):
    ret = 0
    count = 0
    for player in self.players:
      if "pitcher" in player.positions:
        count += 1
        ret += float(player.get_era()) 
    return self.format_decimal(ret)

# -------------------------------------------------------------------------- # 
# modify team

  def add_player(self, new_player):
    if len(self.players) < self.max_roster:
      self.players.append(new_player)
    else:
      ###print('Roster is full')
      return

  def remove_player(self, player):
    indx = None
    for i in range(len(self.players)):
      if self.players[i].name == player:
        ####print(self.players)
        ####print('index', i)
        ####print('player found\n', self.players[i])
        ####print('player found\n', self.players[i].name)
        indx = i
    self.players.pop(indx)
    return self.players

class Player():
  def __init__(self, name, number, team, league, positions=[], message=None, parent=None):
    self.name = name 
    self.playerID = self.get_hash()
    self.team = team.name
    self.teamID = team.teamID
    self.leagueID = league.leagueID
    self.number = number 
    self.positions = positions
    self.pa = 0
    self.at_bat = 0 
    self.fielder_choice = 0
    self.hit = 0 
    self.bb = 0
    self.hbp = 0
    self.so = 0
    self.hr = 0
    self.rbi = 0
    self.runs = 0
    self.singles = 0
    self.doubles = 0
    self.triples = 0
    self.sac_fly = 0
    self.OBP = 0
    self.BABIP = 0
    self.SLG = 0
    self.AVG = 0
    self.ISO = 0
    self.image = None

    #message box
    self.message = message
    self.parent = parent
    ###print('player initialized - msg inst', self.message)


  def __str__(self):
    ret = f'Name: {self.name}\nNumber: {self.number}\nPrimary Position: {self.positions[0]}\n  Secondary Positions: {self.positions[1:]}\n'
    ret += f'PA: {self.pa}\nAt Bats: {self.at_bat}\nHits: {self.hit}\nWalks: {self.bb}\nHBP: {self.hbp}\nSO: {self.so}\nHR: {self.hr}\n'
    ret += f'Runs: {self.runs}\nRBI: {self.rbi}\nOBP: {self.OBP}\nBABIP: {self.BABIP}\nSLG: {self.SLG}\nAVG: {self.AVG}\nISO: {self.ISO}' 
    return ret
  
  def get_hash(self):
    def indx(a, b):
        index = a.index(b)
        if index == 0:
            return 2 
        return index
    ord_lst = [sum(ord(x)*indx(self.name, x) for x in self.name)]
    return ord_lst.pop()
  
  def check_graph_min(self):
    stats = ['hit', 'bb', 'so'] 
    for stat in stats:
      val = getattr(self, stat)
      if val == 0:
        ##print('Sample chart, must update at bats, hits, walks, SOs !')
        return False 
    return True
  
  def set_min(self):
      #self.message.show_message('Sample chart. Player has no updated stats!')
      self.at_bat = 50 
      self.pa = 60
      self.bb = 10 
      self.hit = 20
      self.sac_fly = 10
      self.so = 20 
      self.hr = 3  
      self.singles = 10 
      self.doubles = 5 
      self.triples = 2

  def graph_view_format_player(self):
        sample_player = None
        flag = True
        '''data_test_player = [
          {
            'Stat': 'On Base',
            'Amount': [{"Hit": 177}, {"BB": 111},{"HBP": 6}, {"Error": 3}],
          },
          {
            'Stat': 'Outs',
            'Amount': [{"SO": 175}, {"Sac Fly": 5}, {"GIDP": 14}],
          }
        ]'''
        check = self.check_graph_min()
        if check == False:
           sample_player = Player('Sample Player', 1, 'Sample Team', self.message, ['sample positions'])
           sample_player.set_min()
           flag = False
        ret = [
            {
            'Stat_1': None, 
            'Amount_1': [] 
            },
            {
            'Stat_2': None, 
            'Amount_2': [] 
            }
        ]
        on_base = ['bb', 'doubles', 'hit', 'hr', 'singles', 'triples']
        outs = ['so', 'sac_fly']
        attrs = self._get_attrs()
        if sample_player:
          attrs = sample_player._get_attrs()
        ###print(attrs)
        for el in attrs:
            ###print(el)
            stat = el[0]
            val = el[1]
            ###print(stat, val)
            stat_1 = ret[0]['Stat_1']
            stat_2 = ret[1]['Stat_2']
            if stat in on_base:
                ###print(stat)
                if not stat_1:
                    ret[0]['Stat_1'] = 'On Base' 
                    temp = {stat:val}
                    amt_lst_1 = ret[0]['Amount_1']
                    amt_lst_1.append(temp) 
                else:
                    temp = {stat:val}
                    amt_lst_1 = ret[0]['Amount_1']
                    amt_lst_1.append(temp) 
            elif stat in outs:
                ###print(stat)
                if not stat_2:
                    ret[1]['Stat_2'] = 'Outs'
                    temp = {stat:val}
                    amt_lst_1 = ret[1]['Amount_2']
                    amt_lst_1.append(temp) 
                else:
                    temp = {stat:val}
                    ###print(temp)
                    amt_lst_2 = ret[1]['Amount_2']
                    amt_lst_2.append(temp)
        return (ret, flag)

  def format_player(self, raw_lst):
    team = raw_lst[0]
    name = raw_lst[1]
    number = raw_lst[2]
    #avg = self.AVG
    positions = raw_lst[3:]
    ####print(raw_lst)
    ####print('team', team)
    ####print('name', name)
    ####print('number', number)
    new_player = Player(name, number, team, positions)
    return new_player

    # utilities 

  def format_decimal(self, num):        return "{:.3f}".format(num)
  
  def less_zero(self, stat, val):       return stat + val < 0

  def limit_at_bat(self, stat, val):    return (stat + val) > self.at_bat

  def _add_stat(self, attr, val, minimum=0, maximum=None, max_label=None):
      """Safely add val to stat, validate boundaries."""
      current = getattr(self, attr)
      new_total = current + val

      if new_total < minimum:
          self._warn(f"{attr.upper()} cannot be negative.")
          return

      if maximum is not None and new_total > maximum:
          label = max_label or maximum
          self._warn(f"{attr.upper()} cannot exceed {label}.")
          return

      setattr(self, attr, new_total)
  
  def _warn(self, message):
      #QMessageBox.warning(self.parent, "Stat Input Error", message)
      ##print('warn error msg inst', self.message)
      self.message.show_message(message)
      
  def _get_attrs(self):
      directory = dir(self)
      ret = []
      for el in directory:
        temp = getattr(self, el)
        if isinstance(temp, (int)):
            ####print(temp, el)
            ret.append((el, temp))
      return ret
  
  def _get_max(self, stat):
      check_hits = ['hr', 'runs', 'singles', 'doubles', 'triples']
      check_bats = ['hit', 'bb', 'so', 'sac_fly']
      total = 0 
      if stat in check_hits:
          for el in check_hits:
              curr = getattr(self, el)
              total += curr 
      elif stat in check_bats:
          for el in check_bats:
            curr = getattr(self, el)
            total += curr 
      return total
  
  def _validate_update(self, stat, update, val):
    curr_stat = getattr(self, stat)
    total = self._get_max(update)
    new_total = total + val
    curr_update = getattr(self, update)
    new_val = curr_update + val
    if new_total > curr_stat:
        ####print('invalid stat update')
        self._warn(f"{update.capitalize()} update total cannot exceed {stat.capitalize()} {curr_stat}.")
    else:
        ###print('valid stat update')
        ##print('curr val:', stat, curr_stat)
        ##print('curr total:', total)
        ##print('new total:', new_total)
        setattr(self, update, new_val)
    
    # ------------------------------------------------------------------------ #
    # getters 

  def get_at_bat(self):                 return self.at_bat 
  
  def get_BABIP(self):                  return self.BABIP
  
  def get_SLG(self):                    return self.SLG
  
  def get_AVG(self):                    return self.AVG

  def get_ISO(self):                    return self.ISO 

  def get_OBP(self):                    return self.OBP

    # ------------------------------------------------------------------------ #
    # setters 
  def set_pa(self, val):
    #self.pa += val
    self.pa += val

  def set_at_bat(self, val):
    self.at_bat += val
    #self._validate_update('pa', 'at_bat', val)
    #self._add_stat('at_bat', val)
    '''if self.at_bat + val < 0:
      self.at_bat = 0
    else:
      ###print('type val - at bat', type(val))
      self.at_bat += val'''
        
  def set_hit(self, val):
    self.hit += val 
    self.set_at_bat(val)
    self.set_pa(val)
    #self._validate_update('at_bat', 'hit', val)

    #self._add_stat('hit', val, maximum=self.at_bat)

    '''if self.at_bat == 0:
      self.hit = 0
    elif self.hit > self.at_bat:
      ###print('excess hits')
    else:
      self.hit += val
      ###print('hits proper limit')'''
  
  def set_bb(self, val):
    self.bb += val 
    self.set_pa(val)
    #self._validate_update('pa', 'bb', val)
    #self._add_stat('bb', val, maximum=self.at_bat)
    '''if self.less_zero(self.bb, val):
      self.bb = 0
    else:
      self.bb += val
    '''
  def set_hbp(self, val):
    self.hbp += val
    self.set_pa(val)
    #self._validate_update('pa', 'hbp', val)
  
  def set_so(self, val):
    self.so += val 
    self.set_pa(val)
    #self._validate_update('at_bat', 'so', val)
  
  def set_hr(self, val):
    self._validate_update('hit', 'hr', val)
    #self._add_stat('hr', val, maximum=self.at_bat)
    '''if self.less_zero(self.hr, val):
      self.hr = 0
    else:
      self.hr += val'''

  def set_rbi(self, val):
    #self._validate_update('at_bat', 'hit', val)
    #self._add_stat('rbi', val, maximum=self.at_bat)
    if self.less_zero(self.rbi, val):
      self.rbi = 0
    elif self.at_bat > 0:
       self.rbi += val
    '''if self.less_zero(self.rbi, val):
      self.rbi = 0
    else:
      self.rbi += val'''
  
  def set_runs(self, val):
    #self._validate_update('hit', 'runs', val)
    #self._add_stat('runs', val)
    if self.less_zero(self.runs, val):
      self.runs = 0
    elif self.at_bat > 0:
       self.runs += val

  def set_sac_fly(self, val):
    self.sac_fly += val 
    self.set_pa(val)
    #self._validate_update('pa', 'sac_fly', val)
    #self._add_stat('sac_fly', val, maximum=self.at_bat)
    '''if self.less_zero(self.sac_fly, val):
      self.sac_fly = 0
    else:
      self.sac_fly += val'''
  
  def set_fielder_choice(self, val):
    self.fielder_choice += val 
    self.set_pa(val)

  def set_singles(self, val):
    self._validate_update('hit', 'singles', val)
    #self._add_stat('singles', val, maximum=self.hit)
    '''if self.less_zero(self.singles, val):
      self.singles = 0
    else:
      self.singles += val
    '''
  def set_doubles(self, val):
    self._validate_update('hit', 'doubles', val)
    #self._add_stat('doubles', val, maximum=self.hit)
    '''if self.less_zero(self.doubles, val):
      self.doubles = 0
    else:
      self.doubles += val '''
  
  def set_triples(self, val):
    self._validate_update('hit', 'triples', val)
    #self._add_stat('triples', val, maximum=self.hit)
    '''if self.less_zero(self.triples, val):
      self.triples = 0
    else:
      self.triples += val'''
  
  def set_AVG(self):              self.AVG = self.calc_AVG()
  
  def set_BABIP(self):            self.BABIP = self.calc_BABIP()

  def set_SLG(self):              self.SLG = self.calc_SLG()
  
  def set_ISO(self):              self.ISO = self.calc_ISO()

  def set_OBP(self):              self.OBP = self.calc_OBP()

    # ---------------------------------------------------------------------------------- #
    # calc functions
  
  def calc_OBP(self): 
    # (Hits + Walks + Hit By Pitch) / (At Bats + Walks + Hit By Pitch + Sacrifice Flies)
    ret = 0
    if self.pa == 0 or self.at_bat == 0:
      return self.format_decimal(ret)
    elif (self.at_bat + self.bb + self.hbp + self.sac_fly) == 0:
      return self.format_decimal(ret)
    ret = (self.hit + self.bb + self.hbp) / (self.at_bat + self.bb + self.hbp + self.sac_fly)
    return self.format_decimal(ret)
  
  def calc_BABIP(self):
    #(H - HR)/(AB - K - HR + SF)
    ret = 0
    if self.at_bat - self.so - self.hr + self.sac_fly <= 0:
      return self.format_decimal(ret)
    ret = (self.hit - self.hr)/(self.at_bat - self.so - self.hr + self.sac_fly)
    return self.format_decimal(ret)
    
  def calc_SLG(self):
    #(1B + 2Bx2 + 3Bx3 + HRx4)/AB
    ret = 0
    if self.at_bat == 0:
      return self.format_decimal(ret)
    ret = ( self.singles + (2 * self.doubles) + (3 * self.triples) + (4 * self.hr) ) / self.at_bat 
    return self.format_decimal(ret)
  
  def calc_AVG(self):
    ret = 0
    if self.hit == 0 or self.at_bat == 0:
      return self.format_decimal(ret)
    ret = self.hit / self.at_bat 
    return self.format_decimal(ret)
      
  def calc_ISO(self):
    #(1x2B + 2x3B + 3xHR) / At-bats OR Slugging percentage - Batting average
    ret = 0
    #print('slg:', self.SLG)
    #print('avg:', self.AVG)
    if self.at_bat == 0:
      return self.format_decimal(ret)
    if float(self.SLG) - float(self.AVG) > 0:
      ret = ( (1 * self.doubles) + (2 * self.triples) + (3 * self.hr ) ) / float(self.SLG) - float(self.AVG)
    return self.format_decimal(ret)

class Pitcher(Player):
  def __init__(self, name, number, team, league,  positions=[], message=None, parent=None):
    super().__init__(name, number, team, league, positions=[], message=None, parent=None)
    # self, name, number, team, league, message, positions=[], parent=None
  
    # player pitcher gen attr
    self.name = name 
    self.number = number 
    self.team = team.name 
    self.teamID = team.teamID 
    self.leagueID = league.leagueID
    self.playerID = self.get_hash()
    self.positions = positions
    self.image = None
    self.message = message
    self.parent = parent

    # pitching attr
    self.wins = 0 
    self.losses = 0 
    self.era = 0 
    self.games_played = 0 

    # to incorporate ...
    self.games_started = 0 
    self.games_completed = 0 
    self.shutouts = 0 
    self.saves = 0 
    self.save_ops = 0
    self.ip = 0 
    self.p_at_bats = 0
    self.p_hits = 0 
    self.p_runs = 0
    self.er = 0 
    self.p_hr = 0 
    self.p_hb = 0 
    self.p_bb = 0 
    self.p_so = 0 
    self.WHIP = 0 
    self.p_avg = 0 
    self.k_9 = 0 
    self.bb_9 = 0 
  
  def __str__(self):
    ret = f'Name: {self.name}\nNumber: {self.number}\nPrimary Position: {self.positions[0]}\nSecondary Positions: {self.positions[1:]}\n'
    ret += f'Offense: ----- -----\n Plate Appearance: {self.pa}\nAt Bats: {self.at_bat}\n Hits: {self.hit}\n Walks: {self.bb}\n SO: {self.so}\n HR: {self.hr}\n'
    ret += f' Runs: {self.runs}\n RBI: {self.rbi}\n OBP: {self.OBP}\nBABIP: {self.BABIP}\n SLG: {self.SLG}\n AVG: {self.AVG}\n ISO: {self.ISO}\n' 
    ret += f'Pitching: ----- -----\n Wins: {self.wins}\n Losses: {self.losses}\n G: {self.games_played}\n ERA: {self.era}\n'
    ret += f' IP: {self.ip}\n At Bats: {self.p_at_bats}\n SO: {self.p_so}\n BB: {self.p_bb}\n AVG: {self.p_avg}\n WHIP: {self.WHIP}\n K9: {self.k_9}\n BB9: {self.bb_9}'
    return ret

  # -------- Validation Utilities --------

  def _show_error(self, message):
      #QMessageBox.warning(self.parent, "Input Error", message)
      ##print('show error - msg inst', self.message)
      self.message.show_message(message)

  '''
  def _validate_game_total(self, new_wins=0, new_losses=0):
      if self.games_played == 0:
          self._show_error("No games played yet.")
          return False
      if self.wins + self.losses + new_wins + new_losses > self.games_played:
          self._show_error("Total wins and losses cannot exceed games played.")
          return False
      return True

  def _validate_game_component(self, added, stat_name):
      if getattr(self, stat_name) + added > self.games_played:
          self._show_error(f"{stat_name.replace('_', ' ').capitalize()} cannot exceed games played.")
          return False
      return True
  '''
  
  def _validate_not_exceed(self, val, stat_name, limit):
    if getattr(self, stat_name) + val > limit:
        self._show_error(f"{stat_name.replace('_', ' ').capitalize()} cannot exceed {limit}.")
        return False
    return True

  def _validate_combined_limit(self, val, stat_names, limit, combined_label="Combined stats"):
    current_total = sum(getattr(self, stat) for stat in stat_names)
    if current_total + val > limit:
        self._show_error(f"{combined_label} cannot exceed {limit}.")
        return False
    return True
  
  def _update_stat(self, val, attr_name, custom_validator=None):
    if self.less_zero(getattr(self, attr_name), val):
        self._show_error(f"{attr_name.replace('_', ' ').capitalize()} cannot go below zero.")
        return

    if custom_validator and not custom_validator(val):
        return

    setattr(self, attr_name, getattr(self, attr_name) + val)

  # -------- Game Logic --------

  '''def set_games_played(self, val):
      if self.less_zero(self.games_played, val):  
          return     
      self.games_played += val

  def set_wins(self, val):
      if self.less_zero(self.wins, val):  
          return 
      if self._validate_game_total(new_wins=val):
          self.wins += val

  def set_losses(self, val):
      if self.less_zero(self.losses, val):  
          return 
      if self._validate_game_total(new_losses=val):
          self.losses += val

  def set_games_started(self, val):
      if self.less_zero(self.games_started, val):  
          return 
      if self._validate_game_component(val, "games_started"):
          self.games_started += val

  def set_games_completed(self, val):
      if self.less_zero(self.games_completed, val):  
          return 
      if self._validate_game_component(val, "games_completed"):
          self.games_completed += val

  def set_shutouts(self, val):       self.shutouts += val
  def set_saves(self, val):          self.saves += val
  def set_save_ops(self, val):       self.save_ops += val
  def set_er(self, val):             self.er += val
  def set_ip(self, val):             self.ip += val
  def set_p_hits(self, val):         self.p_hits += val
  def set_p_bb(self, val):           self.p_bb += val
  def set_p_so(self, val):           self.p_so += val
  def set_p_at_bats(self, val):      self.p_at_bats += val
  def set_p_runs(self, val):         self.p_runs += val
  def set_p_hr(self, val):           self.p_hr += val
  def set_p_hb(self, val):           self.p_hb += val'''

  def set_wins(self, val):
      if self.games_played > 0 and (self.wins + self.losses) == self.games_played:
          #QMessageBox.warning(self.parent, "Input Error", "Update games played before wins and losses.")
          self.message.show_message("Update games played before wins and losses.")
          return 
      if (self.wins + val + self.losses) > self.games_played:
          #QMessageBox.warning(self.parent, "Input Error", "Wins - Losses do not match total games played.")
          self.message.show_message("Wins - Losses do not match total games played.")
          return 
      self.wins += val

  def set_losses(self, val):
      if self.games_played > 0 and (self.wins + self.losses) == self.games_played:
          #QMessageBox.warning(self.parent, "Input Error", "Update games played before wins and losses.")
          self.message.show_message("Update games played before wins and losses.")
          return
      if (self.wins + val + self.losses) > self.games_played:
          #QMessageBox.warning(self.parent, "Input Error", "Wins - Losses do not match total games played.")
          self.message.show_message("Wins - Losses do not match total games played.")
          return 
      self.losses += val

  def set_er(self, val):
      self._update_stat(val, 'er', lambda v: self._validate_not_exceed(v, 'er', self.p_at_bats))

  def set_ip(self, val):
      self._update_stat(val, 'ip', lambda v: self._validate_not_exceed(v, 'ip', 9 * self.games_played))

  def set_saves(self, val):
      self._update_stat(val, 'saves', lambda v: self._validate_not_exceed(v, 'saves', self.games_played))

  def set_save_ops(self, val):
      self._update_stat(val, 'save_ops', lambda v: self._validate_not_exceed(v, 'save_ops', self.games_played))
  
  def set_shutouts(self, val):
      self._update_stat(val, 'shutouts', lambda v: self._validate_not_exceed(v, 'shutouts', self.games_completed))
  
  def set_p_at_bats(self, val):
      if self.less_zero(self.p_at_bats, val):
         return 
      self.p_at_bats += val

  def set_p_runs(self, val):
      self._update_stat(val, 'p_runs', lambda v: self._validate_not_exceed(v, 'p_runs', self.p_at_bats))

  def set_p_hr(self, val):
      self._update_stat(val, 'p_hr', lambda v: self._validate_combined_limit(v, ['p_hits', 'p_bb', 'p_so', 'p_hr', 'p_hb'], self.p_at_bats))

  def set_p_bb(self, val):
      self._update_stat(val, 'p_bb', lambda v: self._validate_combined_limit(v, ['p_hits', 'p_bb', 'p_so', 'p_hr', 'p_hb'], self.p_at_bats))

  def set_p_hits(self, val):
      self._update_stat(val, 'p_hits', lambda v: self._validate_combined_limit(v, ['p_hits', 'p_bb', 'p_so', 'p_hr', 'p_hb'], self.p_at_bats))

  def set_p_so(self, val):
      self._update_stat(val, 'p_so', lambda v: self._validate_combined_limit(v, ['p_hits', 'p_bb', 'p_so', 'p_hr', 'p_hb'], self.p_at_bats))

  def set_p_hb(self, val):
      self._update_stat(val, 'p_hb', lambda v: self._validate_combined_limit(v, ['p_hits', 'p_bb', 'p_so', 'p_hr', 'p_hb'], self.p_at_bats))
  
  def set_games_played(self, val):
      if self.less_zero(self.games_played, val):
         return 
      self.games_played += val

  def set_games_started(self, val):
      self._update_stat(val, 'games_started', lambda v: self._validate_not_exceed(v, 'games_started', self.games_played))

  def set_games_completed(self, val):
    self._update_stat(val, 'games_completed', lambda v: self._validate_not_exceed(v, 'games_completed', self.games_played))  

  def set_p_avg(self):               self.p_avg = self.calc_p_avg()
  def set_k_9(self):                 self.k_9 = self.calc_k_9()
  def set_bb_9(self):                self.bb_9 = self.calc_bb_9()
  def set_WHIP(self):                self.WHIP = self.calc_WHIP()
  def set_era(self):                 self.era = self.calc_era()

  # -------- Calculations --------

  def calc_era(self):
      return self.format_decimal((self.er / self.ip) * 9) if self.ip else 0.000

  def calc_WHIP(self):
      return self.format_decimal((self.p_bb + self.p_hits) / self.ip) if self.ip else 0.000

  def calc_p_avg(self):
      return self.format_decimal(self.p_hits / self.p_at_bats) if self.p_at_bats else 0.000

  def calc_k_9(self):
      return self.format_decimal((self.p_so / self.ip) * 9) if self.ip else 0.000

  def calc_bb_9(self):
      return self.format_decimal((self.bb / self.ip) * 9) if self.ip else 0.000

  # -------- Getters --------

  def get_wins(self):         return self.wins
  def get_losses(self):       return self.losses
  def get_games_played(self): return self.games_played
  def get_era(self):          return self.era
  def get_p_at_bats(self):    return self.p_at_bats


                    # -------------------------------------------------------------------------------------------------- #

class Save():
  def __init__(self, db, league):
    self.db = db
    self.openDB = self.open_db()
    self.con = self.get_con()
    self.cur = self.get_cur()
    self.league = league

  def open_db(self):
    # Connect and insert
    con = sqlite3.connect(self.db, timeout=60)
    cur = con.cursor()
    return (con, cur)
  
  def get_con(self):
    try: 
      if self.db:
        con = sqlite3.connect(self.db) 
        return con

    except:
      #print("Error connecting to db!")
      return None 
  
  def get_cur(self):
    try: 
      if self.con:
        cur = self.con.cursor()
        return cur 
    except:
      #print('Error getting cursor!')
      return None
    
  def table_exists(self, con, cur, table_name):
    #con, cur = self.open_db()
    cur.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name=?;
    """, (table_name,))

    return cur.fetchone() is not None

  def field_exists(self, table, field):
    con, cur = self.open_db()
    cur.execute(f"PRAGMA table_info({table});")
    columns = [row[1] for row in cur.fetchall()]  # row[1] is the column name
    return field in columns 
  
  def scan_ret(self, lst, target):
    for i in range(len(lst)):
      temp = lst[i][0]
      ##print(temp[0] == target)
      if target == temp:
        return True
    return False

  def init_new_db(self):
    # Enable foreign key constraints
    con, cur = self.open_db()
    cur.execute("PRAGMA foreign_keys = ON")
    
    con.commit()
    con.close()
    
    self.init_league()
    self.init_team()
    self.init_player()
    self.init_pitcher()

  def init_league(self):
      con, cur = self.open_db()
      '''if self.table_exists('league'):
        ##print('league(s) exist(s)!')

        res = cur.execute(f"SELECT leagueID FROM league")
        ret = res.fetchall()

        # check for league name duplicate 
        if ret:
          if self.scan_ret(ret, self.league.leagueID):
            #print('league id already exists!')
            return'''
      
      # Create league table
      cur.execute(f"""
          CREATE TABLE IF NOT EXISTS league (
              leagueID INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL,
              commissioner TEXT,
              treasurer TEXT,
              communications TEXT,
              historian TEXT,
              recruitment TEXT,
              start TEXT,
              stop TEXT
          )
      """)

     
      
      # set up league cols and fields
      cur.execute("""
      INSERT INTO league (
          leagueID, name, commissioner, treasurer,
          communications, historian, recruitment,
          start, stop
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
      """, (
          self.league.leagueID,
          self.league.name,
          self.league.admin['Commissioner'],
          self.league.admin['Historian'],
          self.league.admin['Recruitment'],
          self.league.admin['Communications'],
          self.league.admin['Historian'],
          self.league.admin['Season Start'],
          self.league.admin['Season End']
      ))

      cur.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_league_unique
        ON league(leagueID);
    """)


      # commit created tables and close
      con.commit()
      con.close()
    # call init league
    
  def init_team(self):
      con, cur = self.open_db()

      # Create team table
      cur.execute("""
        CREATE TABLE IF NOT EXISTS team (
            teamID INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            leagueID INTEGER NOT NULL,
            league TEXT,
            logo TEXT,
            manager TEXT,
            players TEXT,         -- JSON stringified list
            lineup TEXT,          -- JSON stringified dict
            positions TEXT,       -- JSON stringified dict
            wins INTEGER DEFAULT 0,
            losses INTEGER DEFAULT 0,
            games_played INTEGER DEFAULT 0,
            wl_avg REAL DEFAULT 0.0,
            bat_avg REAL DEFAULT 0.0,
            team_era REAL DEFAULT 0.0,
            max_roster INTEGER,
            FOREIGN KEY (leagueID) REFERENCES league(leagueID)
        )
      """) 

      cur.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_team_unique
        ON team(teamID);
      """)

      con.commit()
      con.close()
    # call init team
    
  def init_player(self):
      con, cur = self.open_db()
      
      # Create player table
      cur.execute("""
          CREATE TABLE IF NOT EXISTS player (
              playerID INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL,
              leagueID INTEGER NOT NULL,
              teamID INTEGER NOT NULL,
              number INTEGER,
              team TEXT,
              positions TEXT,       -- JSON stringified list
              pa INTEGER DEFAULT 0,
              at_bat INTEGER DEFAULT 0,
              fielder_choice INTEGER DEFAULT 0,
              hit INTEGER DEFAULT 0,
              bb INTEGER DEFAULT 0,
              hbp INTEGER DEFAULT 0,
              so INTEGER DEFAULT 0,
              hr INTEGER DEFAULT 0,
              rbi INTEGER DEFAULT 0,
              runs INTEGER DEFAULT 0,
              singles INTEGER DEFAULT 0,
              doubles INTEGER DEFAULT 0,
              triples INTEGER DEFAULT 0,
              sac_fly INTEGER DEFAULT 0,
              OBP REAL DEFAULT 0.0,
              BABIP REAL DEFAULT 0.0,
              SLG REAL DEFAULT 0.0,
              AVG REAL DEFAULT 0.0,
              ISO REAL DEFAULT 0.0,
              image TEXT,
              FOREIGN KEY (leagueID) REFERENCES league(leagueID),
              FOREIGN KEY (teamID) REFERENCES team(teamID)
          )
      """)

      cur.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_player_unique
        ON player(playerID);
      """)
      
      con.commit()
      con.close()
    
  def init_pitcher(self):
      # Create pitcher table
      con, cur = self.open_db()
      cur.execute("""
      
     
        CREATE TABLE IF NOT EXISTS pitcher (
            playerID INTEGER PRIMARY KEY,
            leagueID INTEGER NOT NULL,
            teamID INTEGER NOT NULL,
            name TEXT NOT NULL,
            wins INTEGER DEFAULT 0,
            losses INTEGER DEFAULT 0,
            era REAL DEFAULT 0.0,
            games_played INTEGER DEFAULT 0,
            games_started INTEGER DEFAULT 0,
            games_completed INTEGER DEFAULT 0,
            shutouts INTEGER DEFAULT 0,
            saves INTEGER DEFAULT 0,
            save_ops INTEGER DEFAULT 0,
            ip REAL DEFAULT 0.0,
            p_at_bats INTEGER DEFAULT 0,
            p_hits INTEGER DEFAULT 0,
            p_runs INTEGER DEFAULT 0,
            er INTEGER DEFAULT 0,
            p_hr INTEGER DEFAULT 0,
            p_hb INTEGER DEFAULT 0,
            p_bb INTEGER DEFAULT 0,
            p_so INTEGER DEFAULT 0,
            WHIP REAL DEFAULT 0.0,
            p_AVG REAL DEFAULT 0.0,
            k_9 REAL DEFAULT 0.0,
            bb_9 REAL DEFAULT 0.0,
            FOREIGN KEY (playerID) REFERENCES player(playerID),
            FOREIGN KEY (leagueID) REFERENCES league(leagueID),
            FOREIGN KEY (teamID) REFERENCES team(teamID)
        )
    """)
      
      cur.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_pitcher_unique
        ON pitcher(playerID);
      """)
      
      con.commit()
      con.close()
    
  def save_team(self):
    def keep_attrs(obj):
      keep = ['teamID', 'name', 'leagueID', 'league', 'logo', 'manager', 'players', 'lineup', 'positions', 'wins', 'losses', 'games_played', 'wl_avg', 'bat_avg', 'team_era', 'max_roster']
      dir_list = [x for x in keep if self.sql_safe(x)] 
      ##print(dir_list)
      return dir_list
    
    con, cur = self.open_db()

    if self.table_exists(con, cur, 'team'):
        #print('league exists--table team exists')
        
        objsTeam = self.league.get_all_objs()

        res = cur.execute(f"SELECT teamID FROM team")
        ret = res.fetchall()
        
        # check for league name duplicate 
        if len(ret) == 0:
          #print('no teams in db!')
          for i in range(len(objsTeam)):
            ##print('team to save:', objsTeam[i].name)
            team_name = objsTeam[i].name
            team = objsTeam[i]

            '''if self.scan_ret(ret, team.teamID):
              #print('teamID already exists!')
              continue'''
            
            dir_list = keep_attrs(team) 
            ##print(dir_list)
            cols = []
            vals = []
            ##print(exclude_attrs(team))

            for el in dir_list:
              val = getattr(team, el)
              ##print('val:', val, type(val))
              check_type = [int, str, float, dict, list, type(None)]

              if isinstance(val, (dict)):
                val = json.dumps(val)

              elif isinstance(val, (list)):
                roster = []
                for el in val:
                  ##print(el)
                  player_name = el.name
                  roster.append(player_name)
                
                roster_json = json.dumps(roster)
                ##print(roster_json, type(roster_json))
                val = roster_json
                el = 'players'
              
              elif type(val) not in check_type:
                league_name = val.name 
                val = league_name
              
              cols.append(el)
              vals.append(val)

            placeholders = ", ".join(["?"] * len(vals))
            column_str = ", ".join(cols)

            ##print(placeholders)
            ##print(column_str)
            ##print(vals)
            
            cur.execute(
                  f"INSERT INTO team ({column_str}) VALUES ({placeholders})",
                  tuple(vals)
              )
            
          con.commit()

        # check for league name duplicate 
        elif len(ret) >= 1:
          #print('teams in db!')
          res = cur.execute(f"SELECT teamID FROM team")
          ret = res.fetchall()

          for i in range(len(objsTeam)):
            ##print('team to save:', objsTeam[i].name)
            team = objsTeam[i]
            team_ID = team.teamID
            team_name = team.name

            if self.scan_ret(ret, team_ID):
              #print('teamID already exists!')
              self.update_team(con, cur, team, keep_attrs)
            
            else:
              dir_list = keep_attrs(team)
              ##print(dir_list)
              cols = []
              vals = []
              ##print(exclude_attrs(team))

              for el in dir_list:
                val = getattr(team, el)
                ##print('val:', val, type(val))
                check_type = [int, str, float, dict, list, type(None)]

                if isinstance(val, (dict)):
                  val = json.dumps(val)

                elif isinstance(val, (list)):
                  roster = []
                  for el in val:
                    ##print(el)
                    player_name = el.name
                    roster.append(player_name)
                  
                  roster_json = json.dumps(roster)
                  ##print(roster_json, type(roster_json))
                  val = roster_json
                  el = 'players'
                
                elif type(val) not in check_type:
                  league_name = val.name 
                  val = league_name
                
                cols.append(el)
                vals.append(val)

              placeholders = ", ".join(["?"] * len(vals))
              column_str = ", ".join(cols)

              ##print(placeholders)
              ##print(column_str)
              ##print(vals)
              
              cur.execute(
                    f"INSERT INTO team ({column_str}) VALUES ({placeholders})",
                    tuple(vals)
                )
              
            con.commit()

        con.close()
  
  def update_team(self, con, cur, team_obj, keep_func):
    #print('Update: ', team_obj.name)
    dir_list = keep_func(team_obj)
    team_name = team_obj.name 
    team_ID = team_obj.teamID 
    ##print(team_obj.games_played)

    ##print(dir_list)
    cols = []
    vals = []
    ##print(exclude_attrs(team))

    for el in dir_list:
      val = getattr(team_obj, el)
      ##print('val:', el, val, type(val))
      check_type = [int, str, float, dict, list, type(None)]

      if isinstance(val, (dict)):
        val = json.dumps(val)

      elif isinstance(val, (list)):
        roster = []
        for el in val:
          ##print(el)
          player_name = el.name
          roster.append(player_name)
        
        roster_json = json.dumps(roster)
        ##print(roster_json, type(roster_json))
        val = roster_json
        el = 'players'
      
      elif type(val) not in check_type:
        league_name = val.name 
        val = league_name
      
      cols.append(el)
      vals.append(val)

    #placeholders = ", ".join(["?"] * len(vals))
    #column_str = ", ".join(cols)

    set_clause = ", ".join([f"{col} = ?" for col in cols])
    sql = f"UPDATE team SET {set_clause} WHERE teamID = ?"

    ##print(cols)
    ##print(vals)
    ##print(sql)
    
    # modify command
    cur.execute(sql, vals + [team_ID])
    con.commit()
     
  def save_player(self):
    ##print('save player!')
    def keep_attrs_player(obj):
      keep = ['playerID', 'name', 'leagueID', 'teamID', 'number', 'team', 'positions', 'pa', 'at_bat', 'fielder_choice', 'hit', 'bb', 'hbp', 'so', 'hr', 'rbi', 'runs', 'singles', 'doubles', 'triples', 'sac_fly', 'OBP', 'BABIP', 'SLG', 'AVG', 'ISO', 'image']
      dir_list = [x for x in keep if self.sql_safe(x)] 
      return dir_list
    
    def keep_attrs_pitcher(obj):
      keep = ['name', 'playerID', 'teamID', 'leagueID', 'wins', 'losses', 'era', 'games_played', 'games_completed', 'shutouts', 'save_ops', 'ip', 'p_at_bats', 'p_hits', 'p_runs', 'er', 'p_hb', 'p_so', 'WHIP', 'p_avg', 'k_9', 'bb_9']
      dir_raw = dir(obj)
      dir_list = [x for x in keep if self.sql_safe(x)]
      return dir_list
    
    con, cur = self.open_db()

    if not self.table_exists(con, cur, 'team'):
      #print('team table does not exist!')
      return

    elif not self.table_exists(con, cur, 'player'):
      #print('player table does not exist!')
      return
      
    res = cur.execute("SELECT teamID FROM team")
    ret = [row[0] for row in res.fetchall()]

    # teams exist in the DB/league
    if len(ret) >= 1:
      objsTeam = self.league.get_all_objs()
      ##print(objsTeam)

      for i in range(len(objsTeam)):
        ##print('player team to save:', objsTeam[i])
        team = objsTeam[i]
        team_name = team.name 
        team_ID = team.teamID
        players = team.players

        res = cur.execute("SELECT playerID FROM player")
        ret = [row[0] for row in res.fetchall()]
          
        for player in players: 
          player_name = player.name 
          player_ID = player.playerID
          player_team_ID = player.teamID 
          isPitcher = 'pitcher' in player.positions 
          
          # does player exist in DB ???
          if player_ID in ret:
            #print('match player, wish to update?')

            # is the player a pitcher?
            # if yes, update pitcher and update player tables
            if isPitcher:
              #print('match pitcher, wish to update?')
              self.update_pitcher(con, cur, player, keep_attrs_pitcher)
              self.update_player(con, cur, player, keep_attrs_player) 
              continue

            # if not, update player table only
            self.update_player(con, cur, player, keep_attrs_player)
            continue

          # if playerID not in DB, create new player
          elif player_ID not in ret:
            #print('no match player, wish to create?')

            cols = []
            vals = []

            # if player is a pitcher 
            # exclude players attrs, except name, playerID, teamID, leagueID
            if isPitcher:
              #print('is a pitcher')
              res = cur.execute("SELECT playerID FROM pitcher")
              ret = [row[0] for row in res.fetchall()]

              dir_list = keep_attrs_pitcher(player)
              ##print(dir_list)
          
              for el in dir_list:
                val = getattr(player, el)
                ##print(val, type(val))

                if isinstance(val, (dict, list)):
                  ##print('player val:', el, val, type(val))
                  # represents player positions
                  val = json.dumps(val)

                cols.append(el)
                vals.append(val) 

              placeholders = ", ".join(["?"] * len(vals))
              column_str = ", ".join(cols)

              ##print(placeholders)
              ##print(column_str)
              ##print(cols)
              ##print(vals)
              
              cur.execute(
                    f"INSERT INTO pitcher ({column_str}) VALUES ({placeholders})",
                    tuple(vals)
                )
            
              con.commit()
          
          # reset cols and vals in case of Pitcher isntance
          cols = []
          vals = []

          # regardless of pitcher instance, update all Player attributes
          dir_list = keep_attrs_player(player)
          #print(dir_list)

          for el in dir_list:
            val = getattr(player, el)
            ##print(val, type(val))

            if isinstance(val, (dict, list)):
              ##print('player val:', el, val, type(val))
              # represents player positions
              val = json.dumps(val)

            cols.append(el)
            vals.append(val) 

          placeholders = ", ".join(["?"] * len(vals))
          column_str = ", ".join(cols)

          ##print(placeholders)
          ##print(column_str)
          ##print(cols)
          ##print(vals)
          
          cur.execute(
                f"INSERT INTO player ({column_str}) VALUES ({placeholders})",
                tuple(vals)
            )
        
          con.commit()

        self.update_team_roster(con, cur, players, team_ID)

    con.close()

  def update_player(self, con, cur, player_obj, keep_func):
    #print('update player:', player_obj.name)
    dir_list = keep_func(player_obj)
    team_name = player_obj.name 
    team_ID = player_obj.teamID
    player_ID = player_obj.playerID
    #print(player_obj.at_bat)

    ##print(dir_list)
    cols = []
    vals = []
    ##print(exclude_attrs(team))

    for el in dir_list:
      val = getattr(player_obj, el)
      ##print('val:', el, val, type(val))
      check_type = [int, str, float, dict, list, type(None)]

      if isinstance(val, (dict)):
        val = json.dumps(val)

      elif isinstance(val, (list)):
        pos = []
        for el in val:
          ##print(el)
          pos.append(el)
        
        pos_json = json.dumps(pos)
        ##print(roster_json, type(roster_json))
        val = pos_json
        el = 'positions'
      
      elif type(val) not in check_type:
        league_name = val.name 
        val = league_name
      
      cols.append(el)
      vals.append(val)

    #placeholders = ", ".join(["?"] * len(vals))
    #column_str = ", ".join(cols)

    set_clause = ", ".join([f"{col} = ?" for col in cols])
    sql = f"UPDATE player SET {set_clause} WHERE playerID = ?"

    #print(cols)
    #print(vals)
    #print(sql)
    
    # modify command
    cur.execute(sql, vals + [player_ID])
    con.commit()

  def update_pitcher(self, con, cur, player_obj, keep_func):
    #print('update player/pitcher:', player_obj.name)
    dir_list = keep_func(player_obj)
    team_name = player_obj.name 
    team_ID = player_obj.teamID
    player_ID = player_obj.playerID
    ##print(team_obj.games_played)

    ##print(dir_list)
    cols = []
    vals = []
    ##print(exclude_attrs(team))

    for el in dir_list:
      val = getattr(player_obj, el)
      ##print('val:', el, val, type(val))
      check_type = [int, str, float, dict, list, type(None)]

      if isinstance(val, (dict)):
        val = json.dumps(val)

      elif isinstance(val, (list)):
        pos = []
        for el in val:
          ##print(el)
          player_name = el.name
          pos.append(player_name)
        
        pos_json = json.dumps(pos)
        ##print(roster_json, type(roster_json))
        val = pos_json
        el = 'positions'
      
      elif type(val) not in check_type:
        league_name = val.name 
        val = league_name
      
      cols.append(el)
      vals.append(val)

    #placeholders = ", ".join(["?"] * len(vals))
    #column_str = ", ".join(cols)

    set_clause = ", ".join([f"{col} = ?" for col in cols])
    sql = f"UPDATE pitcher SET {set_clause} WHERE playerID = ?"

    print(cols)
    print(vals)
    print(sql)
    
    # modify command
    cur.execute(sql, vals + [player_ID])
    con.commit()
     
  def update_team_roster(self, con, cur, roster, teamID):
    res = cur.execute("SELECT teamID FROM team")
    ret = res.fetchall()
    roster_JSON = json.dumps([x.name for x in roster])
    team_ids = [row[0] for row in ret]

    ##print(ret)
    if len(ret) == 0:
      #print('No teams in league!')
      return
    
    if teamID in team_ids:
      #print('match: ', teamID)
      
      cur.execute(
          """UPDATE team 
          SET players = ? 
          WHERE teamID = ?
          """, 
          (roster_JSON, teamID)
        )
      
      con.commit()
      
  def sql_safe(self, val):
    return isinstance(val, (type(None), int, float, str))

  def save_csv(self, file_name=None):
    con, cur = self.open_db()
    cur

    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cur.fetchall()]

    for table in tables:
      cur.execute(f"SELECT * FROM {table}")
      rows = cur.fetchall()

      # Get column names (simulates `.headers on`)
      column_names = [description[0] for description in cur.description]

      with open(f"{table}.csv", "w", newline='', encoding='utf-8') as f:
          writer = csv.writer(f)
          writer.writerow(column_names)  # Write headers
          writer.writerows(rows)         # Write data

    con.close()

class Load():
  def __init__(self, db):
    self.db = db  
  
  def open_db(self):
    # Connect and insert
    con = sqlite3.connect(self.db, timeout=60)
    cur = con.cursor()
    return (con, cur)
  
  def load_csv_new(self, file_name):
    # Connect to SQLite database
    con, cur = self.open_db()

    table_name = os.path.splitext(os.path.basename(file_name))[0] 

    # Create table manually or dynamically from headers
    with open(file_name, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Simulates `.headers on`

        # Create table dynamically
        cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(headers)});")

        placeholders = ', '.join('?' * len(headers))
        #print(placeholders)
        #print(headers)
        
        cur.executemany(
            f"INSERT or IGNORE INTO {table_name} VALUES ({placeholders});",
            reader
        )

    con.commit()
    con.close()
  
  def load_csv_existing(self, file_name):
    # Connect to SQLite database
    con, cur = self.open_db()

    table_name = os.path.splitext(os.path.basename(file_name))[0] 

    # get leagueID in DB
    # get teamID in DB 
    # get playerID in DB

    # Create table manually or dynamically from headers
    with open(file_name, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Simulates `.headers on`

        # Create table dynamically
        cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(headers)});")

        placeholders = ', '.join('?' * len(headers))
        #print(placeholders)
        #print(headers)
        
        cur.executemany(
            f"INSERT or IGNORE INTO {table_name} VALUES ({placeholders});",
            reader
        )

    con.commit()
    con.close()


  def overwrite_league(self):
    print('leagueID exists!')
    pass 

  def overwrite_team(self):
    print('teamID exists!')
    pass

  def overwrite_player(self):
    print('playerID exists!')
    pass

  def overwrite_pitcher(self):
    print('player/pitcherID exists!')
    pass
    

    
    

def prompt_user():
  res = input("Would you like to start a new league? y/n")
  if res == 'y' or 'Y':
    print('start new league!')
  elif res == 'n' or 'N':
    print('load league!')
  else:
    print('Error\n')

#prompt_user()


league_1 = LinkedList(name='PBL') 
#league_2 = LinkedList(name='PBL 2')

save_1 = Save('stat_man.db', league_1) 
#save_2 = Save('stat_mg.db', league_2) 



team1 = Team(league_1, 'Team1', 'Manager', max_roster=10)
#team2 = Team(league_1, 'Team2', 'Manager', None, 15)
#team3 = Team(league_1, 'Team3', 'Manager', None, 17)

#team3 = Team(league_2, 'Team3', 'Manager', None, 16)
#team4 = Team(league_2, 'Team4', 'Manager', None, 21)

# should collide in tema field
#team5 = Team(league_2, 'Team4', 'Manager', None, 21)

# should not collide in tema field
#team6 = Team(league_2, 'Team5', 'Manager', None, 21)

league_1.add_team(team1)
#league_1.add_team(team2)
#league_1.add_team(team3)



#league_2.add_team(team3)
#league_2.add_team(team4)

#should collide
#league_2.add_team(team5)
# shold not collide
#league_2.add_team(team6)

# team 1
player1 = Player('Nick', 18, team1, league_1, ['1', '2', '3'])
player2 = Pitcher('James', 18, team1, league_1, ['pitcher', '2', '3'])
#player3 = Player('Frank', 18, team1, league_1,'None', ['pitcher', '2', '3'])
#player4 = Pitcher('Harold', 18, team1, league_1,'None', ['pitcher', '2', '3'])
#player5 = Pitcher('Albert', 18, team1, league_1,'None', ['1', '2', '3'])
#player6 = Player('Chance', 18, team1, league_1,'None', ['1', '2', '3'])
#player7 = Player('Allison', 18, team1, league_1,'None', ['1', '2', '3'])
#player8 = Player('Heather', 18, team1, league_1,'None', ['1', '2', '3'])
#player16 = Player('Jackson', 18, team1, league_1,'None', ['pitcher', '2', '3'])

# team 2
#player9 = Player('Nashon', 18, team2, league_1, 'None', ['1', '2', '3'])
#player14 = Player('Cranky', 18, team2, league_1, 'None', ['1', '2', '3'])

# team 3 
#player10 = Player('Cuckoo', 20, team3, league_1, 'None', ['left field', 'right field'])
#player15 = Player('Rooster', 20, team3, league_1, 'None', ['left field', 'right field'])

# team 3 
#player11 = Player('Alfortish', 20, team3, league_1, 'None', ['left field', 'right field'])

# team 1 
#player12 = Player('Alberforth', 20, team1, league_1, 'None', ['left field', 'right field'])
#player13 = Player('Alexis', 20, team1, league_1, 'None', ['left field', 'right field'])

# team 1
team1.add_player(player1)
team1.add_player(player2)
#team1.add_player(player3)
#team1.add_player(player4)
#team1.add_player(player5)
#team1.add_player(player6)
#team1.add_player(player7)
#team1.add_player(player8)
#team1.add_player(player12)
#team1.add_player(player13)
#team1.add_player(player16)

# team 2
#team2.add_player(player9)
#team2.add_player(player14)

# team 3
#team3.add_player(player10)
#team3.add_player(player11)
#team3.add_player(player15)
    
# update team test 
team1.set_games_played(10, league_1)
team1.set_wins(5, league_1)
team1.set_losses(5, league_1)

team1.set_games_played(11, league_1)

# update player test 
player1.set_at_bat(10)
player1.set_bb(5)
player2.set_games_played(1)
player2.set_ip(3)

# test calls 

#save_1.init_new_db() 
#save_2.init_db()

#save_1.save_team()

#save_1.save_player()

#save_1.save_csv()


# test load csv files to DB
load = Load('stat_man.db')

load.load_csv_new('pitcher.csv')
load.load_csv_new('player.csv')
load.load_csv_new('team.csv')
load.load_csv_new('league.csv')

















