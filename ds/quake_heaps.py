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
    self.minimum = None

  def insert(self, x):
    """ Inserts Node object x as its own tree """
    self.append(x)
    if self.minimum is None or x.value < self.minimum.value:
      self.minimum = x

  def decrease_key(self, x, diff):
    """ 
    Sets value of x to x.value - diff
    After updating value, cut its subtree out and make new tree
    """
    if diff < 0:
      print 'Diff must be non-negative'
    height = 0
    while x.parent.value == x.value:
      x.value -= diff
      x = x.parent
      height += 1
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

  def __cut(self, x):
    """
    Cuts the node x from its parent and makes a new tree rooted at x
    If x is already a root, do nothing
    """
    if x.parent:
      x.parent.child = None
      x.parent = None
      self.roots.append(x)


