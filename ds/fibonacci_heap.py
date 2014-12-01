class FibonacciHeap:
  def __init__(self):
    self.min = None
    self.n = 0
    self.roots = []

  def insert(self, x):
    if self.min == None or self.min.value > x.value:
      self.min = x
    self.n += 1
    # Update pointers on linked list
    if len(self.roots) > 0:
      first = self.roots[0]
      last = self.roots[0]
      if len(self.roots) > 1:
        last = roots[-1]
      first.left = x
      last.right = x
      x.left = last
      x.right = first
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
    """ Melds itself with a new heap"""
    if self.min != None and heap.min != None:    
      if heap.min.value < self.min.value:
        self.min = heap.min
    elif heap.min != None:
      self.min = heap.min
    self.n += heap.n
    self.roots.extend(heap.roots)

  def print_trees(self):
    """
    Prints out the trees.
    New trees denoted with *s
    Levels denoted with '--' 
    Siblings denoted with <->
    Cousins separted by ||
    """
    
    # Print one tree at a time
    for root in self.roots:
      print_queue = [root]
      parent = None
      level_nodes = []
      levels = {}
      levels[root] = 0
      current_level = 0
      for job in print_queue:
        # If starting a new level, print the previous level
        if levels[job] != current_level:
          self.__print_level(level_nodes)
          level_nodes = []
          current_level = levels[job]
        first_child = job.child
        if first_child:
          print_queue.append(first_child)
          levels[first_child] = levels[job] + 1
          child = first_child.right
          while child != first_child:
            print_queue.append(child)
            levels[child] = levels[job] + 1
            child = child.right
        level_nodes.append(job)
      # print out the leaf layer
      if len(level_nodes) > 0:
        self.__print_level(level_nodes)
      # Separate trees with ***
      print '********************'
  
  def __print_level(self, level_nodes):
    parent = level_nodes[0].parent
    for node in level_nodes:
      if node != level_nodes[0]:
        if node.parent != parent:
          print '||',
          parent = node.parent
        else:
          print '<->',
      print node.value,
    print '\n--'

  def __link(self, x, y):
    """
    Links the two trees together
    Assumes x.value < y.value
    """
    
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
    """ 
    Upper bound is floor(lg(n))
    """
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

def tree_test():
  a = FibonacciHeapNode(6)
  b = FibonacciHeapNode(9)
  c = FibonacciHeapNode(12)
  d = FibonacciHeapNode(8)
  e = FibonacciHeapNode(16)
  f = FibonacciHeapNode(20)

  a.child = b 
  c.parent = a
  c.left = b
  c.right = d

  b.parent = a
  b.right = c
  b.left = d

  d.parent = a
  d.right = b
  d.left = c

  b.child = e
  e.parent = b

  c.child = f
  f.parent = c

  fheap = FibonacciHeap()
  fheap.insert(a)

  g = FibonacciHeapNode(7)
  h = FibonacciHeapNode(10)
  i = FibonacciHeapNode(40)
  j = FibonacciHeapNode(15)
  k = FibonacciHeapNode(14)
  l = FibonacciHeapNode(11)
  m = FibonacciHeapNode(18)
  
  g.child = h
  h.parent = g
  i.parent = g
  j.parent = g

  h.left = j
  h.right = i

  i.left = h
  i.right = j

  j.left = i
  j.right = h

  k.parent = h
  h.child = k
  l.parent = h
  k.left = l
  k.right = l
  l.left = k
  l.right = k

  m.parent = k
  k.child = m

  fheap.insert(g)
  

  fheap.print_trees()


if __name__ == "__main__":
  tree_test()
