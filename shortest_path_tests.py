import ds.fibonacci_heap as fheap
import ds.binary_heap as bheap
import ds.quake_heap as qheap
import graph.graph as graph
import random

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
  p = {} #Optimal path
  # Initialize distances to Infinity
  for v in G.V:
    if v == s: 
      d[v] = 0
      p[s] = s
    else:
      d[v] = float('inf')
      p[v] = None 
  labelled = make_heap(heap_type)
  nodes = {}
  for v in G.V:
    nodes[v] = labelled.make_node(d[v])
  labelled.insert(nodes[s])
  while len(scanned) < n:    
    min_node = labelled.delete_min()
    if min_node is None:

      return d, 'Unreachable'  
    for vertex in nodes:
      if nodes[vertex] == min_node:
        u = vertex
        break
    for w in G.adj[u]:      
      if w not in scanned:
        e = (u,w)
        if d[u] + G.W[e] < d[w]:
          d[w] = d[u] + G.W[e]
          p[w] = u
          # Check to see if previously inserted
          if nodes[w].value != float('inf'):
            labelled.decrease_key(nodes[w], d[w])
          else:
            nodes[w].value = d[w]
            labelled.insert(nodes[w])
    scanned.append(u)
  path = [t]
  node = t

  while node != s:
     node = p[node]
     path.append(node)
  path.reverse()
  return d, path
  
def test_a():
  """
  Quick sanity checks
  G =
      2 - 5 - 9
    / | \ |   |
  1 - 3 - 6 - 8
    \ | / | /
      4 - 7
  Weights are randomly generated (0,1)
  """
  V = [1, 2, 3, 4, 5, 6, 7, 8, 9]
  E = [(1,2), (1,3), (1,4), 
       (2,3), (2,5), (2,6),
       (3,6), (3,4),
       (4,7), (4,6),
       (5,9), (6,8), (7,8), (8,9)]
  W = {}
  for e in E:
    W[e] = random.random()

  G = graph.Graph(V, E, W)
  s = 1
  t = 9
  b_dist, b_path = dijkstra(G, s, t, BINARY_HEAP)
  f_dist, f_path = dijkstra(G, s, t, FIBONACCI_HEAP)
  q_dist, q_path = dijkstra(G, s, t, QUAKE_HEAP)
  print 'Binary Heap Solution: %f' % (b_dist[t])
  print 'Binary Heap Path: ',
  print b_path 
  print 'Fibonacci Heap Solution: %f' % (f_dist[t])
  print 'Fibonacci Heap Path: ',
  print f_path
  print 'Quake Heap Solution: %f' % (q_dist[t])
  print 'Quake Heap Path: ',
  print q_path

def test(num_vertices, num_edges):
  V = range(num_vertices)
  E = []
  for i in range(num_edges):
    u = random.randint(0,num_vertices-1)
    rest = range(0,u) + range(u+1,num_vertices)
    v = random.choice(rest)
    E.append((u,v))
  W = {}
  for e in E:
    W[e] = random.random()
  G = graph.Graph(V,E,W, True)
  s = random.choice(V)
  t = random.choice(V)
  
  print 's = %d, t = %d' % (s,t)

  b_dist, b_path = dijkstra(G, s, t, BINARY_HEAP)
  print 'Binary Heap Solution: %f' % (b_dist[t])
  print 'Binary Heap Path: ',
  print b_path 

  f_dist, f_path = dijkstra(G, s, t, FIBONACCI_HEAP)
  print 'Fibonacci Heap Solution: %f' % (f_dist[t])
  print 'Fibonacci Heap Path: ',
  print f_path

  q_dist, q_path = dijkstra(G, s, t, QUAKE_HEAP)
  print 'Quake Heap Solution: %f' % (q_dist[t])
  print 'Quake Heap Path: ',
  print q_path

if __name__ == '__main__':
  print "Test #1: |V| = 100, |E| = 1000"
  test(100,1000)

  print "Test #2: |V| = 300, |E| = 3000"
  test(300,50000)

