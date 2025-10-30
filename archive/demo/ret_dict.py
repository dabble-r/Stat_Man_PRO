class Team():
  def __init__(self, max_roster=25):
    self.name = 'test'
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
  
  def __str__(self): 
    ret = ''
    #print(self.players)
    ret += f'Team: {self.name}'
    return ret

  # string
  def return_dict(self, dict):
        ret = "" 
        for el in dict:
            ret += f"{el}:{dict[el]}\n"
        return ret
          
  # team lineup 
  # list of tuples
  def format_dict(self, dict):
        ret = []
        ret_dict = self.return_dict(dict).split("\n")
        #print(ret_dict)
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
        print('formatted positions:', positions)
        ret += all
        ret.append(('Lineup', '----- -----'))
        ret += lineup
        ret.append(('Positions', '----- -----'))
        ret += positions
        ret.pop()
        return ret


test = Team()
print(test)
#print(test.return_stats())
test.lineup['4'] = 'Nick'
existing = getattr(test, 'lineup')['4']
print(existing)