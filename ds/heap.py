"""
Abstract class for all heaps
"""

class Node:
  def __init__(self, value):
    self.value = value
    pass

class Heap:
  @staticmethod
  def make_node(self, value):
    raise NotImplementedError("Class %s doesn't implement make_node()" % (self.__class__.__name__))
  
  def decrease_key(self, node, value):
    raise NotImplementedError("Class %s doesn't implement decrease_key()" % (self.__class__.__name__))
  
  def insert(self, node):
    raise NotImplementedError("Class %s doesn't implement insert()" % (self.__class__.__name__))

  def delete_min(self):
    raise NotImplementedError("Class %s doesn't implement delete_minimum()" % (self.__class__.__name__))
  
  def delete(self):
    raise NotImplementedError("Class %s doesn't implement delete()" % (self.__class__.__name__))


