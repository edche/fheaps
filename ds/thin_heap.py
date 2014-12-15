import math
import random
from heap import Heap, Node

SIBLING_VIOLATION = 1
CHILD_VIOLATION = 2

class ThinHeapNode(Node):
  def __init__(self, value):
    self.value = value
    self.rank = 0
    self.parent = None
    self.child = None
    self.left = None
    self.right = None

class ThinHeap(Heap):
  def __init__(self):
    self.minimum = None
    self.n = 0
    self.roots = [] 

  def make_node(self, value):
    return ThinHeapNode(value)

  def insert(self, x):
    if self.minimum is None or self.minimum.value > x.value:
      self. minimum = x
    self.n += 1
    self.roots.append(x)

  def delete_min(self):
    if self.minimum is None:
      return None

    min_el = self.minimum
    self.roots.remove(min_el)
    self.n -= 1

    # Move Children to root
    child = min_el.child
    while child:
      next_child = child.right
      child.right = None
      child.left = None
      child.parent = None
      self.roots.append(child)
      child = next_child
    # Linking
    if len(self.roots) == 0:
      self.minimum = None
      return min_el
    
    ranks = [None for _ in range(self.n)] 
    orig_roots = []
    orig_roots.extend(self.roots)

    for root in orig_roots:
      r = root.rank
      while ranks[r] is not None:
        y = ranks[r]
        root = self.__link(root,y)
        ranks[r] = None
      ranks[r] = root
    #Update new minimum
    self.minimum = None
    for root in self.roots:
      if self.minimum is None or root.value < self.minimum.value:
        self.minimum = root
    return min_el
    
  def __link(self, x, y):
    """
    Links two thin heaps together
    Make y the leftmost child of x
    where x.value < y.value
    """
    # Swap values if necessary
    if x.value > y.value:
      x,y = y,x    
    y.parent = x
    if x.child:
      x.child.left = y
    y.right = x.child
    y.left = None
    x.child = y
    x.rank += 1
    self.roots.remove(y)
    return x

  def decrease_key(self, node, val):
    assert(node.value >= val)
    node.value = val
    parent = node.parent
    violation = None 
    if self.minimum.value > val:
      self.minimum = node

    if node.parent is None:
      return

    # Check to see if y is violated
    #y, violation = self.__check_violations(node) 
    self.__remove_from_child_list(node)

    while violation:
      if violation == SIBLING_VIOLATION:
        if y.child:
          marked = y.rank == y.child.rank + 2
        else:
          marked = y.rank == 1

        if marked:
          # Case 2b
          y.rank -= 1
          y, violation = self.__check_violations(y)
        else:
          # Case 2a
          # if y is unmarked and has no child, then it is not violated, so it must have a child if we are here
          w = y.child
          if w is None:
            return
          if w.right:
            y.child = w.right
            w.right.left = None
          if y.right:
            y.right.left = w
            w.right = y.right
          w.left = y
          y.right = w
          violation = None
      elif violation == CHILD_VIOLATION:
        self.__remove_from_child_list(y)
        if y.child:
          y.rank = y.child.rank + 1
        else:
          y.rank = 0
        y, violation = self.__check_violations(y)

  def __check_violations(self, node):
    """
    Checks for violations
    """
    if node.parent is None:
      return None, None
    if node.left:
      y = node.left
      sibling = True
    else:
      y = node.parent
      sibling = False

    if y.parent is None:
      # node y is a root (Case 1)
      if y.child:
        y.rank = y.child.rank + 1
      else:
        y.rank = 0
      return y, None
    else:
      if sibling:
        # Check for sibling violation
        if (y.right and y.right.rank == y.rank - 2) or (y.right is None and y.rank == 1):
          return y, SIBLING_VIOLATION
      else:
        # Check for child violation
        if (y.child and y.rank == y.child.rank + 3) or (y.child is None and y.rank == 2):
          return y, CHILD_VIOLATION
    return y, None
  
  def __remove_from_child_list(self, node):
    """
    Remove node from parent and add to root
    """
    parent = node.parent
    node.parent = None
    if node.left and node.right:
      # if node has left and right sibling
      node.left.right = node.right
      node.right.left = node.left
    elif node.right:
      # node is leftmost child
      parent.child = node.right
      node.right.left = None
      parent.rank = parent.child.rank + 1
    elif node.left:
      # Node is rightmost child
      node.left.right = None
    else:
      # Node has neither right nor left sibling
      parent.child = None
      parent.rank = 0
   
    # Add node to roots
    self.roots.append(node)

  
def test():
  t = ThinHeap()
  nodes = []
  for i in range(1000):
    node = t.make_node(random.random())
    t.insert(node)
    nodes.append(node)
  for j in range(1000):
    if random.random() > 0.5:
      x = t.delete_min()
      nodes.remove(x)
    else:
      rand_node = nodes[random.randint(0, len(nodes)-1)]
      t.decrease_key(rand_node, rand_node.value - random.random())
if __name__ == '__main__':
  test()






      


    
 




    


