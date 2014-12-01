class FibonacciHeap:
  def __init__(self):
    self.min = None
    self.n = 0
    self.roots = []

  def insert(self, x):
    if self.min == None or self.min.value > x.value:
      self.min = x
    self.n += 1
    self.__root_append(x) 
    
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
    # If value is -Inf, then this was invoked from delete. Do not perform linking
    if min_el.value != float('-inf'):
      ranks = [None]*(self.__max_degree(self.n) + 1)
      orig_roots = []
      orig_roots.extend(self.roots)

      for x in orig_roots:
        r = x.rank
        while ranks[r] is not None:
          y = ranks[r]
          x,y = min(x,y), max(x,y)
          self.__link(x,y)
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

  def decrease_key(self, node, val):
    if val < 0:
      print 'The decreased value must be >= 0'
    node.value -= val
    if node not in self.roots:      
      self.__cascading_cut(node)   
    #Check if we need to update min
    if node.value < self.min.value:
      self.min = node
      
  def delete(self, node):
    if node == self.min:
      self.delete_min()
    else:
      self.decrease_key(node, float('inf'))
      self.delete_min()

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
        # If starting a new level, print the previous leve
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

  def __max_degree(self,n):
    """ 
    Upper bound is floor(lg(n))
    """
    lg = 0
    while n/2 > 0:
      lg += 1
      n = n/2
    return lg
  
  def __root_append(self, x):
    """
    Appends x to the list of roots nodes and maintains circular linked list
    """
    # If x came from another list, fix the pointers in that list
    x.left.right = x.right
    x.right.left = x.left

    if len(self.roots) == 0:
      x.left = x
      x.right = x
    elif len(self.roots) == 1:
      x.left = self.roots[0]
      x.right = self.roots[0]
      self.roots[0].left = x
      self.roots[0].right = x
    else:
      last = self.roots[-1]
      first = self.roots[0]
      x.left = last
      x.right = first
      last.right = x
      first.left = x
    self.roots.append(x)

  def __cascading_cut(self, x):
    # Cut x from its parent
    p = x.parent
    if x.right != x and p.child == x:
      p.child = x.right
    elif p.child == x:
      p.child = None
    p.rank -= 1
    x.parent = None

    # Add x to list of roots
    self.__root_append(x)

    # If p is not a root, we need to check for further cascading cuts
    if p not in self.roots:
      if p.mark:
        self.__cascading_cut(p)
      else:
        p.mark = True
        

class FibonacciHeapNode:
  def __init__(self, value):
    self.value = value
    self.rank = 0
    self.parent = None
    self.child = None
    self.left = self
    self.right = self
    self.mark = False


