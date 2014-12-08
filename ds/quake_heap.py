import math
import random
from heap import Heap, Node
class QuakeHeapNode(Node):
  def __init__(self, val):
    self.value = val
    self.name = 0
    self.left = None # Left Child
    self.right = None # Right Child
    self.parent = None
    self.height = 0

class QuakeHeap(Heap):
  def __init__(self, alpha = 0.75):
    if alpha >= 1 or alpha <= 0.5:
      print 'Invalid alpha. Alpha in (0.5, 1). Setting alpha to 0.75'
    else:
      self.alpha = alpha
    self.roots = []
    self.leaves = []
    self.minimum = None
    self.n = 0
    self.name = 0
    self.deleted = set() 
  
  def make_node(self, value):
    q = QuakeHeapNode(value)
    q.name = self.name
    self.name += 1
    return q

  def insert(self, node):
    self.roots.append(node)
    self.leaves.append(node)
    self.__update_min()
    self.n += 1

  def decrease_key(self, node, new_val):
    assert(node.value >= new_val)
    # Find highest instance of node.
    # node will always be a leaf
    node.value = new_val
    while node.parent:
      node.value = new_val
      if node.name != node.parent.name:
        break
      else:
        node = node.parent

    parent = node.parent
    node.parent = None
    if parent:
      if parent.left == node:
        sibling = parent.right
        parent.left = None
      else:
        sibling = parent.left
        parent.right = None
      if sibling is None:
        self.__update_heights(parent, 0)
      else:
        self.__update_heights(parent, sibling.height + 1)
      self.roots.append(node)
    node.value = new_val
    self.__update_min()

  def delete_min(self):
    if len(self.roots) == 0:
      return None
    x = self.minimum
    self.roots.remove(x)

    min_node = None
    for leaf in self.leaves:
      if leaf.name == x.name:
        min_node = leaf
        self.leaves.remove(leaf)
        self.deleted.add(leaf.name)
    assert(min_node is not None)

    # Remove path of nodes storing x
    left,right = x.left, x.right
    new_roots = []
    parent = x
    while left or right:
      parent.left = None
      parent.right = None
      if left and x.name == left.name:
        if right:
          right.parent = None
          new_roots.append(right)
        parent = left
        left, right = left.left, left.right
      elif right and x.name == right.name:
        if left:
          left.parent = None
          new_roots.append(left)
        parent = right
        left, right = right.left, right.right
    self.roots.extend(new_roots)

    # Perform linking
    max_height = int(math.ceil(math.log(self.n, 1/self.alpha))) + 1
    heights = [None]*(max_height)
    self.n -= 1
    orig_roots = []
    orig_roots.extend(self.roots)
    
    for root in orig_roots:
      h = root.height
      while heights[h] is not None:
        y = heights[h]
        root = self.__link(y,root)
        heights[h] = None
        h += 1
      heights[h] = root
    self.__update_min()

    # Check for quakes
    current_level = set() 
    current_level.update(self.leaves)

    new_roots = []

    for i in range(max_height):
      n_current = len(current_level)
      parent_level = set()
      for node in current_level:
        if node.parent and node.parent.name == node.name: 
          parent_level.add(node.parent)
        elif not node.parent:
          new_roots.append(node)
      n_parent = len(parent_level)
      if n_parent > self.alpha*n_current: 
        self.roots = list(current_level)
        self.roots.extend(new_roots)
        for root in self.roots:
          root.parent = None
        break
      else:
        current_level = parent_level

    for root in self.roots:
      if root.name in self.deleted:
        self.roots.remove(root)
    self.__update_min()
    return min_node

  def __update_min(self):
    self.minimum = None
    for root in self.roots:
      if self.minimum is None or self.minimum.value > root.value:
        self.minimum = root

  def __link(self, x, y):
    if x.value > y.value:
      x,y = y,x
    z = QuakeHeapNode(x.value)

    z.name = x.name
    z.height = x.height + 1
    z.left = x
    z.right = y
    x.parent = z
    y.parent = z
    self.roots.remove(x)
    self.roots.remove(y)
    self.roots.append(z)
    return z
  
  def __update_heights(self, node, new_h):
    """
    Update heights of node to new_h
    Bubbles up the heights to parent
    """
    parent = node.parent
    node.height = new_h
    if parent:
      if parent.left == node:
        sibling = parent.right
      else:
        sibling = parent.left
      if sibling is None or sibling.height < new_h:
        self.__update_heights(parent, new_h + 1)
      else:
        self.__update_heights(parent, sibling.height + 1) 
        
def test():
  q = QuakeHeap()
  nodes = []
  for i in range(100):
    nodes.append(q.make_node(random.random()))
    q.insert(nodes[i])
  for j in range(100):
    if random.random() > 0.5:
      x = q.delete_min()
    else:
      rand = random.randint(0,len(q.roots)-1)
      rand_node = q.roots[rand]
      q.decrease_key(rand_node, rand_node.value - random.random())

if __name__ == '__main__': test()
