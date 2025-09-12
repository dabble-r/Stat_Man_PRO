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
  



  