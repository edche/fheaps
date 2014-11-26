class FibonacciHeap:
  def __init__(self):
    self.min = None
    self.n = 0
    self.roots = []

  def insert(self, x):
    if self.min == None or self.min.value > x.value:
      self.min = x
    self.n += 1
    self.roots.append(x)
    
  def find_min(self):
    return self.min   

  def delete_min(self):
    if self.min is None:
      return None      

    min_el = self.min
    self.roots.remove(min_el)
    
    if min_el.child != None:
      child_array = [min_el.child]
      child = min_el.child.right
   
      while child != min_el.child:
        child_array.append(child)
        child = child.right    
      self.roots.extend(child_array)
    
    # Linking and finding new min
    if self.roots is None:
      return min_el
    
    ranks = []
    for i in range(len(self.roots)):
      ranks.append(None)

    for x in self.roots:
      r = x.rank
      while ranks[r] != None:
        y = ranks[r]
        if y.value < x.value:
          __link(y,x)
        else:
          __link(x,y)
        ranks[r] = None
        r += 1
      ranks[r] = x      

    #Update new minimum
    new_min = self.roots[0]
    for x in self.roots:
      if x.value < new_min.value:
        new_min = x
    self.min = new_min
    return min_el
      
  def meld(self, heap):
    # Melds itself with a new heap
    if self.min != None and heap.min != None:    
      if heap.min.value < self.min.value:
        self.min = heap.min
    elif heap.min != None:
      self.min = heap.min
    self.n += heap.n
    self.roots.extend(heap.roots)
  
  def __link(self, x, y):
    # Links the two trees together
    # Assumes x.value < y.value
    
    # Removes y from doubly linked list in root list
    y.left.right = y.right
    y.right.left = y.left
    y.parent = x

    if x.child != None:
      x.child.right.left = y
      y.right = x.child.right
      y.left = x.child
      x.child.right = y
    else:
      x.child = y
      x.child.right = y
      x.child.left = y
    x.rank += 1
    y.mark = False
    self.roots.remove(y)

  def __max_degree(n):
    """ Upper bound is floor(lg(n))"""
    lg = 0
    while n/2 > 0:
      lg += 1
      n = n/2
    return lg

class FibonacciHeapNode:
  def __init__(self, value):
    self.value = value
    self.refresh()

  def refresh(self):
    self.rank = 0
    self.parent = None
    self.child = None
    self.left = self
    self.right = self
    self.mark = False

if __name__ == "__main__":
  fheap = FibonacciHeap()
  x = FibonacciHeapNode(10)
  y = FibonacciHeapNode(7)
  fheap.insert(x)
  fheap.insert(y)
  print fheap.find_min().value
  fheap.delete_min()
  print fheap.find_min().value
  h2 = FibonacciHeap()
  z = FibonacciHeapNode(5)
  h2.insert(z)
  fheap.meld(h2)
  print fheap.find_min().value

