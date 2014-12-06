import math
class Node:
  def __init__(self, val):
    self.value = val
    self.left = None # Left Child
    self.right = None # Right Child
    self.parent = None
    self.height = 0

class QuakeHeap():
  def __init__(self, alpha = 0.75):
    if alpha >= 1 or alpha <= 0.5:
      print 'Invalid alpha. Alpha in (0.5, 1). Setting alpha to 0.75'
    else:
      self.alpha = alpha
    self.roots = []
    self.leaves = []
    self.minimum = None
    self.n = 0

  def insert(self, x):
    """ Inserts Node object x as its own tree """
    self.roots.append(x)
    self.leaves.append(x)
    if self.minimum is None or x.value < self.minimum.value:
      self.minimum = x
    self.n += 1

  def decrease_key(self, x, diff):
    """ 
    Sets value of x to x.value - diff
    After updating value, cut its subtree out and make new tree
    """
    if diff < 0:
      print 'Diff must be non-negative'
    height = 0
    while x.parent and x.parent.value == x.value:
      x.value -= diff
      x = x.parent
      height += 1
    x.value -= diff
    # After while loop, x will be highest node reflecting the value
    self.__cut(x)
    # Update minimum if necessary
    if x.value < self.minimum.value:
      self.minimum = x
    x.height = height
  
  def delete_min(self):
    """
    Returns the minimum value of our Quake Heap and deletes this node.
    This is done by removing all paths containing x
    """
    x = self.minimum
    if not x:
      return None
    left, right = x.left, x.right
    height = x.height
    self.roots.remove(x)

    while left or right:
      if left and left.value == x.value:
        del left.parent
        right.height = height - 1
        self.__cut(right)
        left, right = left.left, left.right
      else:
        del left.parent
        left.height = height - 1
        self.__cut(left)
        left, right = right.left, right.right
      height -= 1
    self.n -= 1

    max_height = int(math.ceil(math.log(self.n, 1/self.alpha)))
    # Perform linking
    heights = [None] * (max_height + 1)
    orig_roots = []
    orig_roots.extend(self.roots)

    for root in orig_roots:
      h = root.height
      while heights[h]:
        y = heights[h]
        self.__link(root,y)
        heights[h] = None
        h += 1
      heights[h] = root 

    # Check for quakes
    current_level = []
    current_level.extend(self.leaves)

    for i in range(max_height):
      n_current = len(current_level)
      parent_level = []
      for node in current_level:
        if node.parent and node.parent not in parent_level:
          parent_level.append(node.parent)
      n_parent = len(parent_level)
      if n_parent > self.alpha*n_current:
        self.roots = current_level
        break
      else:
        current_level = parent_level
    return x.value

  def to_string(self):
    for root in self.roots:
      print_queue = []
      print_queue.append(root)
      while len(print_queue) > 0:
        # Append children of each level to print queue
        child_queue = []
        parent = print_queue[0].parent
        for job in print_queue:
          left, right = job.left, job.right
          if left:
            child_queue.append(left)
          if right:
            child_queue.append(right)
          print job.value,
          if job != print_queue[-1]:
            if job.parent == parent:
              print ' <-> ',
            else:
              print ' || ',
              parent = job.parent
        print_queue = child_queue
        print
      print '-----------------' 

  def __cut(self, x):
    """
    Cuts the node x from its parent and makes a new tree rooted at x
    If x is already a root, do nothing
    """
    if x.parent:
      if x.parent.left.value == x.value:
        x.parent.left = None
      else:
        x.parent.right = None
      x.parent = None
      self.roots.append(x)

  def __link(self, x, y):
    """
    Links trees of same height rooted at x and y
    """
    for root in self.roots:
      if root.value == x.value:
        self.roots.remove(root)
        break

    for root in self.roots:
      if root.value == y.value:
        self.roots.remove(root)
        break

    min_val = min(x.value, y.value)
    z = Node(min_val)
    self.roots.append(z)

    z.left = x
    z.right = y
    x.parent = z
    y.parent = z
    z.height = x.height + 1

def test():
  qh = QuakeHeap()
  a = Node(1)
  b = Node(2)
  c = Node(3)
  qh.insert(a)
  qh.insert(b)
  qh.insert(c)
  qh.delete_min()
  d = Node(4)
  e = Node(5)
  f = Node(6)
  qh.insert(d)
  qh.insert(e)
  qh.insert(f)
  qh.decrease_key(f,6)
  g = Node(1)
  h = Node(1)
  i = Node(1)
  qh.insert(g)
  qh.insert(h)
  qh.insert(i)
  qh.delete_min()
  qh.to_string()

if __name__ == '__main__': test()