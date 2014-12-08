import math
import random
from heap import Heap, Node

class DHeapNode(Node):
  def __init__(self, value):
    self.value = value

class DHeap(Node):
  def __init__(self, d):
    self.nodes = {} # keeps track of node locations    
    self.tree = [] # Use array to store nodes
    self.d = d

  def make_node(self, value):
    return DHeapNode(value) 

  def insert(self, node):
    self.tree.append(node)
    self.nodes[node] = len(self.tree) - 1
    self.__up_heap(len(self.tree) - 1)

  def delete_min(self):
    if len(self.tree) == 0:
      return None
    elif len(self.tree) == 1:
      min_el = self.tree[0]
      self.tree = []
      self.nodes = {}
      return min_el
    else:
      min_el = self.tree[0]
      self.__swap(0, len(self.tree)-1)
      self.tree.pop(-1)
      self.nodes.pop(min_el, None)
      self.__down_heap(0)
      return min_el

  def decrease_key(self, node, new_val):
    assert(node.value > new_val)
    node.value = new_val
    self.__up_heap(self.nodes[node])

  def __up_heap(self, idx):
    parent = int(math.floor((idx-1)/self.d))
    if parent < 0: return
    # If the node is larger than its parent, swap and up_heap
    if self.tree[idx].value < self.tree[parent].value:
      self.__swap(idx, parent)
      self.__up_heap(parent)
  
  def __down_heap(self, idx):
    child = self.__get_preferred_child(idx)
    val = self.tree[idx].value
    if child:
      child_val = self.tree[child].value
      if child_val < val:
        self.__swap(child, idx)
        self.__down_heap(child)

  def __swap(self, i, j):
    x = self.tree[i]
    y = self.tree[j]
    self.nodes[x] = j
    self.nodes[y] = i
    self.tree[i] = y
    self.tree[j] = x

  def __get_preferred_child(self, idx):
    """
    Gets the smallest child if it exists. Otherwise, returns None
    """
    low_idx = self.d*idx + 1
    high_idx = min(self.d*idx + self.d + 1, len(self.tree))
    child_range = range(low_idx,high_idx)
    best_child = None
    return_idx = 0
    for i in child_range:
      if best_child is None or self.tree[i].value < self.tree[best_child].value:
        best_child = i
    return best_child

def test():
  h = DHeap(4)
  nodes = []
  for i in range(100):
    nodes.append(h.make_node(random.random()))
    h.insert(nodes[i])
  for j in range(100):
    if random.random() > 0.5:
      x = h.delete_min()
      nodes.remove(x)
    else:
      rand = random.randint(0, len(nodes)-1)
      rand_node = nodes[rand]
      h.decrease_key(rand_node, rand_node.value - random.random())

if __name__ == '__main__': test()




