import ds.fibonacci_heap as fheap
import ds.binary_heap as bheap
import ds.quake_heap as qheap
import graph.graph as graph
from random import random

BINARY_HEAP = 1
FIBONACCI_HEAP = 2
QUAKE_HEAP = 3

def make_heap(heap_type):
  if heap_type == BINARY_HEAP:
    return bheap.BinaryHeap()
  elif heap_type == FIBONACCI_HEAP:
    return fheap.FibonacciHeap()
  elif heap_type == QUAKE_HEAP:
    return qheap.QuakeHeap()
  else:
    print 'Heap type not supported'

def dijkstra(G, s, t, heap_type):
  """
  Single source shortest path algorithm from s to t
  """
  n = len(G.V)
  d = {} #temporary distance function
  scanned = []
  # Initialize distances to Infinity
  for v in G.V:
    if v == s: 
      d[v] = 0
    else:
      d[v] = float('inf')
  labelled = make_heap(heap_type)
  nodes = {}
  for v in G.V:
    nodes[v] = labelled.make_node(d[v])
  labelled.insert(nodes[s])
  while len(scanned) < n:
    min_node = labelled.delete_min() 
    assert(min_node is not None)
    u = None
    for vertex in nodes:
      if nodes[vertex] == min_node:
        u = vertex
        break
    for v in G.adj[u]:
      e = (u,v)
      if d[u] + G.W[e] < d[v]:
        d[v] = d[u] + G.W[e]
        if nodes[v].value != float('inf') :
          labelled.decrease_key(nodes[v], d[v])
        else:
          nodes[v].value = d[v]
          labelled.insert(nodes[v])

    scanned.append(u)
  return d[t]

def test_a():
  """
  Quick sanity checks
  G =
      2 - 5 - 9
    / | \ |   |
  1 - 3 - 6 - 8
    \ | / | /
      4 - 7
  Weights are randomly generated
  """
  V = [1, 2, 3, 4, 5, 6, 7, 8, 9]
  E = [(1,2), (1,3), (1,4), 
       (2,3), (2,5), (2,6),
       (3,6), (3,4),
       (4,7), (4,6),
       (5,9), (6,8), (7,8), (8,9)]
  W = {}
  for e in E:
    W[e] = random()

  G = graph.Graph(V, E, W)
  s = 1
  t = 9
  #b_dist = dijkstra(G, s, t, BINARY_HEAP)
  f_dist = dijkstra(G, s, t, FIBONACCI_HEAP)
  #q_dist = dijkstra(G, s, t, QUAKE_HEAP)
  #print 'Binary Heap Solution: %f' % (b_dist)
  print 'Fibonacci Heap Solution: %f' % (f_dist)
  #print 'Quake Heap Solution: %f' % (q_dist)

def test():
  V = [1,2,3]
  E = [(1,2)]
  W = {}
  W[(1,2)] = 2

  f = fheap.FibonacciHeap()
  G = graph.Graph(V, E, W)
if __name__ == '__main__': test_a()
