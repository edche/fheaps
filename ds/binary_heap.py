import math
import random
from heap import Heap, Node
class HeapType:
  def compare(self, a, b):
    """True if a has priority over b"""
    pass
  def preferred(self,a,b):
    """ Returns the min/max for down-heap"""
    pass
  
class MinHeap(HeapType):
  def compare(self, a, b):
    return a < b

class MaxHeap(HeapType):
  def compare(self, a, b):
    return b < a

min_heap = MinHeap()
max_heap = MaxHeap()

class BinaryHeapNode(Node):
  def __init__(self, value):
    self.value = value

class BinaryHeap(Heap):
  def __init__(self, heap_type = None):
    self.heap_type = heap_type
    self.nodes = {} # keep track of node locations
    if not heap_type:
      self.heap_type = min_heap
    self.tree = [] # Use array to store

  def make_node(self, value):
    return BinaryHeapNode(value)

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
    parent = int(math.floor((idx-1)/2))
    if parent < 0: return
    # If the node is larger than its parent, swap and up_heap again.
    if self.heap_type.compare(self.tree[idx].value, self.tree[parent].value):
      self.__swap(idx, parent)
      self.__up_heap(parent)

  def __down_heap(self, idx):
    child = self.__get_preferred_child(idx)
    val = self.tree[idx].value
    if child:
      child_val = self.tree[child].value
      if self.heap_type.compare(child_val, val): #if child has higher priority, swap
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
    Gets the highest priority child if it exists. Otherwise, returns None
    """
    left, right = int(2*idx + 1), int(2*idx + 2)
    if left >= len(self.tree):
      left = None
    if right >= len(self.tree):
      right = None
    if left and right:      
      lval = self.tree[left].value
      rval = self.tree[right].value
      if self.heap_type.compare(lval, rval):
        return left
      else:
        return right
    elif left:
      return left
    elif right:
      return right
    else:
      return None

def test():
  b = BinaryHeap()
  nodes = []
  for i in range(100):
    nodes.append(b.make_node(random.random()))
    b.insert(nodes[i])
  for j in range(100):
    if random.random() > 0.5:
      x = b.delete_min()
      nodes.remove(x)
    else:
      rand = random.randint(0,len(nodes)-1)
      rand_node = nodes[rand]
      b.decrease_key(rand_node, rand_node.value - random.random())

if __name__ == '__main__': test()

