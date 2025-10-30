

from __future__ import annotations
from PySide6.QtWidgets import QMessageBox
import math



class Player():
  def __init__(self, name, number, team, message, positions=[], parent=None):
    self.name = name 
    self.number = number 
    self.team = team
    self.positions = positions
    self.at_bat = 0 
    self.hit = 0 
    self.bb = 0
    self.so = 0
    self.hr = 0
    self.rbi = 0
    self.runs = 0
    self.singles = 0
    self.doubles = 0
    self.triples = 0
    self.sac_fly = 0
    self.BABIP = 0
    self.SLG = 0
    self.AVG = 0
    self.ISO = 0
    self.max = 0
    self.image = None

    #message box
    self.message = message
    #print('player initialized - msg inst', self.message)

    # message box self 
    self.parent = parent

  def __str__(self):
    ret = f'Name: {self.name}\nNumber: {self.number}\nPrimary Position: {self.positions[0]}\n  Secondary Positions: {self.positions[1:]}\n'
    ret += f'At Bats: {self.at_bat}\nHits: {self.hit}\nWalks: {self.bb}\nSO: {self.so}\nHR: {self.hr}\n'
    ret += f'Runs: {self.runs}\nRBI: {self.rbi}\nBABIP: {self.BABIP}\nSLG: {self.SLG}\nAVG: {self.AVG}\nISO: {self.ISO}' 
    return ret
  
  def check_graph_min(self):
    stats = ['at_bat', 'hit', 'bb', 'so'] 
    for stat in stats:
      val = getattr(self, stat)
      if val == 0:
        print('Sample chart, must update at bats, hits, walks, SOs !')
        return False 
    return True
  
  def set_min(self):
      #self.message.show_message('Sample chart. Player has no updated stats!')
      self.at_bat = 40 
      self.bb = 5 
      self.hit = 5 
      self.sac_fly = 5
      self.so = 5 
      self.hr = 5  
      self.singles = 5 
      self.doubles = 5 
      self.triples = 5
      

  def graph_view_format_player(self):
        sample_player = None
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
           sample_player = Player('Sample Player', 1, 'Sample Team', self.message, ['sample positions'])
           sample_player.set_min()
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
        #print(attrs)
        for el in attrs:
            #print(el)
            stat = el[0]
            val = el[1]
            #print(stat, val)
            stat_1 = ret[0]['Stat_1']
            stat_2 = ret[1]['Stat_2']
            if stat in on_base:
                #print(stat)
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
                #print(stat)
                if not stat_2:
                    ret[1]['Stat_2'] = 'Outs'
                    temp = {stat:val}
                    amt_lst_1 = ret[1]['Amount_2']
                    amt_lst_1.append(temp) 
                else:
                    temp = {stat:val}
                    #print(temp)
                    amt_lst_2 = ret[1]['Amount_2']
                    amt_lst_2.append(temp)
        return ret

  def format_player(self, raw_lst):
    team = raw_lst[0]
    name = raw_lst[1]
    number = raw_lst[2]
    #avg = self.AVG
    positions = raw_lst[3:]
    ##print(raw_lst)
    ##print('team', team)
    ##print('name', name)
    ##print('number', number)
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
      print('warn error msg inst', self.message)
      self.message.show_message(message)
      
  def _get_attrs(self):
      directory = dir(self)
      ret = []
      for el in directory:
        temp = getattr(self, el)
        if isinstance(temp, (int)):
            ##print(temp, el)
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
        ##print('invalid stat update')
        self._warn(f"{update.capitalize()} update total cannot exceed {stat.capitalize()} {curr_stat}.")
    else:
        #print('valid stat update')
        print('curr val:', stat, curr_stat)
        print('curr total:', total)
        print('new total:', new_total)
        setattr(self, update, new_val)
    
    # ------------------------------------------------------------------------ #
    # getters 

  def get_at_bat(self):                 return self.at_bat 
  
  def get_BABIP(self):                  return self.BABIP
  
  def get_SLG(self):                    return self.SLG
  
  def get_AVG(self):                    return self.AVG

  def get_ISO(self):                    return self.ISO 

    # ------------------------------------------------------------------------ #
    # setters 

  def set_at_bat(self, val):
    self.at_bat += val
    #self._add_stat('at_bat', val)
    '''if self.at_bat + val < 0:
      self.at_bat = 0
    else:
      #print('type val - at bat', type(val))
      self.at_bat += val'''
        
  def set_hit(self, val):
    self._validate_update('at_bat', 'hit', val)

    #self._add_stat('hit', val, maximum=self.at_bat)

    '''if self.at_bat == 0:
      self.hit = 0
    elif self.hit > self.at_bat:
      #print('excess hits')
    else:
      self.hit += val
      #print('hits proper limit')'''
  
  def set_bb(self, val):
    self._validate_update('at_bat', 'bb', val)
    #self._add_stat('bb', val, maximum=self.at_bat)
    '''if self.less_zero(self.bb, val):
      self.bb = 0
    else:
      self.bb += val
    '''
  
  def set_so(self, val):
    self._validate_update('at_bat', 'so', val)
  

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
    self._validate_update('at_bat', 'sac_fly', val)
    #self._add_stat('sac_fly', val, maximum=self.at_bat)
    '''if self.less_zero(self.sac_fly, val):
      self.sac_fly = 0
    else:
      self.sac_fly += val'''

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

    # ---------------------------------------------------------------------------------- #
    # calc functions
  
  def calc_BABIP(self):
    #(H - HR)/(AB - K - HR + SF)
    ret = 0
    if self.at_bat == 0:
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
    elif self.at_bat > 0 and self.hit <= self.at_bat:
      if (self.hit / self.at_bat) < 0:
        return self.format_decimal(ret)
      ##print(self.at_bat, self.hit)
      ret = self.hit / self.at_bat 
      return self.format_decimal(ret)
      
  def calc_ISO(self):
    #(1x2B + 2x3B + 3xHR) / At-bats OR Slugging percentage - Batting average
    ret = 0
    ##print('slg:', self.SLG)
    ##print('avg:', self.AVG)
    if self.at_bat == 0:
      return self.format_decimal(ret)
    if float(self.SLG) - float(self.AVG) > 0:
      ret = ( (1 * self.doubles) + (2 * self.triples) + (3 * self.hr ) ) / float(self.SLG) - float(self.AVG)
    return self.format_decimal(ret)

class Pitcher(Player):
  def __init__(self, name, number, team, message, positions=[]):
    super().__init__(name, number, team, message, positions=[])
  
    # player pitcher gen attr
    self.name = name 
    self.number = number 
    self.team = team
    self.positions = positions
    self.image = None
    self.message = message

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
    ret += f'Offense: ----- -----\n At Bats: {self.at_bat}\n Hits: {self.hit}\n Walks: {self.bb}\n SO: {self.so}\n HR: {self.hr}\n'
    ret += f' Runs: {self.runs}\n RBI: {self.rbi}\n BABIP: {self.BABIP}\n SLG: {self.SLG}\n AVG: {self.AVG}\n ISO: {self.ISO}\n' 
    ret += f'Pitching: ----- -----\n Wins: {self.wins}\n Losses: {self.losses}\n G: {self.games_played}\n ERA: {self.era}\n'
    ret += f' IP: {self.ip}\n At Bats: {self.p_at_bats}\n SO: {self.p_so}\n BB: {self.p_bb}\n AVG: {self.p_avg}\n WHIP: {self.WHIP}\n K9: {self.k_9}\n BB9: {self.bb_9}'
    return ret

  # -------- Validation Utilities --------

  def _show_error(self, message):
      #QMessageBox.warning(self.parent, "Input Error", message)
      print('show error - msg inst', self.message)
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

  

  '''def get_wins(self):
      return self.wins

    def get_losses(self):
      return self.losses

    def get_games_played(self):
      return self.games_played

    def get_era(self):
      return self.era

    def set_wins(self, val):
      if self.games_played > 0 and (self.wins + self.losses) == self.games_played:
          QMessageBox.warning(self.parent, "Input Error", "Update games played before wins and losses.")
          return 
      if (self.wins + val + self.losses) > self.games_played:
          QMessageBox.warning(self.parent, "Input Error", "Wins - Losses do not match total games played.")
          return 
      self.wins += val

    def set_losses(self, val):
      if self.games_played > 0 and (self.wins + self.losses) == self.games_played:
          QMessageBox.warning(self.parent, "Input Error", "Update games played before wins and losses.")
          return
      if (self.wins + val + self.losses) > self.games_played:
          QMessageBox.warning(self.parent, "Input Error", "Wins - Losses do not match total games played.")
          return 
      self.losses += val
      
    def set_games_played(self, val):
      self.games_played += val

    def set_era(self):
      ##print('set era')
      self.era = self.calc_era()

    def calc_era(self):
      ret = 0
      if self.ip == 0:
        return self.format_decimal(ret)
      ret = (self.er / self.ip) * 9 
      return self.format_decimal(ret)
    
    def set_er(self, val):
      self.er += val 
    
    def set_games_started(self, val):
      self.games_started += val 
    
    def set_games_completed(self, val):
      self.games_completed += val 
    
    def set_shutouts(self, val):
      self.shutouts += val 
    
    def set_saves(self, val):
      self.saves += val 
    
    def set_save_ops(self, val):
      self.save_ops += val 
    
    def set_ip(self, val):
      self.ip += val 
    
    def set_p_at_bats(self, val):
      self.p_at_bats += val
    
    def set_p_hits(self, val):
      self.p_hits += val 
    
    def set_p_runs(self, val):
      self.p_runs += val 
    
    def set_p_hr(self, val):
      self.p_hr += val 
    
    def set_p_hb(self, val):
      self.p_hb += val 
    
    def set_p_bb(self, val):
      self.p_bb += val 
    
    def set_p_so(self, val):
      self.p_so += val

    def set_WHIP(self):
      self.WHIP = self.calc_WHIP()

    def calc_WHIP(self):
      ret = 0
      if self.ip > 0:
        ret = (self.p_bb + self.p_hits) / self.ip
      return self.format_decimal(ret)
    
    def set_p_avg(self):
      self.p_avg = self.calc_p_AVG()
    
    def calc_p_AVG(self):
      ret = 0 
      if self.p_at_bats > 0:
        ret = self.p_hits / self.p_at_bats
      return self.format_decimal(ret)
    
    def set_k_9(self):
      self.k_9 = self.calc_k_9()

    def calc_k_9(self):
      ret = 0 
      if self.ip > 0:
        ret = (self.p_so / self.ip) * 9 
      return self.format_decimal(ret)
    
    def set_bb_9(self):
      self.bb_9 = self.calc_bb_9()

    def calc_bb_9(self):
      ret = 0 
      if self.ip > 0:
        ret = (self.bb / self.ip) * 9 
      return self.format_decimal(ret)

        self.games_started = 0 DONE
        self.games_completed = 0 DONE
        self.shutouts = 0 DONE
        self.saves = 0 DONE
        self.save_ops = 0 DONE
        self.ip = 0 DONE
        self.p_hits = 0 DONE
        self.p_runs = 0 DONE
        self.er = 0 DONE
        self.p_hr = 0 DONE
        self.p_hb = 0 DONE
        self.p_bb = 0 DONE
        self.p_so = 0 DONE
        self.WHIP = 0 DONE
        self.p_avg = 0 DONE
        self.k_9 = 0 DONE
        self.bb_9 = 0 DONE
        self.p_at_bats = 0 DONE
    
      '''

class Team():
  def __init__(self, name, manager, message, max_roster=math.inf):
    self.name = name  
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
    ##print(self.players)
    ret += f'Team: {self.name}\nManager: {self.manager}\nRoster: {self.get_size()} / {self.max_roster}\nPlayers: {[x.name for x in self.players]}\nG: {self.games_played}\nWins: {self.wins}\nLosses: {self.losses}\nW-L: {self.wl_avg}\nAVG: {self.bat_avg}\nTeam Era: {self.team_era}'
    return ret
  
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

  # order of funcs: 
  # format attrs players 
  # _get_attrs_all_dict
  # _get_attrs_all_lst
    
  def _get_attrs_all_dict(self, attrs_players):
      lst = attrs_players
      ret = {}
      for el in lst:
        stat, num = el 
        if stat != 'number':
          if stat == "AVG":
            float_avg = float(num)
            if stat in ret:
              #print(stat, float_avg, type(float_avg))
              ret[stat] += float_avg
            else: 
               ret[stat] = float_avg
          else:
              if stat in ret:
                 ret[stat] += num
              else:
                ret[stat] = num
      return ret
  
  def _get_attrs_all_lst(self, dict):
    ret = []
    for el in dict:
      stat = el 
      val = dict[el]
      ret.append((stat, val))
    return ret
  
  def check_num(self, val, attr):
    if attr == 'AVG':
      try:
        float_attr = float(val)
        if float_attr:
           return True
      except:
         print(f'error type attr: {attr}')
    else:
      if isinstance(val, (int)) or isinstance(val, (float)):
        return True 
    return False
  
  def _get_attrs_team(self):
    ret = []
    directory = dir(self)
    for el in directory:
       temp = getattr(self, el)
       if isinstance(temp, (int)):
          ret.append((el, temp))
    return ret
  
  def format_attrs_players(self):
    ret = []
    for player in self.players:
      directory = dir(player)
      for attr in directory:
        temp = getattr(player, attr)
        if self.check_num(temp, attr):
          #print(temp, el)
          ret.append((attr, temp))
    return ret
        
  def check_graph_min(self):
    if self.games_played == 0:
      return False
    else:
      return True
  
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
        #print(self)
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
        attrs = self.format_attrs_players()
        dict = self._get_attrs_all_dict(attrs)
        lst = self._get_attrs_all_lst(dict)
        lst_team = self._get_attrs_team()
        lst += lst_team
        #print('team graph view func:', lst)
        if sample_team:
           #print('sample team')
           attrs = sample_team.format_attrs_players()
           dict = sample_team._get_attrs_all_dict(attrs)
           lst = sample_team._get_attrs_all_lst(dict)
           lst += lst_team
        #print(attrs)
        for el in lst:
            #print(el)
            stat = el[0]
            val = el[1]
            #print(stat, val)
            stat_1 = ret[0]['Stat_1']
            stat_2 = ret[1]['Stat_2']
            if stat in team:
                #print(stat)
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
                #print(stat)
                if not stat_2:
                    ret[1]['Stat_2'] = 'Individual'
                    temp = {stat:val}
                    amt_lst_1 = ret[1]['Amount_2']
                    amt_lst_1.append(temp) 
                else:
                    temp = {stat:val}
                    #print(temp)
                    amt_lst_2 = ret[1]['Amount_2']
                    amt_lst_2.append(temp)
        return ret
  
  # string
  def return_dict(self, dict):
        ret = "" 
        ##print('return dict:', dict)
        for el in dict:
            #print('return dict:', el)
            ret += f"{el}:{dict[el]}\n"
        return ret
          
  # team lineup 
  # list of tuples
  def format_dict(self, dict):
        ret = []
        ret_dict = self.return_dict(dict).split("\n")
        ##print(ret_dict)
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
        ##print('formatted positions:', positions)
        ##print('formatted linuep:', lineup)
        ret += all
        ret.append(('Lineup', '----- -----'))
        ret += lineup
        ret.append(('Positions', '----- -----'))
        ret += positions
        ret.pop()
        ##print('return stats:', ret)
        return ret
  
  # -------------------------------------------------------------------------# 
  # getters 
  # graph view

  # ["Hits", "SO", "Runs", "ERA", "K"]
  def get_all_hits(self):
    total = 0
    for player in self.players:
      temp = player.hit
      total += temp 
    return total

  def get_all_so(self):
    total = 0
    for player in self.players:
      temp = player.so
      total += temp 
    return total
  
  def get_all_runs(self):
    total = 0
    for player in self.players:
      temp = player.runs
      total += temp 
    return total 
  
  def get_all_k(self):
    total = 0
    for player in self.players:
      pos = player.positions 
      if 'pitcher' in pos:
        temp = player.p_so 
        total += temp
    return total
  
  
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
        ##print(el)
        return el
    ##print('Player not found')
    return

  def get_manager(self):                return self.manager 

  def get_team_era(self):
    return self.team_era 

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
      #print(f'No position {order} in batting order. Try number less than {self.get_size() + 1}\n')
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
    #print("positions:\n", self.get_positions())
  
  def set_wl_avg(self):                 self.wl_avg = self.calc_wl_avg()

  def set_bat_avg(self):                self.bat_avg = self.calc_bat_avg()

  def set_manager(self, val):           self.manager = val
  
  def set_lineup(self, attr, stat, player, parent):      
    reply = self.ques_replace(attr, stat, parent)
    if reply == QMessageBox.StandardButton.No: 
      return
    self.lineup[stat] = player
    #print("positions:\n", self.get_positions())
  
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
      #print('Roster is full')
      return

  def remove_player(self, player):
    indx = None
    for i in range(len(self.players)):
      if self.players[i].name == player:
        ##print(self.players)
        ##print('index', i)
        ##print('player found\n', self.players[i])
        ##print('player found\n', self.players[i].name)
        indx = i
    self.players.pop(indx)
    return self.players
  

from PySide6.QtWidgets import QMessageBox, QDialog
#from team import beef, rougarou

class LinkedList():
  COUNT = 0

  @classmethod
  def get_count(cls):
    return cls.COUNT 
  
  @classmethod
  def set_count(cls):
    cls.COUNT += 1
  
  def __init__(self, head=None):
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

    # --------------------------------------------------------------- # 

  def format_decimal(self, num):
    return "{:.3f}".format(num)

  def __str__(self):
    ret = ''
    if LinkedList.COUNT == 0:
      #print('No teams in league')
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
        ##print('return dict:', dict)
        for el in dict:
            #print('return dict:', el)
            ret += f"{el}:{dict[el]}\n"
        return ret
          
  # team lineup 
  # list of tuples
  def format_dict(self, dict):
        ret = []
        ret_dict = self.return_dict(dict).split("\n")
        ##print(ret_dict)
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
        #print('return stats:', admin)
        return admin

  def ques_replace(self, attr, stat, parent):
    #print("admin:\n", attr, stat)
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
        ##print(f'Removing {target}')
        return
      
      elif self.head.team.name != target and LinkedList.COUNT == 1:
        return
      
      if self.head.team.name == target and LinkedList.COUNT > 1:
        curr = self.head
        self.head = curr.next
        curr = None
        LinkedList.COUNT -= 1
        ##print(f'Removing {target}')
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
      ##print('end of list')
  
  def find_team(self, target):
    traverser = self.head
    if traverser == None:
      ##print('No teams in league\n')
      return None
    if traverser.team.name == target:
      return traverser.team
    else:
      while traverser.next != None:
        if traverser.next.team.name == target:
          return traverser.next.team
        traverser = traverser.next 
    ##print('Team not found')
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
      #print('No teams in league')
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
    #print('attr:', attr)
    #print('stat:', stat)
    #print('val:', val)
    if 'Season' in stat:
      self.admin[stat] = val
      return
    
    reply = self.ques_replace(attr, stat, parent)
    if reply == QMessageBox.StandardButton.No: 
      return
    self.admin[stat] = val

    print("admin:\n", stat, val)

    # --------------------------------------------------------------------- #
  def get_name(self):
    return self.admin['League Name']
  
  def get_all_players_num(self):
    ret = []
    if LinkedList.COUNT == 0:
      #print('No teams in league')
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
      #print('No teams in league')
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
      #print("no team sin league")
      return ret 
    traverser = self.head 
    while traverser != None:
      name = traverser.team.name 
      roster = traverser.team.max_roster
      avg = self.format_decimal(float(traverser.team.get_bat_avg()))
      ret.append((name, roster, avg))
      traverser = traverser.next 
    return ret
  
  def get_all_objs(self):
    ret = []
    if LinkedList.COUNT == 0:
      #print("no team sin league")
      return ret 
    traverser = self.head 
    while traverser != None:
      team_obj = traverser.team
      ret.append(team_obj)
      traverser = traverser.next 
    return ret

  def get_all_wl(self):
    ret = []
    if LinkedList.COUNT == 0:
      #print("no team sin league")
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
      #print("no team sin league")
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
      #print('No teams in league')
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
    
  def graph_view_team_data_barset(self):
    ret = []
    teams = self.get_all_objs()
    for indx, team in enumerate(teams):
      # ["Hits", "SO", "Runs", "ERA", "K"]
      count = 'team' + str(indx)
      name = team.name 
      hits = team.get_all_hits()
      so = team.get_all_so()
      k = team.get_all_k()
      runs = team.get_all_runs()
      era = team.get_team_era()
      temp = (count, name, [hits, so, runs, era, k])
      ret.append(temp)
    #print(ret)
    return ret
  
  def graph_view_team_data_lineseries(self):
    ret = []
    teams = self.get_all_objs()
    for indx, team in enumerate(teams):
      # ["Hits", "SO", "Runs", "ERA", "K"]
      count = 'team' + str(indx)
      name = team.name 
      avg = team.get_bat_avg()
      temp = (count, name, avg)
      ret.append(temp)
    #print(ret)
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

  




# Dummy message handler (since QMessageBox isn't available here)
class DummyMessage:
    def show_message(self, text):
        print(f"[MESSAGE]: {text}")

msg = DummyMessage()



"""PySide6 port of the line/bar example from Qt v5.x"""

import sys
import math
from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QPainter, QPen, QColor, QFont
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCharts import (QBarCategoryAxis, QBarSeries, QBarSet, QChart,
                              QChartView, QLineSeries, QValueAxis)


from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCharts import (
    QChart, QChartView, QBarSeries, QBarSet,
    QBarCategoryAxis, QValueAxis, QLineSeries
)
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt, QPointF
import sys

class BarGraphWithDualAxes(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Team Stats with Batting Average")

        # 🟦 Bar Series with 5 values per bar
        self._bar_series = QBarSeries()
        categories = ["Hits", "SO", "Runs", "ERA", "K"]
        
        # 📈 Line Series for Batting AVG (0–1.000 range)
        self._line_series = QLineSeries()
        self._line_series.setName("AVG")
        
        pen = QPen(QColor(Qt.black))
        pen.setWidth(3)  # Optional: make the line thicker
        self._line_series.setPen(pen)

        # 📊 Chart Setup
        self.chart = QChart()
        self.chart.setTitle("Team Performance")
        self.chart.addSeries(self._bar_series)
        self.chart.addSeries(self._line_series)

        # 🧭 X Axis
        self._axis_x = QBarCategoryAxis()
        self._axis_x.append(categories)
        self.chart.addAxis(self._axis_x, Qt.AlignBottom)
        self._bar_series.attachAxis(self._axis_x)
        self._line_series.attachAxis(self._axis_x)

        # 🧮 Left Y Axis (Bar values)
        self._axis_y1 = QValueAxis()
        self._axis_y1.setTitleText("Team Stats")
        self._axis_y1.setRange(0, 100)
        self.chart.addAxis(self._axis_y1, Qt.AlignLeft)
        self._bar_series.attachAxis(self._axis_y1)

        # 📐 Right Y Axis (Batting AVG)
        self._axis_y2 = QValueAxis()
        self._axis_y2.setTitleText("Batting AVG")
        self._axis_y2.setRange(0, 1.000)
        self.chart.addAxis(self._axis_y2, Qt.AlignRight)
        self._line_series.attachAxis(self._axis_y2)

        # 🖼️ Chart View
        self._chart_view = QChartView(self.chart)
        self._chart_view.setRenderHint(QPainter.Antialiasing)
        self.setCentralWidget(self._chart_view)

        # 🏷️ Legend
        self.chart.legend().setVisible(True)
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        self.chart.legend().setFont(font)
        self.chart.legend().setAlignment(Qt.AlignBottom)

    def set_y1_range(self):
        lst = dir(self)
        max = 0
        for el in lst:
          if el == '_bar_series':
            #print(el)
            temp = getattr(self, el) 
            for set in temp.barSets():
               for i in range(set.count()):
                  value = set.at(i)
                  if value > max:
                    max = value
                  #print(f'value {value} at {i}')
        ret = round(max * 1.25)
        if len(str(ret)) >= 2:
          return round(ret, -1)
        return round(ret)
    
    def create_barset(self, teams):
      # self._bar_series.append(team1)
      # list of tuples - team number and 
      bar_series = getattr(self, '_bar_series')
      for team in teams:
        team, name, vals = team
        team = QBarSet(name)
        team.append(vals)
        bar_series.append(team)
    
    def create_line_series(self, teams):
      # self._bar_series.append(team1)
      # list of tuples - team number and 
      line_series = getattr(self, '_line_series')
      for indx, team in enumerate(teams):
        team, name, val = team
        #print(team, name, val)
        avg = float(val)
        #print(avg)
        temp = QPointF(indx, avg)
        line_series.append(temp)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    
    # ---------------- Create Players ---------------- #
    p1 = Pitcher("Max Velocity", 28, "pitcher", "Right", "Ace starter")
    p2 = Pitcher("Sam Slider", 30, "pitcher", "Right", "Breaking-ball specialist")
    p3 = Pitcher("Luis Changeup", 25, "pitcher", "Left", "Crafty control pitcher")
    p4 = Pitcher("Ryan Fastball", 32, "pitcher", "Right", "Power pitcher")
    p5 = Pitcher("Tom Knuckle", 27, "pitcher", "Right", "Unpredictable knuckleballer")

    
    # Pitcher 1 - John Heater (Power pitcher)
    p1.set_games_played(25)
    p1.set_wins(12)
    p1.set_losses(13)
    p1.set_p_at_bats(500)
    p1.set_p_hits(120)
    p1.set_p_hr(15)
    p1.set_p_bb(40)
    p1.set_p_so(190)
    p1.set_er(45)

    p1.set_at_bat(40)
    p1.set_hit(10)     # 10/40 = .250 AVG
    p1.set_runs(3)
    p1.set_hr(1)       # HR ≤ hits
    p1.set_rbi(4)
    p1.set_bb(2)
    p1.set_so(18)
    p1.set_sac_fly(0)

    # Pitcher 2 - Sam Slider (Breaking ball pitcher)
    p2.set_games_played(25)
    p2.set_wins(18)
    p2.set_losses(7)
    p2.set_p_at_bats(500)
    p2.set_p_hits(160)
    p2.set_p_hr(22)
    p2.set_p_bb(55)
    p2.set_p_so(150)
    p2.set_er(70)

    p2.set_at_bat(35)
    p2.set_hit(8)      # .229 AVG
    p2.set_runs(2)
    p2.set_hr(0)
    p2.set_rbi(3)
    p2.set_bb(3)
    p2.set_so(12)
    p2.set_sac_fly(1)

    # Pitcher 3 - Luis Changeup (Crafty lefty)
    p3.set_games_played(25)
    p3.set_wins(16)
    p3.set_losses(9)
    p3.set_p_at_bats(500)
    p3.set_p_hits(150)
    p3.set_p_hr(18)
    p3.set_p_bb(48)
    p3.set_p_so(165)
    p3.set_er(65)

    p3.set_at_bat(25)
    p3.set_hit(6)      # .240 AVG
    p3.set_runs(2)
    p3.set_hr(0)
    p3.set_rbi(2)
    p3.set_bb(1)
    p3.set_so(9)
    p3.set_sac_fly(0)

    # Pitcher 4 - Ryan Fastball (Flamethrower)
    p4.set_games_played(28)
    p4.set_wins(15)
    p4.set_losses(13)
    p4.set_p_at_bats(500)
    p4.set_p_hits(140)
    p4.set_p_hr(25)
    p4.set_p_bb(60)
    p4.set_p_so(220)
    p4.set_er(72)

    p4.set_at_bat(50)
    p4.set_hit(12)     # .240 AVG
    p4.set_runs(4)
    p4.set_hr(3)       # HR ≤ hits
    p4.set_rbi(6)
    p4.set_bb(4)
    p4.set_so(28)
    p4.set_sac_fly(1)

    # Pitcher 5 - Tom Knuckle (Knuckleballer)
    p5.set_games_played(29)
    p5.set_wins(7)
    p5.set_losses(22)
    p5.set_p_at_bats(500)
    p5.set_p_hits(175)
    p5.set_p_hr(20)
    p5.set_p_bb(50)
    p5.set_p_so(120)
    p5.set_er(85)      # fixed typo from set_era -> set_er

    p5.set_at_bat(20)
    p5.set_hit(2)      # .100 AVG
    p5.set_runs(0)
    p5.set_hr(0)
    p5.set_rbi(1)
    p5.set_bb(1)
    p5.set_so(10)
    p5.set_sac_fly(1)



    # ---------------- Create Teams ---------------- #
    team1 = Team("Thunderbolts", "Coach Carter", msg, max_roster=10)
    team2 = Team("Iron Giants", "Manager Lee", msg, max_roster=12)
    team3 = Team("Desert Scorpions", "Coach Alvarez", msg, max_roster=15)
    team4 = Team("Ocean Sharks", "Manager Kim", msg, max_roster=20)
    team5 = Team("Sky Hawks", "Coach Johnson", msg, max_roster=18)


    # ---------------- Add 1 Player to Each Team ---------------- #
    team1.add_player(p1)
    team2.add_player(p2)
    team3.add_player(p3)
    team4.add_player(p4)
    team5.add_player(p5)

    team1.set_bat_avg()
    team2.set_bat_avg()
    team3.set_bat_avg()
    team4.set_bat_avg()
    team5.set_bat_avg()

    league = LinkedList()
    league.add_team(team1)
    league.add_team(team2)
    league.add_team(team3)
    league.add_team(team4)
    league.add_team(team5)

    teams_graph_data = league.graph_view_team_data_barset()
    #print(teams_graph_data)
    teams_graph_data_line = league.graph_view_team_data_lineseries()


    window = BarGraphWithDualAxes()
    #window.create_barset([('team1', 'Beef Sliders', [1,2,3,4,5]), ('team2', 'Blues', [10,6,3,7,8]), ('team3', 'S9', [11,4,7,9,4]), ('team4', 'Pelicans', [12,5,9,10,22]), ('team5', 'Rougarou', [13,7,6,3,5])])
    #window.create_line_series([('team1', 'Beef Sliders', 0.432), ('team1', 'Beef Sliders', 0.500), ('team1', 'Beef Sliders', 0.375), ('team1', 'Beef Sliders', 0.600), ('team1', 'Beef Sliders', 0.190)])
    
    window.create_barset(teams_graph_data)
    window.create_line_series(teams_graph_data_line)
      

    max = window.set_y1_range()
    window._axis_y1.setRange(0, max)
    window.resize(1000, 750)

    

    window.show()


    sys.exit(app.exec())