from heap import Heap, Node
import random
import math

class FibonacciHeapNode(Node):
  def __init__(self, value):
    self.value = value
    self.rank = 0
    self.parent = None
    self.children = []
    self.mark = False

class FibonacciHeap(Heap):
  def __init__(self):
    self.min = None
    self.n = 0
    self.roots = []

  def make_node(self, value):
    return FibonacciHeapNode(value)

  def insert(self, x):
    if self.min is None or self.min.value > x.value:
      self.min = x
    self.n += 1
    self.roots.append(x)

  def delete_min(self):
    if self.min is None:
      return None      

    min_el = self.min
    self.roots.remove(min_el)
    self.n -= 1
    
    # Move children to root
    for child in min_el.children:
      child.parent = None
    self.roots.extend(min_el.children)
    
    # Linking and finding new min
    if len(self.roots) == 0:
      self.min = None
      return min_el
    
    ranks = [None]*(int(math.ceil(math.log(self.n, 2)) + 1))
    orig_roots = []
    orig_roots.extend(self.roots)

    for root in orig_roots:
      r = root.rank
      while ranks[r] is not None:
        y = ranks[r]
        root = self.__link(root,y)
        ranks[r] = None
        r += 1
      ranks[r] = root      

    #Update new minimum
    new_min = self.roots[0]
    for root in self.roots:
      if root.value < new_min.value:
        new_min = root
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
    assert(val <= node.value)
    node.value = val
    if node not in self.roots:      
      self.__cascading_cut(node)   
    #Check if we need to update min
    if node.value < self.min.value:
      self.min = node
      
  def delete(self, node):
    if node == self.min:
      self.delete_min()
    else:
      self.decrease_key(node, float('-inf'))
      self.delete_min()

  def to_string(self): 
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
          print_queue.extend(job.children)
          for child in job.children:
            levels[child] = levels[job] + 1
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
    """
    # Swap values if necessary
    if x.value > y.value:
      x,y = y,x

    y.parent = x
    # Add y to list of x's children
    x.children.append(y)
    x.rank += 1
    y.mark = False
    self.roots.remove(y)
    return x
 
  def __cascading_cut(self, x):
    # Cut x from its parent
    p = x.parent
    if p:
      p.children.remove(x)
      p.rank -= 1
      x.parent = None
      self.roots.append(x)

      # If p is not a root, we need to check for further cascading cuts
      if p not in self.roots:
        if p.mark:
          self.__cascading_cut(p)
        else:
          p.mark = True

def test():
  f = FibonacciHeap()
  nodes = []
  for i in range(100):
    nodes.append(f.make_node(random.random()))
    f.insert(nodes[i])
  for j in range(100):
    if random.random() > 0.5:
      x = f.delete_min()
      nodes.remove(x)
    else:
      rand = random.randint(0,len(nodes)-1)
      rand_node = nodes[rand]
      f.decrease_key(rand_node, rand_node.value - random.random())

if __name__ == '__main__':
  test()



