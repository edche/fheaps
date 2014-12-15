from heap import Heap, Node
from copy import deepcopy
import random
import math

class FatHeapNode(Node):
  def __init__(self, value):
    self.value = value
    self.left = None # left sibling
    self.right = None # right sibling
    self.child = None
    self.parent = None
    self.rank = 0
    self.violated = False

class Inventory():
  def __init__(self):
    self.counter = [0] # ranks or violations
    self.ptrs = [[]] # stores ptrs to data type
    self.minimum = None
    self.n = 0

  def resize(self, new_size):
    old_size = len(self.counter)
    if new_size > old_size:
      diff = new_size - len(self.counter)
      self.counter.extend([0]*diff)
      new_ptr_list = [[] for _ in range(diff)]
      self.ptrs.extend(new_ptr_list)

class FatHeap(Heap):
  """
  We implement a simplified Fat Heap by Elmasry and Katajainen
  """
  def __init__(self):
    self.tree_inventory = Inventory()
    self.violation_inventory = Inventory()
    self.n = 0
    self.minimum = None

  def make_node(self, value):
    return FatHeapNode(value)

  def insert(self, node):
    self.tree_inventory.ptrs[0].append(node) 
    self.tree_inventory.counter[0] += 1
    self.n += 1
    self.tree_inventory.n += 1
    if self.n <= 1 or math.floor(math.log(self.n, 3)) > math.floor(math.log(self.n-1, 3)):
      self.tree_inventory.resize(self.n)
      self.violation_inventory.resize(self.n)

    if self.n > 1 and self.tree_inventory.n > 2*math.floor(math.log(self.n, 3)) + 2:
      self.__tree_reduction()
    if self.minimum is None or self.minimum.value > node.value:
      self.minimum = node
    if self.tree_inventory.minimum is None or self.tree_inventory.minimum.value > node.value:
      self.tree_inventory.minimum = node

  def delete_min(self):
    if self.n == 0:
      return None
    minimum = self.minimum
    assert(minimum is not None)
    self.n -= 1

    self.minimum = None
    if minimum == self.violation_inventory.minimum:
      # If minimum is a violated node (i.e. not a root), bubble it up
      minimum.violated = False
      self.violation_inventory.ptrs[minimum.rank].remove(minimum)
      self.violation_inventory.counter[minimum.rank] -= 1
      self.violation_inventory.n -= 1
      minimum = self.__bubble_up(minimum)
      # Update new violated minimum
      self.violation_inventory.minimum = None
      for r in range(len(self.violation_inventory.ptrs)):
        ptrs = self.violation_inventory.ptrs[r]
        for ptr in ptrs:
          if self.violation_inventory.minimum is None or self.violation_inventory.minimum.value > ptr.value:
           self.violation_inventory.minimum = ptr
           assert(r == ptr.rank)
      if minimum.value < self.tree_inventory.minimum.value:
        self.tree_inventory.minimum = minimum

    # Minimum is a root 
    if minimum in self.tree_inventory.ptrs[minimum.rank]:
      self.tree_inventory.ptrs[minimum.rank].remove(minimum)
      self.tree_inventory.n -= 1
      self.tree_inventory.counter[minimum.rank] -= 1
    child = minimum.child
    if child and child.right == child:
      child.right = None
    while child != None:
      next_child = child.right
      child.left = None
      child.right = None
      child.parent = None
      if child.violated:
        self.violation_inventory.ptrs[child.rank].remove(child)
        self.violation_inventory.counter[child.rank] -= 1
        self.violation_inventory.n -= 1
        if child == self.violation_inventory.minimum:
          self.violation_inventory.minimum = None
      child.violated = False
      if self.violation_inventory.minimum is None:
        for ptrs in self.violation_inventory.ptrs:
          for ptr in ptrs:
            if self.violation_inventory.minimum is None or self.violation_inventory.minimum.value > ptr.value:
              self.violation_inventory.minimum = ptr
      self.tree_inventory.ptrs[child.rank].append(child)
      self.tree_inventory.counter[child.rank] += 1
      self.tree_inventory.n += 1
      child = next_child
    self.tree_inventory.minimum = None

    # Check for tree reduction
    if self.n > 1 and self.tree_inventory.n > 2*math.log(self.n, 3) + 2:
      self.__tree_reduction()
    # Update minimum
    for i in range(len(self.tree_inventory.ptrs)):
      roots = self.tree_inventory.ptrs[i]
      if roots:
        for root in roots:
          if self.tree_inventory.minimum is None or self.tree_inventory.minimum.value > root.value:
            self.tree_inventory.minimum = root
    if self.violation_inventory.minimum is None or self.tree_inventory.minimum.value < self.violation_inventory.minimum.value:
      self.minimum = self.tree_inventory.minimum
    else:
      self.minimum = self.violation_inventory.minimum
    return minimum
  
  def decrease_key(self, node, new_val):
    assert(new_val < node.value)
    node.value = new_val
    if new_val < self.minimum.value:
      self.minimum = node
    # Roots cannot be violated
    if node.parent is not None:
      if self.violation_inventory.minimum is None or new_val < self.violation_inventory.minimum.value:
        self.violation_inventory.minimum = node
      if not node.violated:
        self.violation_inventory.ptrs[node.rank].append(node)
        self.violation_inventory.counter[node.rank] += 1
        self.violation_inventory.n += 1        
        node.violated = True
      #if self.violation_inventory.n > math.floor(math.log(self.n,3)) + 1:
        #self.__violation_reduction()
    else:
      if new_val < self.tree_inventory.minimum.value:
        self.tree_inventory.minimum = node      

  def __bubble_up(self, node):
    current = node

    node.violated = False
    while current.parent:
      parent = current.parent
      # Swap siblings
      parent_left = parent.left
      parent_right = parent.right
      current_left = current.left
      current_right = current.right

      if parent_left:
        parent_left.right = current
      if parent_right:
        parent_right.left = current

      current.left = parent_left
      current.right = parent_right

      if current_left:
        current_left.right = parent
      if current_right:
        current_right.left = parent

      parent.left = current_left
      parent.right = current_right

      # Swap parent child relationship
      grand_parent = parent.parent
      current_child = current.child
      parent.parent = current
      current.parent = grand_parent
      if parent.child == current:
        current.child = parent
      else:
        current.child = parent.child
      parent.child = current_child

      if grand_parent and grand_parent.child == parent:
        grand_parent.child = current

      # Fix children to point to new parents
      par_child = parent.child
      while par_child:
        if par_child != parent and par_child != current:
          par_child.parent = parent
        par_child = par_child.right

      cur_child = current.child
      while cur_child:
        if cur_child != current and cur_child != parent:
          cur_child.parent = current
        cur_child = cur_child.right
      current_rank = current.rank
      
      if parent.violated and parent in self.violation_inventory.ptrs[parent.rank]:
        self.violation_inventory.ptrs[parent.rank].remove(parent)
        self.violation_inventory.counter[parent.rank] -= 1
      if parent in self.tree_inventory.ptrs[parent.rank]:
        self.tree_inventory.ptrs[parent.rank].remove(parent)
        self.tree_inventory.counter[parent.rank] -= 1
      current.rank = parent.rank
      parent.rank = current_rank
      if parent.violated:
        self.violation_inventory.ptrs[parent.rank].append(parent)
        self.violation_inventory.counter[parent.rank] += 1
    
    if current not in self.tree_inventory.ptrs[current.rank]:
      self.tree_inventory.ptrs[current.rank].append(current)
      self.tree_inventory.counter[current.rank] += 1
    if current.value < self.tree_inventory.minimum.value:
      self.tree_inventory.minimum = current
    return current

  def __tree_reduction(self):
    for r in range(len(self.tree_inventory.ptrs)):
      for x in self.tree_inventory.ptrs[r]:
        assert(x.rank == r)
      while self.tree_inventory.counter[r] >= 3:
        new_tree = []
        for i in range(3):
          new_tree.append(self.tree_inventory.ptrs[r].pop())
          assert(r == new_tree[i].rank)
        min_idx = 0
        for i in range(1,3):
          if new_tree[i].value < new_tree[min_idx].value:
            min_idx = i
        root = new_tree[min_idx]
        assert(root.rank == r)
        root.rank += 1  
        for i in range(3):
          if i != min_idx:
            child = root.child
            if child:
              child.left = new_tree[i]
              new_tree[i].right = child
            root.child = new_tree[i]
            new_tree[i].parent = root
        self.tree_inventory.counter[r] -= 3
        self.tree_inventory.ptrs[r+1].append(root)
        self.tree_inventory.counter[r+1] += 1 
  
  def __violation_reduction(self):
    # Step 1: Find rank r such that:
    #   a)  u.rank==v.rank==r
    #   b) counter[r+1] <= 1
    for r in range(len(self.violation_inventory.ptrs) - 1):
      ptrs = self.violation_inventory.ptrs[r]
      while self.violation_inventory.counter[r] >= 2 and self.violation_inventory.counter[r+1] <= 1:
        u = ptrs.pop()
        v = ptrs.pop()
        u.violated = False
        v.violated = False
        self.violation_inventory.counter[r] -= 2
        self.violation_inventory.n -= 2
        self.__make_last_child(u)
        self.__make_last_child(v)
        if u.parent.value > v.parent.value:
          u, v = v, u
        self.__make_siblings(u,v)
        parent = u.parent
        assert(u.parent == v.parent)
        assert(parent.violated == False)
        min_node = u
        if v.value < min_node.value:
          min_node = v
        self.__make_last_child(min_node)
        assert(min_node.left == None)

        if min_node.value < parent.value:
          parent_left = parent.left
          parent_right = parent.right
          parent_parent = parent.parent
          new_left_child = min_node.right
          new_left_child.right = min_node.child
          if min_node.child:
            min_node.child.left = new_left_child          
          parent.child = parent.child.right.right
          if parent.child:
            parent.child.left = None

          min_node.parent = parent_parent
          min_node.left = parent_left
          min_node.right = parent_right
          min_node.child = parent
          parent.parent = min_node
          old_rank = min_node.rank
          min_node.rank = parent.rank
          parent.rank = old_rank

          if min_node.parent:
            self.violation_inventory.ptrs[min_node.rank].append(min_node)
            self.violation_inventory.counter[min_node.rank] += 1
            self.violation_inventory.n += 1 
        elif parent.parent is not None:
          parent.violated = True
          self.violation_inventory.ptrs[parent.rank].append(parent)
          self.violation_inventory.counter[parent.rank] += 1
          self.violation_inventory.n += 1
    return
  
  def __make_last_child(self, u):
    if (u.left != None):
      x = u.left
      while not (x.rank == u.rank + 1 and x not in self.violation_inventory.ptrs[u.rank+1]):
        x = x.left
        if x is None:
          return
      y = x.child
      assert(y.rank == u.rank)
      u_left = u.left
      u_right = u.right
      y_left = y.left
      y_right = y.right
      u_parent = u.parent

      u.parent = x
      u.left = y_left
      u.right = y_right
      if y_left:
        y_left.right = u
      if y_right:
        y_right.left = u

      y.parent = u_parent
      y.left = u_left
      y.right = u_right
      if u_left:
        u_left.right = y
      if u_right:
        u_right.left = y
    else:
      if u.parent.child != u:
        z = u.parent.child
        u_right = u.right
        u.left = None
        z.left = u
        z.right = u_right
        u.right = z
        u.parent.child = u

  def __make_siblings(self, u, v):
    if (u.parent != v.parent):
      y = v.right
      y_right = y.right
      y_left = y.left
      
      u_right = u.right
      u_left = u.left
      u_parent = u.parent

      u.parent = v.parent
      u.left = y_left
      u.right = y_right

      y.parent = u_parent
      y.left = u_left
      y.right = u_right           
        
def test():
  f = FatHeap()
  nodes = []
  for i in range(100):
    node = f.make_node(random.random())
    f.insert(node)
    nodes.append(node)
  while len(nodes) > 0:
    if random.random() > 0.5:
      print "delete min"
      x = f.delete_min()    
      nodes.remove(x)
    else:
      print "decrease key"
      rand_node = nodes[random.randint(0, len(nodes)-1)]
      f.decrease_key(rand_node, rand_node.value - random.random())

if __name__ == '__main__':
  test()

