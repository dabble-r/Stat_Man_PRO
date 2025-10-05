import math
from League.node import NodeStack


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
  

class InstanceStack():
    def __init__(self):
        self.name = "Instance Stack"
        self.instances = []
        self.rows = []
        self.values = []
        self.table_check = ["leagueID", "teamID", "playerID", "pitcherID"]
        
    
    def addRow(self, row):
        self.rows.append(row)
    
    def addValue(self, value):
        self.values.append(value) 

    def popRow(self):
        self.rows.pop()
    
    def popValue(self):
        self.values.pop()

    def peek(self):
        return self.instances[0]
    
    def get_length(self):
        return len(self.instances)
    
    def isEmpty(self):
        return len(self.instances) == 0 
    
    def topRow(self):
        top = self.rows[-1]
        return top 
    
    def topValue(self):
        top = self.values[-1]
        return top
    
    def getTable(self):
        while len(self.rows) != 0:
          top = self.topRow()
          table_hint = list(top.keys())[0] 
          if table_hint in self.table_check:
            return table_hint
        return None
    
    def getType(self):
        table_hint = self.getTable()
        value_hint = self.topValue()
        zipped = list(zip(self.topRow(), value_hint))
        temp = {}
        match table_hint:
            case "leagueID":
                temp['league'] = zipped
                self.instances.insert(0, temp)
                temp = {}
                
            case "teamID":
                temp["team"] = zipped
                self.instances.insert(1, temp)
                temp = {}
                
            case "playerID":
                temp["player"] = zipped
                self.instances.append(temp)
                temp = {}
                
            case "pitcherID":
                temp["pitcher"] = zipped
                self.instances.append(temp)
                temp = {}
        self.popRow()
        self.popValue()

    def getLeague(self):
        pass 
    
    def getTeam(self):
        pass 
    
    def getPlayer(self):
        pass 
    
    def getPitcher(self):
        pass
    
    def getInstances(self):
        self.getType()
        return self.instances
        
        
            
        

    
        
    
      

    def load_all_to_gui(self, attrs, vals):
        lst_attr = [x for x in attrs]
        lst_vals = [x for x in vals]
        print("instance type: ", lst_attr[0])
        print("attrs for gui: ", lst_attr)
        print("vals for gui: ", lst_vals)


  