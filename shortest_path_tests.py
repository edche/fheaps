import ds.fibonacci_heap as fheap
#import ds.binary_heap as bheap
import ds.dheap as dheap
import ds.quake_heap as qheap
import ds.thin_heap as theap
import ds.fat_heap as fatheap
import graph.graph as graph
import random
import datetime
from operator import add
from argparse import ArgumentParser

BINARY_HEAP = 0
FIBONACCI_HEAP = 1
QUAKE_HEAP = 2
FOUR_ARY_HEAP = 3
EIGHT_ARY_HEAP = 4
SIXTEEN_ARY_HEAP = 5
THIN_HEAP = 6
FAT_HEAP = 7
heaps_to_test = [BINARY_HEAP, FIBONACCI_HEAP, QUAKE_HEAP, FOUR_ARY_HEAP, EIGHT_ARY_HEAP, SIXTEEN_ARY_HEAP, THIN_HEAP, FAT_HEAP]
heap_names = {BINARY_HEAP: 'Binary Heap', FIBONACCI_HEAP: 'Fibonacci Heap', QUAKE_HEAP: 'Quake Heap', FOUR_ARY_HEAP: '4-ary Heap',
    EIGHT_ARY_HEAP: '8-ary Heap', SIXTEEN_ARY_HEAP: '16-ary Heap', THIN_HEAP: 'Thin Heap', FAT_HEAP: 'Fat Heap'}

def make_heap(heap_type):
  if heap_type == BINARY_HEAP:
    return dheap.DHeap(2)
  elif heap_type == FIBONACCI_HEAP:
    return fheap.FibonacciHeap()
  elif heap_type == QUAKE_HEAP:
    return qheap.QuakeHeap()
  elif heap_type == FOUR_ARY_HEAP:
    return dheap.DHeap(4)
  elif heap_type == EIGHT_ARY_HEAP:
    return dheap.DHeap(8)
  elif heap_type == SIXTEEN_ARY_HEAP:
    return dheap.DHeap(16)
  elif heap_type == THIN_HEAP:
    return theap.ThinHeap()
  elif  heap_type == FAT_HEAP:
    return fatheap.FatHeap()
  else:
    print 'Heap type not supported'

def dijkstra(G, s, t, heap_type):
  """
  Single source shortest path algorithm from s to t
  """
  n = len(G.V)
  d = {} #temporary distance function
  scanned = set()
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
      break
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
    scanned.add(u)
  path = [t]
  node = t

  while node and node != s:
     node = p[node]
     path.append(node)
  path.reverse()
  return d, path
  

def test(num_vertices, num_edges, heaps_to_test, verbose):
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
  
  result = "PASSED"
  if verbose:
    print 's = %d, t = %d' % (s,t)

  num_heaps = len(heaps_to_test)
  dists = [None] * num_heaps
  paths = [None] * num_heaps
  times = [None] * num_heaps
  for i in range(num_heaps):
    dist, path, time = run_test(G,s,t,heaps_to_test[i])
    dists[i] = dist
    paths[i] = path
    times[i] = time
    '''
  if not all(dists[0] == dist for dist in dists):
    result = "FAILED"
    print dists
    '''
  if not all(paths[0] == path for path in paths):
    result = "FAILED"
    print paths
  return times, result

def run_test(G, s, t, heap_type):
  start = datetime.datetime.now()
  dist, path = dijkstra(G,s,t, heap_type)
  end = datetime.datetime.now()
  time = (end - start).total_seconds()
  return dist, path, time

if __name__ == '__main__':
  parser = ArgumentParser()
  parser.add_argument('-V', type=int, help='number of vertices')
  parser.add_argument('-E', type=int, help='number of edges')
  parser.add_argument('-q', action='store_true', default=True, help='quiet mode')
  parser.add_argument('-t', type=int, help='number of trials')
  args = parser.parse_args()

  verbose = args.q
  num_vert = args.V
  num_edges = args.E
  num_trials = args.t
  average_time = [0]*len(heaps_to_test)
  print 'Graph Description: |V| = %d, |E| = %d' % (num_vert, num_edges)

  for i in range(num_trials):
    try:
      times, result = test(num_vert,num_edges, heaps_to_test, verbose)
      print "Trial #%d: " % (i)
      print result
      print times
      average_time = map(add, average_time, times)
    except Exception as error:
      print error

  for i in range(len(heaps_to_test)):
    average_time[i] /= num_trials
  print 'Average Times for |V| = %d and |E| = %d:' % (num_vert, num_edges)
  for i in range(len(heaps_to_test)):
    print heap_names[heaps_to_test[i]] + ': %f' % (times[i])
