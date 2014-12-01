from fibonacci_heap import FibonacciHeap, FibonacciHeapNode
def print_test():
  print "BEGIN PRINT TEST"
  print "FIGURE 1a IN TARJAN"
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
  print "END PRINT TEST"

def delete_min_test():
  print "BEGIN DELETE MIN:"
  print "FIGURE 3 IN TARJAN PAPER"
  a = FibonacciHeapNode(3)
  b = FibonacciHeapNode(4)
  c = FibonacciHeapNode(5)
  d = FibonacciHeapNode(14)

  a.child = b
  b.parent = a
  c.parent = a
  d.parent = b
  b.child = d

  b.left = c
  b.right = c
  c.left = b
  c.right = b

  e = FibonacciHeapNode(6)
  f = FibonacciHeapNode(7)
  g = FibonacciHeapNode(18)
  h = FibonacciHeapNode(11)
  
  e.child = f
  f.parent = e
  g.parent = e
  h.parent = f
  f.child = h

  f.left = g
  f.right = g
  g.left = f
  g.right = f

  i = FibonacciHeapNode(8)
  j = FibonacciHeapNode(10)

  j.parent = i
  i.child = j

  k = FibonacciHeapNode(12)

  fheap = FibonacciHeap()
  fheap.insert(a)
  fheap.insert(e)
  fheap.insert(i)
  fheap.insert(k)
  fheap.n = 11
  a.rank = 2
  b.rank = 1
  e.rank = 2
  f.rank = 1
  i.rank = 1

  print "ORIGINAL:"
  fheap.print_trees()
  
  print "DELETE MIN"
  fheap.delete_min()
  fheap.print_trees()
  print "END DELETE MIN"
def dec_key_del_test():
  print '************************'
  print 'BEGIN DECREASE KEY + DELETE TEST'
  print 'FIGURE 5 in TARJAN PAPER'
  print 'ORIGINAL:'
  a = FibonacciHeapNode(4)
  b = FibonacciHeapNode(7)
  
  b.parent = a
  a.child = b

  c = FibonacciHeapNode(8)
  c.left = b
  c.right = b
  b.left = c
  b.right = c
  c.parent = a

  d = FibonacciHeapNode(12)
  d.parent = b
  b.child = d

  e = FibonacciHeapNode(10)
  e.left = d
  d.right = e
  e.parent = b

  f = FibonacciHeapNode(9)
  e.right = f
  d.left = f
  f.right = d
  f.left = e
  f.parent = b

  g = FibonacciHeapNode(15)
  g.parent = e
  e.child = g

  h = FibonacciHeapNode(3)
  i = FibonacciHeapNode(14)
  i.parent = h
  h.child = i

  j = FibonacciHeapNode(5)
  j.left = i
  j.right = i
  i.left = j
  i.right = j 
  j.parent = h

  fheap = FibonacciHeap()
  fheap.insert(a)
  fheap.insert(h)
  fheap.n = 10
  print '************************'
  print 'ORIGINAL: FIG 5a)'
  fheap.print_trees()
  print 'Min = %d' % (fheap.find_min().value)

  print 'DECREASE_KEY(10,4)'
  print 'FIG 5b)'
  fheap.decrease_key(e,4)
  fheap.print_trees()

  print 'DELETE 7'
  print 'FIG 5c)'
  fheap.delete(b)
  fheap.print_trees()
  print 'Min = %d' % (fheap.find_min().value)

  print 'END DECREASE KEY + DELETE TEST'
  print '************************'
def cascading_cut_test():
  print '************************'
  print 'BEGIN CASCADING CUT TEST'
  print 'FIGURE 6 in TARJAN PAPER'
  a = FibonacciHeapNode(2)
  b = FibonacciHeapNode(20)

  a.child = b
  b.parent = a

  c = FibonacciHeapNode(4)
  b.left = c
  b.right = c
  c.parent = a
  c.left = b
  c.right = b
  c.mark = True

  d = FibonacciHeapNode(5)
  d.parent = c
  c.child = d
  d.mark = True

  e = FibonacciHeapNode(8)
  e.left = d
  d.right = e
  e.parent = c

  f = FibonacciHeapNode(11)
  f.parent = c
  f.left = e
  f.right = d
  d.left = f
  e.right = f

  g = FibonacciHeapNode(9)
  g.parent = d
  d.child = g
  g.mark = True

  h = FibonacciHeapNode(6)
  h.parent = d
  h.left = g
  g.right = h

  i = FibonacciHeapNode(14)
  i.parent = d
  i.left = h
  i.right = g
  g.left = i
  h.right = i

  j = FibonacciHeapNode(10)
  j.parent = g
  g.child = j

  k = FibonacciHeapNode(16)
  j.left = k
  j.right = k
  k.left = j
  k.right = j
  k.parent = g

  l = FibonacciHeapNode(12)
  l.parent = j
  j.child = l

  m = FibonacciHeapNode(15)
  m.parent = j
  m.left = l
  m.right =l
  l.left = m
  l.right = m

  fheap = FibonacciHeap()
  fheap.insert(a)
  fheap.n = 13
  print 'ORIGINAL:'
  fheap.print_trees()
  fheap.decrease_key(j, 3)
  print '************************'
  print 'DECREASE_KEY(10,3)'
  fheap.print_trees()
  print 'END CASCADING CUT TEST'
  print '************************'
if __name__ == "__main__":
  print_test()
  delete_min_test()
  dec_key_del_test()
  cascading_cut_test()

