from PySide6.QtWidgets import QMessageBox

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

class Player():
  def __init__(self, name, number, team, positions=[], parent=None):
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

    # message box self 
    self.parent = parent

  def _warn(self, message):
      QMessageBox.warning(self.parent, "Stat Input Error", message)

  def _get_attrs(self):
      directory = dir(self)
      ret = []
      for el in directory:
        temp = getattr(self, el)
        if isinstance(temp, (int)):
            #print(temp, el)
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
    curr = getattr(self, stat)
    #print('curr:', curr)
    total = self._get_max(update)
    #print('new:', new)
    new_total = total + val
    if new_total > curr:
        #print('invalid stat update')
        self._warn(f"{stat} update total {new_total} cannot exceed {curr}.")
    else:
        print('valid stat update')
        setattr(self, stat, new_total)

#test = Player("nick", 18, 'beef', ['left field'])

#ret = test._get_attrs()
#print(ret)

#test.at_bat = 6
#test.hit = 5
#test.singles = 3 
#test.doubles = 1

#test._validate_update('at_bat', 'hit', 2)
#test._validate_update('hit', 'singles', 3)


class Stack():
  def __init__(self):
    self.name = "Undo Stat Stack"
    self.lst = []
    
  def __str__(self):
    ret = ''
    if self.is_empty():
      ret = 'Stack Empty'
      return ret
    for indx, node in enumerate(self.lst):
      ret += f"{indx+1}:  Obj: {node.name} - Stat: {node.stat} - L: {node.prev}\n\n" 
    return ret
  
  def is_empty(self):
    return len(self.lst) == 0
    #return self.head is None
  
  def get_size(self):
    return len(self.lst)
  
  def get_first(self):
    if self.is_empty():
      return None
    return self.lst[0]
  
  def get_last(self):
    if self.is_empty():
      return None
    last = self.lst[-1]
    return last
  
  def get_second_last(self):
    if self.is_empty():
      return None 
    if len(self.lst) >= 2:
      return self.lst[-2]
    
  def add_node(self, obj, team, stat, prev, func, flag, player=None):
    new_node = NodeStack(obj, team, stat, prev, func, flag, player=None)
    self.lst.append(new_node)
  
  def remove_last(self):
    if self.is_empty():
      return 
    self.lst.pop()
  
  def undo_exp(self):
    if self.is_empty():
      return 
    
    last_action = self.get_last()
    obj, team, stat, prev, func, flag, player = last_action
    
    #func(stat, prev)
    setattr(obj, stat, prev)
    #print(team, stat, prev, func, flag, player)

    self.remove_last()
    
class Test():
  def __init__(self, name, wins, losses, games_played):
    self.name = name 
    self.wins = wins 
    self.losses = losses 
    self.games_played = games_played
  
  def __str__(self):
    ret = ''
    ret += f"G: {self.games_played} W: {self.wins} L: {self.losses}"
    return ret

  def add(self, stat, val):
    setattr(self, stat, (getattr(self, stat)+val))

  def text(self, stat, val):
    setattr(self, stat, val)
  
stack = Stack()
test = Test(None, 0, 0, 0)

stack.add_node(test, 'team name', 'games_played', test.games_played, test.add, 'team')
print('prev:', test.games_played)
test.add("games_played", 10)

stack.add_node(test, 'team name', 'wins', test.wins, test.add, 'team')
test.add("wins", 10)

last = stack.get_last()
obj, team, stat, prev, func, flag, player = last 
#print(team, stat, prev, func, flag, player)

stack.undo_exp()
stack.undo_exp()
print(test)
#print(stack)

