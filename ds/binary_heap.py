import math
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

class BinaryHeap:
  def __init__(self, heap_type = None, data = None):
    self.heap_type = heap_type
    if not heap_type:
      self.heap_type = min_heap
    self.tree = []
    if data:
      self.__make_heap(data)

  def insert(self, value):
    self.tree.append(value)
    self.__up_heap(len(self.tree)-1)

  def delete(self, i):
    last_idx = len(self.tree) -1
    # Move last element to subtree rooted at i
    self.tree[i] = self.tree[last_idx]
    del self.tree[-1]
    self.__down_heap(i)

  def to_string(self):
    if len(self.tree) == 0:
      return
    print_queue = [0]
    idx = 0
    level = 1 
    n = len(self.tree)
    while idx < len(print_queue):
      print self.tree[idx],
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
  
  def __up_heap(self, i):
    parent = int(math.floor((i-1)/2))
    if self.heap_type.compare(self.tree[i], self.tree[parent]):
      self.__swap(i,parent)
      self.__up_heap(parent)

  def __down_heap(self,i):
    left, right = self.__get_children(i)
    val = self.tree[i]
    lval = self.tree[left]
    rval = self.tree[right]
    if self.heap_type.compare(lval, val) and self.heap_type.compare(rval, val):
      child = self.__get_preferred_child(left, right)
      self.__swap(child, i)
    elif self.heap_type.compare(lval, val):
      self.swap(left, i)
      self.__down_heap(left)
    elif self.heap_type.compare(rval, val):
      self.swap(right, i)
      self.__down_heap(right)
    else:
      return

  def __make_heap(self, A):
    """
    Builds a heap out of array A
    """
    self.tree = A
    n = len(A)
    for i in xrange(int(math.ceil(n/2)),-1,-1):
      self.__heapify(i)

  def __get_children(self,i):
    """
    Returns left and  right child if they exist
    """
    left = 2*i + 1
    right = 2*i + 2
    return left, right
  
  def __get_preferred_child(self, i, j):
    if self.heap_type.compare(self.tree[i],self.tree[j]):
      return i
    else:
      return j

  def __heapify(self, i):
    left, right = self.__get_children(i) 
    top = i
    n = len(self.tree)
    if left < n and self.heap_type.compare(self.tree[left], self.tree[top]):
      top = left
    if right < n and self.heap_type.compare(self.tree[right], self.tree[top]): 
      top = right
    if top != i:
      self.__swap(top, i)
      self.__heapify(top)

  def __swap(self, i, j):
    temp = self.tree[j]
    self.tree[j] = self.tree[i]
    self.tree[i] = temp
  
def test():
  A = [1, 7, 9, 8 ,3, 5]
  heap = BinaryHeap(min_heap, A)
  heap.insert(2)
  heap.delete(0)
  heap.to_string()
if __name__ == '__main__': test()

