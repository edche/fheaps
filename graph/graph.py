class Graph:
  def __init__(self, V, E, W = None, directed = False):
    """    
    V: a list of vertex labels 
    E: a list of tuples (x,y)
    W: weights for edges (dictionary)
    directed: directed graph or not
    adj: adjacency list ( dictionary)
    """
    self.V = V
    self.E = E
    self.W = W
    self.adj = {}

    for u in V:
      self.adj[u] = []

    for (u,v) in E:
      self.adj[u].append(v) 
      if not directed:
        self.adj[v].append(u)
        if (v,u) not in self.W:
          self.W[(v,u)] = self.W[(u,v)]
