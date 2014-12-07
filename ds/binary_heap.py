import math
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
  def __init__(self, heap_type = None, data = None):
    self.heap_type = heap_type
    self.location = {}
    if not heap_type:
      self.heap_type = min_heap
    self.tree = []
    if data:
      self.__make_heap(data)

  def insert(self, node):
    self.tree.append(node)
    self.location[node] = len(self.tree)-1
    self.__up_heap(len(self.tree)-1)

  def delete_min(self):
    if len(self.tree) == 0:
      return None
    elif len(self.tree) == 1:
      x = self.tree[0]
      self.location = {}
      self.tree = []
      return x
    else:
      x = self.tree[0]
      self.tree[0] = self.tree[-1]
      self.tree.pop(-1)
      for k in self.location:
        self.location[k] -= 1
      self.location[self.tree[0]] = 0
      self.location.pop(x, None)
      self.__down_heap(0)

      return x

  def decrease_key(self, node, new_val):
    assert(node.value >= new_val) 
    for k in self.location:
      print str(k.value) + ' ',
    print
    print node.value
    i = self.location[node]
    self.tree[i].value = new_val
    self.__up_heap(i)

  def to_string(self):
    if len(self.tree) == 0:
      return
    print_queue = [0]
    idx = 0
    level = 1 
    n = len(self.tree)
    while idx < len(print_queue):
      print self.tree[idx].value,
      left, right = self.__get_children(idx)
      if left < n:
        print_queue.append(left)
      if right < n:
        print_queue.append(right)
      if idx == math.pow(2,level) - 2:
        print
        level += 1
      elif idx % 2 == 1 and idx != print_queue[-1]:
        print ' <-> ',
      elif idx != print_queue[-1]:
        print ' || ',
      idx += 1

  def make_node(self, value):
    return BinaryHeapNode(value)
  
  def __up_heap(self, i):
    parent = int(math.floor((i-1)/2))
    if self.heap_type.compare(self.tree[i].value, self.tree[parent].value):
      self.__swap(i,parent)
      self.__up_heap(parent)

  def __down_heap(self,i):
    left, right = self.__get_children(i)
    val = self.tree[i].value
    lval = float('inf')
    rval = float('inf')
    if left:
      lval = self.tree[left].value
    if right:
      rval = self.tree[right].value
    if self.heap_type.compare(lval, val) and self.heap_type.compare(rval, val):
      child = self.__get_preferred_child(left, right)
      self.__swap(child, i)
    elif self.heap_type.compare(lval, val):
      self.__swap(left, i)
      self.__down_heap(left)
    elif self.heap_type.compare(rval, val):
      self.__swap(right, i)
      self.__down_heap(right)
    else:
      return

  def __make_heap(self, A):
    """
    Builds a heap out of array A
    """
    for el in A:
      self.insert(BinaryHeapNode(el))
    n = len(A)
    for i in xrange(int(math.ceil(n/2)),-1,-1):
      self.__heapify(i)

  def __get_children(self,i):
    """
    Returns left and  right child if they exist
    """
    left = 2*i + 1
    right = 2*i + 2
    if left >= len(self.tree):
      left = None
    if right >= len(self.tree):
      right = None
    return left, right
  
  def __get_preferred_child(self, i, j):
    if self.heap_type.compare(self.tree[i].value,self.tree[j].value):
      return i
    else:
      return j

  def __heapify(self, i):
    left, right = self.__get_children(i) 
    top = i
    n = len(self.tree)
    if left < n and self.heap_type.compare(self.tree[left].value, self.tree[top].value):
      top = left
    if right < n and self.heap_type.compare(self.tree[right].value, self.tree[top].value): 
      top = right
    if top != i:
      self.__swap(top, i)
      self.__heapify(top)

  def __swap(self, i, j):
    self.location[self.tree[i]] = j
    self.location[self.tree[j]] = i
    self.tree[j], self.tree[i] = self.tree[i], self.tree[j]
  
def test():
  A = [1,2,3,4,5,6]
  heap = BinaryHeap(min_heap, A)
  heap.insert(BinaryHeapNode(2))
  heap.to_string()
  heap.make_node(10)
  heap.decrease_key(heap.tree[1],1)
  heap.to_string()
if __name__ == '__main__': test()

