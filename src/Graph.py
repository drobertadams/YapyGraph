import copy
import logging
import pickle
import sys

from YapyGraph.src.Vertex import Vertex

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

class Graph(object):
    """
    Represents a directed graph of Vertex objects. The graph can search for
    matching subgraphs. Vertex degree is maintained as the sum of in-degree and
    out-degree.
    """

    # =========================================================================
    def __init__(self):
        """
        Builds an empty graph.
        """
        # The vertices in this graph. Stored as a dictionary using vertex id as 
        # the key, and a Vertex object as he value.
        self._vertices = {}

        # The directed edges in this graph. Stored as a dictionary using vertex id as
        # the key (starting end of the edge), and another vertex id as the value
        # representing the other endpoint of the edge. Edges are directional
        # running from key id to value id.
        self._edges = {}

        # All the neighbors in this graph, regardless of direction. key and value
        # are both vertex id. If v1 -> v2, then this dictionary stores two entries:
        # v1 -> v2 and v2 -> v1.
        #self._neighbors = {}

        # A stack of match dictionaries as used by _updateState().
        # self._matchHistory = []

    # =========================================================================
    def addEdge(self, u:str or Vertex, v:str or Vertex, bi:bool=False) -> None:
        """
        Adds a directed edge from u to v. If u or v are strings, they are vertex
        id's of existing vertices. If either doesn't exist, this method raises
        an exception. u and v can also be Vertex objects, in which case they
        are added as new vertices to the graph.

        Inputs: 
            u,v - endpoints of the edge; can be either new Vertex objects or 
                  the ids of existing vertices.
            bi - is this edge bidirectional? If so, two edges will be added
        """
        if isinstance(u, str): # u is string vertex id, find it
            u = self._vertices[u]
            if u is None:
                raise Exception("Vertex %s does not exist." % u) 
        else: # u is a new Vertex, add it
            self.addVertex(u)

        if isinstance(v, str): # v is vid, find it
            v = self._vertices[v]
            if v is None:
                raise Exception("Vertex %s does not exist." % v) 
                return
        else: # v is a new Vertex, add it
            self.addVertex(v)

        # Update edges if they don't already exist.
        if v not in self._edges[u.id]:
            self._edges[u.id].append(v)     # add an edge from u to v
            u.degree += 1
            v.degree += 1
            # Update neighbors
            # self._neighbors[u.id].append(v)     # m is a neighbor of n
            # self._neighbors[v.id].append(u)     # n is a neighbor or m

        if bi and u not in self._edges[v.id]:
            self._edges[v.id].append(u)     # add an edge from v to u 
            u.degree += 1
            v.degree += 1     

    # =========================================================================
    def addVertex(self, v:Vertex) -> Vertex:
        """
        Adds a new vertex to the graph. If a vertex with the same id
        already exists, the new vertex is not added. Instead, a reference
        to the existing vertex is returned.

        Inputs: v - Vertex to add
        Outputs: The Vertex that was just added, or the existing Vertex if
        one already exists with the same id.
        """
        if v.id not in self._vertices:
            self._vertices[v.id] = v
            self._edges[v.id] = []  # no edges yet
           # self._neighbors[v.id] = []
        else:
            v = self._vertices[v.id]

        return v

    # =========================================================================
    def deleteEdge(self, sid:str, eid:str) -> bool:
        """
        Removes the edge from between the given vertices. This is a one-way removal.

        Inputs: 
            sid, eid - start and end vertex IDs
        Outputs: False if the edge doesn't exist, True otherwise
        """
        # sid and eid must be valid vertices.
        if sid not in self._vertices or \
            eid not in self._vertices:
            return False

        # Get the vertices.
        startVertex = self._vertices[sid]
        endVertex = self._vertices[eid]

        # If sid does not point to eid, return False.
        if endVertex not in self._edges[sid]:
            return False

        # Remove the edge.
        self._edges[sid].remove(endVertex)

        # Update neighbors if we've just removed the only edge
        # between u1 and u2.
        # if startVID not in self._edges[endVID]:
        #     self._neighbors[startVID].remove(endVertex)
        #     self._neighbors[endVID].remove(startVertex)

        # Update vertex degrees.
        startVertex.degree -= 1
        endVertex.degree   -= 1

        return True

    # =========================================================================
    def deleteVertex(self, vid:str) -> Vertex:
        """
        Deletes the vertex with the given vid along with all edges to and 
        from it.

        Inputs: vid - vertex ID to delete
        Outputs: Vertex that was deleted, or None
        """
        if vid not in self._vertices:
            return None

        # Remove any edges leading out of vid.
        for endVertex in self._edges[vid]:
            self.deleteEdge(vid, endVertex.id)

        # Remove any edges leading to vid.
        for startVID in self._vertices:
            self.deleteEdge(startVID, vid)

        # Remove vid as a key in the list of edges.
        self._edges.pop(vid)

        # Remove vid from any neighbor lists, and from the list itself.
        # for id in self._neighbors:
        #     if id in self._neighbors[id]: self._neighbors[id].remove(vid)
        # self._neighbors.pop(vid)

        # Delete the vertex itself.
        return self._vertices.pop(vid)

    # =========================================================================
    def edges(self):
        """
        Iterator that returns all (Vertex,Vertex) tuples in this graph.
        """
        for startVID in self._edges:
            for endVertex in self._edges[startVID]:
                startVertex = self._vertices[startVID]
                yield ( startVertex, endVertex )

    # =========================================================================
    def hasEdge(self, startVID:str, endVID:str) -> bool:
        """
        Checks to see if an edge exists between the given start and end vid.
        Inputs: startVID, endVID - vertex ids
        Outputs: True if an edge exists, False otherwise
        """
        if startVID not in self._vertices or endVID not in self._vertices:
            return False
        endVertex = self._vertices[endVID]
        return endVertex in self._edges[startVID]

    # =========================================================================
    def getVertex(self, name:str) -> Vertex:
        """
        Returns the first Vertex in this graph that has the given name, 
        or None.
        """
        for v in self._vertices.values():
            if v.name() == name:
                return v
        return None
    
    # =========================================================================
    def numVertices(self):
        """
        Returns the number of vertices in this graph.
        """
        return len(self._vertices)
    
    # =========================================================================
    def __repr__(self):
        """Outputs this graph in dot notation. See 
        http://www.graphviz.org/content/dot-language. Sample output:

            digraph {
              A->B->C;
              B->D;
            }

        """
        s = "digraph {\n"

        if len(self._vertices) == 1:
            # Only one vertex. Print it's name.
            for vertexID,vertex in self._vertices.items():
                s += str(vertex)
        else:
            for vertexID,neighbors in self._edges.items():
                for neighbor in neighbors:
                    s += "%s->%s;\n" % ( str(self._vertices[vertexID]), str(neighbor) )

        s += "\n}"
        return s

    # -------------------------------------------------------------------------
    def search(self, q) -> list:
        """
        Search for every instance of Graph q in self. Based on Ullman's
        search algorithm as described in _An In-depth Comparison of Subgraph 
        Isomorphism Algorithms in Graph Databases_, Lee et al., 2013.
        NB: Only the vertex labels are used to find matches.

        https://dl.acm.org/doi/pdf/10.14778/2535568.2448946
        https://dl-acm-org.ezproxy.gvsu.edu/doi/pdf/10.14778/2535568.2448946

        Inputs: query Graph q

        Output: all subgraph isomorphisms of q in g, in the form of vid->vid
        mappings from q to g.
        """
        # A list of all isomorphism solutions.
        solutions = []

        # 1: M := ∅;
        # M is a dict of vid(q)->vid(g) mappings for a single isomorphism. Once
        # one is found, it will be appended to `solutions`.
        M = dict()

        # C is a list of candidates for each query vertex u.
        C = self._findCandidates(q) 
        if len(C) != q.numVertices() or len(C) == 0:
            # If we didn't find candidates for all u's, return no solutions.
            return solutions
        
        # 8: SubgraphSearch (q, g, M, ...);
        self._subgraphSearch(q, M, C, solutions)

        return solutions

    # =========================================================================
    def vertices(self) -> list:
        """
        Returns a list of Vertex objects in this graph.
        """
        return self._vertices.values()
    
    # =========================================================================
    def _filterCandidates(self, u:Vertex) -> list:
        """
        Returns a list of data (g) vertices that have the same label as query
        vertex u and whose degree is >= u's degree.
        This method should be called on the data graph.

        Input: Query vertex u.
        Output: List of vertices v from self (g).
        """
        return [ v for v in self.vertices() if v.hasLabel(u.label) and v.degree >= u.degree ]
        
    # =========================================================================
    def _findCandidates(self, q) -> dict:
        """ 
        Returns a dictionary of candidate data vertices for each query vertex u,
        calling _filterCandidates() to do the heavy lifting. The resulting 
        dictionary has key u.id and value is a list of v.id's.
        
        Input: query graph q
        """
        C = dict()

        # 2: for each u ∈ V(q) do
        for u in q.vertices():

            # 3: C(u) := FilterCandidates (q, g, u, . . .);
            #    [[ ∀v ∈ C(u)((v ∈ V(g)) ∧ (L(u) ⊆ L(v))) ]]
            c_u = self._filterCandidates(u)

            # 4: if C(u) = ∅ then
            if len(c_u) == 0:
                # There are no appropriate candidates, return an empty dictionary.
                return dict()
            else:
                # Add the candidates for u to the dictionary.
                C[u.id] = c_u

        return C

    # =========================================================================
    def _findMatchedNeighbors(self, u:Vertex, q, M:dict) -> list:
        """
        Returns a list of all neighbors of query vertex q that has already been
        matched in M.

        Inputs:
            u - query vertex that is basis for the search
            q - query graph
            M - current matches

        Output: List of neighbors of u that have been matched.
        """
        if u is None:
            return []
        
        return [n for n in q._edges[u.id] if q._isMatched(n, M)]

    # =========================================================================
    def _isJoinable(self, u:Vertex, v:Vertex, q, M:dict) -> bool:	
        """
        Returns true if query vertex u and data Vertex v are "joinable" (matchable
        for a solution). 
        
        Iterates through all matched neighbors, n, of u. If n is matched to data
        vertex m, then we check to see if there is an edge from v to m in the data
        graph.

        8: [[ ∀(u', v' ∈ M((u, u') ∈ E(q) =⇒ (v, v') ∈ E(g) ∧ L(u, u') = L(v, v)) ]]

        Inputs: 
            u - query vertex
            v - data vertex
            q - query graph
            M - list of matched id's 
        Outputs: True if u and v can be matched, False otherwise
        """

        neighbors = q._findMatchedNeighbors(u, q, M)

        for n in neighbors:
            # Get matching data vertex for n.
            m = self._vertices[M[n.id]]

            # We know there's an edge from u to n, so make sure there's
            # an edge from v to m.
            if not self.hasEdge(v.id, m.id):
                return False

        return True
    
    # =========================================================================
    def _isMatched(self, u:Vertex, M:dict) -> bool:
        """
        Returns True if vertex u has already been matched in M, appearing on
        either side of the u->v mapping.
        """
        return u.id in M.keys() or u.id in M.values()

    # =========================================================================
    def _nextQueryVertex(self, q, M:dict) -> Vertex:
        """
        Returns a query vertex from `q` whose id does not appear in `M`.
        [[ u ∈ V(q) ∧ ∀(u', v) ∈ M(u' != u) ]]

        Inputs: q - the query graph
                M - the current mapping solution
        Output: The next unmatched Vertex, or None.
        """
        for vertex in q.vertices():
            if vertex.id not in M:
                return vertex
            
        return None

    #--------------------------------------------------------------------------
    def _subgraphSearch(self, q, M: dict, C: list, solutions:list):
        """
        Searches for all instances of q in self. Solutions are stored in
        `solutions`.

        Inputs:
            q - query Graph
            M - dictionary of vertex mappings
            C - candidate data vertices for each query vertex
            solutions - solution mappings found so far
        """

        # 1: if |M| = |V (q)| then
        # 2:    report M;
        # If every query vertex has been matched, then we're done. Store the
        # solution we found and return. 
        if len(M) == q.numVertices():
            solutions.append(copy.deepcopy(M))

        else:
            # 4: u := NextQueryVertex (...);
            # [[ u ∈ V(q) ∧ ∀(u', v) ∈ M(u' != u) ]]
            # Get the next query vertex that needs a match.
            u = self._nextQueryVertex(q, M)

            # 6: for each v ∈ C(u) such that v is not yet matched do
            for v in [ c for c in C[u.id] if not self._isMatched(c, M) ]:
                # 7: if IsJoinable (q, g, M, u, v, . . .) then
                if self._isJoinable(u, v, q, M):
                    # 9: UpdateState (M, u, v, . . .);
                    # [[ (u, v) ∈ M ]]
                    M[u.id] = v.id
                
                    # 10: SubgraphSearch (q, g,M, ...);
                    self._subgraphSearch(q, M, C, solutions)

                    # 11: RestoreState (M, u, v, . . .);
                    # [[ (u, v) ∈/ M ]]
                    M.pop(u.id)
