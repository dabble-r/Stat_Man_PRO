import math
from src.core.node import NodeStack


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
        self.tables = []
        self.table_check = ["leagueID", "teamID", "playerID", "pitcherID"]
        
  
    def add(self, table_name, row, values):
      self.tables.append(table_name)
      self.rows.append(row)
      self.values.append(values) 

    def popRow(self):
        self.rows.pop()
    
    def popValue(self):
        self.values.pop()
  
    def popTable(self):
      self.tables.pop()

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
      if len(self.tables) == 0:
          return None
      return self.tables[-1]
    
    def getType(self):
      table_name = self.getTable()
      value_hint = self.topValue()
      # zip keys in insertion order with aligned values list
      zipped = list(zip(self.topRow().keys(), value_hint))
      temp = {}
      if table_name == "league":
          temp['league'] = zipped
          self.instances.insert(0, temp)
      elif table_name == "team":
          temp['team'] = zipped
          self.instances.insert(1, temp)
      elif table_name == "player":
          temp['player'] = zipped
          self.instances.append(temp)
      elif table_name == "pitcher":
          temp['pitcher'] = zipped
          self.instances.append(temp)
      self.popRow()
      self.popValue()
      self.popTable()

    def getLeague(self):
        pass 
    
    def getTeam(self):
        pass 
    
    def getPlayer(self):
        pass 
    
    def getPitcher(self):
        pass
    
    def getInstances(self):
        # process all queued rows into instances, stop if indeterminate
        guard = 0
        while len(self.rows) > 0 and len(self.values) > 0 and guard < 10000:
            hint = self.getTable()
            if hint is None:
                break
            self.getType()
            guard += 1
        return self.instances
        
        
            
        

    
        
    
      

    def load_all_to_gui(self, attrs, vals):
        lst_attr = [x for x in attrs]
        lst_vals = [x for x in vals]
        print("instance type: ", lst_attr[0])
        print("attrs for gui: ", lst_attr)
        print("vals for gui: ", lst_vals)


  