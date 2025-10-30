import math

class Node():
  def __init__(self, team, next=None):
    self.team = team
    self.next = next

class LinkedList():
  COUNT = 0

  @classmethod
  def get_count(cls):
    return cls.COUNT 
  
  @classmethod
  def set_count(cls):
    cls.COUNT += 1
  
  def __init__(self, name, head=None):
    self.name = name
    self.admin = {
      "Comissioner": "first last",
      "Treasurer": "first last",
      "Communications": "first last",
      "Historian": "first last",
      "Recruiting": "first last"
    }
    self.year = "default"
    self.season = "default"
    self.location = "default"
    self.head = head 
  
  def __str__(self):
    if LinkedList.COUNT == 0:
      #print('No teams in league')
      return ''
    else:
      ret = "League\n"
      traverser = self.head
      while traverser.next != None:
        tmp = f'Team: {traverser.team.name}\n'
        ret += tmp
        tmp = ''
        traverser = traverser.next
      ret += f'Team: {traverser.team.name}\n'
      return ret
  
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
      if self.head.team.name == target:
        self.head = None
        LinkedList.COUNT = 0
        ##print(f'Removing {target}')
        return
      traverser = self.head
      while traverser.next is not None:
        prev = traverser 
        curr = traverser.next
        ##print('team name', traverser.team.name)
        if curr.team.name == target:
          ##print('found', target)
          prev.next = curr.next
          curr = None
          LinkedList.COUNT -= 1
          ##print(f'Removing {target}')
          return
        else:
          traverser = traverser.next 
      ##print('end of list')

class Team():
  def __init__(self, name, manager, max_roster=math.inf):
    self.name = name  
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
  
  # ------------------------------------------------------------------------ #
  # utilities

  def __str__(self): 
    ret = ''
    ##print(self.players)
    ret += f'Team: {self.name}\nManager: {self.manager}\nRoster: {self.get_size()} / {self.max_roster}\nPlayers: {[x.name for x in self.players]}\nG: {self.games_played}\nWins: {self.wins}\nLosses: {self.losses}\nW-L: {self.wl_avg}\nAVG: {self.bat_avg}\nTeam Era: {self.team_era}'
    return ret
  

league = LinkedList('Twst League')

beef = Team('beef', 'nick', 10)
s9 = Team('s9', 'nick', 10)
blues = Team('blues', 'nick', 10)
pelicans = Team('pelicans', 'nick', 10)
rougarou = Team('rougarou', 'nick', 10)

league.add_team(beef)
league.add_team(s9)
league.add_team(blues)
league.add_team(pelicans)
league.add_team(rougarou)

#league.remove_team('blues')
#league.remove_team('pelicans')
#league.remove_team('abc')

print(league)