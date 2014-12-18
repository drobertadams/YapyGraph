import copy
import logging
import pickle
import sys

from Vertex import Vertex

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

class Graph(object):
    """
    Represents a directional graph of Vertex objects. The graph can search for
    matching subgraphs. Vertex degree is maintained as the sum of indegree and
    outdegree.

    TODO: Tests/refactoring for...
    Graph.search(subGraph)
    """

    #--------------------------------------------------------------------------
    def __init__(self):
        """
        Builds an empty graph.
        """
        # A dictionary (key is vertex id) of Vertex objects.
        self._vertices = {}

        # A dictionary (key is vertex id) of a list of edges to Vertex objects.
        self._edges = {}

        # A dictionary (key is vertex id) of a list of neighbor Vertex objects.
        # This is different than _edges in that neighbors stores all adjancent
        # vertices, regardless of edge direction.
        self._neighbors = {}

        # A list of solutions as used by the seach() method. Since that method
        # is recursive, we need a single spot to store all the solutions found.
        self._solutions = []

        # A stack of match dictionaries as used by _updateState().
        self._matchHistory = []

    #--------------------------------------------------------------------------
    def addEdge(self, n, m):
        """
        Adds a directional edge from Vertex n to Vertex m. If 
        neither vertex exist in the graph, they are added. 
        Inputs: n, m - endpoints of the edge; can be either new Vertex 
            objects or the id of existing vertices.
        Outputs: none
        """
        if isinstance(n, str): # n is vid
            n = self._vertices[n]
        else: # n is Vertex
            self.addVertex(n)

        if isinstance(m, str): # m is vid
            m = self._vertices[m]
        else: # m is Vertex
            self.addVertex(m)

        self._edges[n.id].append(m)
        self._neighbors[n.id].append(m)
        self._neighbors[m.id].append(n)

        n.degree = n.degree + 1
        m.degree = m.degree + 1

    #--------------------------------------------------------------------------
    def addVertex(self, vertex):
        """
        Adds a new vertex to the graph. If a vertex with the same id
        already exists, the new vertex is not added. Instead, a reference
        to the existing vertex is returned.
        Inputs: vertex - Vertex object to add
        Outputs: The Vertex that was just added, or the existing Vertex if
        one already exists with the same id.
        """
        if vertex.id not in self._vertices:
            self._vertices[vertex.id] = vertex
            self._edges[vertex.id] = []
            self._neighbors[vertex.id] = []
        else:
            vertex = self._vertices[vertex.id]

        return vertex

    #--------------------------------------------------------------------------
    def deleteEdge(self, startVID, endVID):
        """
        Removes the edge from between the given Vertices. 
        Inputs: startVID, endVID - vertex IDs
        Outputs: False if the edge doesn't exist, True otherwise
        """
        if startVID not in self._vertices or \
            endVID not in self._vertices:
            return False

        startVertex = self._vertices[startVID]
        endVertex = self._vertices[endVID]

        if endVertex not in self._edges[startVID]:
            # startVID does not point to endVID.
            return False

        self._edges[startVID].remove(endVertex)

        self._neighbors[startVID].remove(endVertex)
        self._neighbors[endVID].remove(startVertex)

        startVertex.degree = startVertex.degree - 1
        endVertex.degree = endVertex.degree - 1

        return True

    #--------------------------------------------------------------------------
    def deleteVertex(self, vid):
        """
        Deletes the vertex with the given vid along with all edges to and 
        from it.
        Inputs: vertex ID (string) 
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

        # Delete the vertex itself.
        return self._vertices.pop(vid)

    #--------------------------------------------------------------------------
    @property
    def edges(self):
        """
        Iterator that returns all (Vertex,Vertex) tuples from this graph.
        """
        for startVID in self._edges:
            for endVertex in self._edges[startVID]:
                startVertex = self._vertices[startVID]
                yield ( startVertex, endVertex )

    #--------------------------------------------------------------------------
    def findVertexWithLabel(self, label):
        """
        Returns the first Vertex in this graph that has the given label.
        Inputs: string label
        Outputs: Vertex or None
        """
        for vertex in self.vertices:
            if vertex.label == label:
                return vertex
        return None

    #--------------------------------------------------------------------------
    def hasEdgeBetweenLabels(self, startLabel, endLabel):
        """
        Returns whether or not an edge exists from a vertex with label 
        startLabel to a vertex with label endLabel.
        Inputs: startLabel, endLabel - string vertex labels
        Outputs: True if edge exists, False otherwise
        """
        startVertex = self.findVertexWithLabel(startLabel)
        endVertex = self.findVertexWithLabel(endLabel)
        if startVertex is None or endVertex is None:
            return False
        return self.hasEdgeBetweenVertices(startVertex.id, endVertex.id)

    #--------------------------------------------------------------------------
    def hasEdgeBetweenVertices(self, startVID, endVID):
        """
        Checks to see if an edge exists between the given start and end vid.
        Inputs: startVID, endVID - vertex ids
        Outputs: True if an edge exists, False otherwise
        """
        if startVID not in self._vertices or endVID not in self._vertices:
            return False
        endVertex = self._vertices[endVID]
        return endVertex in self._edges[startVID]

    #--------------------------------------------------------------------------
    @property
    def labels(self):
        """
        Returns a list of all the labels in this graph (there may be 
        duplicates).
        Outputs: list of label strings
        """
        return [ v.label for v in self.vertices ]
    
    #--------------------------------------------------------------------------
    @property
    def numVertices(self):
        """
        Returns the number of vertices in this graph.
        """
        return len(self.vertices)

    #--------------------------------------------------------------------------
    @property
    def vertices(self):
        """
        Returns a list of Vertex objects in this graph.
        """
        return self._vertices.values()
    
    #--------------------------------------------------------------------------
    def search(self, q):
        """
        Search for every instance of q in self. Based on _An In-depth 
        Comparison of Subgraph Isomorphism Algorithms in Graph Databases_, 
        Lee et al., 2013.
        Inputs: q - Graph to search for.
        Outputs: a list of solutions (list of "matches"). matches is a
        list of [Vertex.id, Vertex.id] mappings.
        """
        #logging.debug('self has %d vertices' % self.numVertices)
        logging.debug(">>> Searching for %s in %s" % (q, self))

        # matches is a dict of vid(query)->vid(data) mappings of which query
        # vertex is matched to which data graph vertex. 
        matches = {}

        # Find candidates for each query vertex. Only search for subgraphs
        # if all query vertices have at least one data vertex candidate.
        if self._findCandidates(q):
            self._subgraphSearch(matches, q)

        return self.solutions

    #--------------------------------------------------------------------------
    def _filterCandidates(self, u):
        """
        Returns a list of data(self) Vertices that have the same label as query
        Vertex u. 
        Input: Query Vertex u.
        Output: list of Vertices from self.
        """
        candidates = []
        for vertex in self.vertices:
            if vertex.label == u.label:
                candidates.append(vertex)
        return candidates

    #--------------------------------------------------------------------------
    def _findCandidates(self, q):
        """
        For each query vertex, create a list of possible data vertices.
        Candidate vertices are stored in each vertex in a `candidates`
        item.
        Input: query graph q
        Output: True if all query vertices have at least one candidate, 
        False otherwise.
        """
        if self.numVertices == 0 or q.numVertices == 0:
            return False

        for u in q.vertices:
           u.candidates = self._filterCandidates(u)
           if len(u.candidates) == 0:
              return False
        return True

    #--------------------------------------------------------------------------
    def _findMatchedNeighbors(self, u, matches):
            # Find the matched vertices adjacent to query vertex u. This method
            # should be called on the query graph.
            # Input: Vertex u, dict of matches
            # Output: List of neighbors of u that appear in matches.
            if u is None or matches is None or len(matches) == 0:
                    return []

            neighbors = []
            # logging.debug('%s has neighbors %s' % (u, str(self._neighbors[u.id])))
            for neighborVertex in self._neighbors[u.id]:
                    if neighborVertex.id in matches:
                            neighbors.append(neighborVertex)
            return neighbors

    #--------------------------------------------------------------------------
    def _isJoinable(self, u, v, q, matches):		
            """
            See if u and v are joinable this data graph. 
            Iterates through all adjacent matched query vertices of u. 
            If an adjacent query vertex, n, is already matched with a data 
            vertex, w, then it checks whether there is a corresponding edge 
            (v, w) in this data graph going in the same direction as the edge
            between (u, n).
            Inputs: 
                    * query vertex u
                    * data vertex v
                    * query graph q, 
                    * list of matched query/data vertices
            Outputs: True if u and v can be matched, False otherwise
            """

            if u is None or v is None or q is None:
                    return False

            if len(matches) == 0:
                    return True

            neighbors = q._findMatchedNeighbors(u, matches)
            for n in neighbors:
                    w = self.vertices[matches[n.id]]
                    if u.id in q._edges and n in q._edges[u.id] and w in self._edges[v.id]:
                            return True
                    elif u in q._edges[n.id] and v in self._edges[w.id]:
                            return True
                    else:
                            return False

            return False

    #--------------------------------------------------------------------------
    def _nextUnmatchedVertex(self, matches):
        """
        Returns a vertex whose vid does not appear in matches.
        Input: dictionary of matches
        Output: The next unmatched Vertex, or None.
        """
        for vertex in self.vertices:
            if vertex.id not in matches:
                return vertex
        return None

    #--------------------------------------------------------------------------
    def _refineCandidates(self, candidates, u, matches):
            # Given a query vertex u, removes candidate vertices from the original
            # candidate list (candidates) created by _filterCandidates() that are no longer 
            # obvious matches because they have a degree smaller than u. It also
            # removes vertices that have already been matched.
            # Input: list of candidate graph vertices candidates, a query vertex
            # u, and the mapping of already mapped vertices.
            # Output: the revised list of candidate vertices.
            candidates = [v for v in candidates if (v.degree >= u.degree) and 
                    (v.id not in matches)]
            return candidates

    #--------------------------------------------------------------------------
    def _restoreState(self, matches):
            # Input: dict matches.
            # Output: Updated matches without the last set of matches.
            # Undoes the last vertex mapping by removing the last mapping pair
            # _(u, v)_ from _matches_.
            return pickle.loads(self.matchHistory.pop())

    #--------------------------------------------------------------------------
    def __repr__(self):
        if len(self._vertices) == 1:
            for vertexID,vertex in self._vertices.items():
                return str(vertex)
        else:
            # With multiple vertices, print an adjacency list.
            s = ''
            for vertexID,neighbors in self._edges.items():
                for neighbor in neighbors:
                    s += '%s->%s, ' % (self._vertices[vertexID], neighbor)
            return s

    #--------------------------------------------------------------------------
    def _subgraphSearch(self, matches, q):
        """
        Searches for all instances of q in self. Solutions are stored in
        self._solutions.
        Inputs: 
            * matches - dictionary of vertex mappings
            * q - query Graph
        Outputs: nothing
        """
        # If every query vertex has been matched, then we're done. Store the
        # solution we found and return. 
        if len(matches) == len(q.vertices):
            logging.debug('found a solution %s' % matches)
            self._solutions.append(copy.deepcopy(matches))
            return 
        
        # Get the next query vertex that needs a match.
        u = q._nextUnmatchedVertex(matches)

        # Test the degenerate case...there are no query vertices that need a match.
        if u is None:
            return

        logging.debug('checking for a match with data vertex %s' % u)

        # Refine the list of candidate vertices from that obviously aren't
        # good candidates.
        u.candidates = self._refineCandidates(u.candidates, u, matches)

        # Check each candidate for a possible match.
        for v in u.candidates:

                logging.debug('checking query vertex candidate %s' % v)

                # Check to see _u_ and _v_ are joinable in _g_.
                if self._isJoinable(u, v, q, matches):

                        logging.debug("oh yea, that's a match")

                        # Yes they are, so store the mapping and try the next vertex.
                        self._updateState(u, v, matches)
                        logging.debug('matches is now %s' % matches)
                        self._subgraphSearch(matches, q)

                        # Undo the last mapping.
                        matches = self._restoreState(matches)

    #--------------------------------------------------------------------------
    def _updateState(self, u, v, matches):
            """
            Stores the current mapping of Vertex u to Vertex v.
            Each call to _updateState() stores the previous set of matches to
            a stack of matches, so that _restoreState() can undo it.
            Inputs: 
                    * u - query Vertex
                    * v - data Vertex
                    * matches - dictionary of Vertex.id -> Vertex.id mappings 
            Outputs: nothing
            """

            self.matchHistory.append(pickle.dumps(matches))
            matches[u.id] = v.id
            #matches[v.id] = u.id
