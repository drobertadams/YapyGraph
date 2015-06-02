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
        Removes the edge from between the given vertices. 
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
        Inputs: vertex ID
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

        # Remove vid from list of edges.
        self._edges.pop(vid)

        # Remove the vertex from any neighbor lists.
        for id in self._neighbors:
            if id in self._neighbors[id]: self._neighbors[id].remove(vid)
        self._neighbors.pop(vid)

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
    def findVertex(self, name):
        """
        Returns the first Vertex in this graph that has the given name, 
        or None.
        """
        for vertex in self.vertices:
            if vertex.name == name:
                return vertex
        return None

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
    def names(self):
        """
        Returns a list of all the vertex "names" in this graph (there may be 
        duplicates).
        Outputs: list of name strings
        """
        return [ v.name for v in self.vertices ]

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
        Search for every instance of Graph q in self. Based on _An In-depth 
        Comparison of Subgraph Isomorphism Algorithms in Graph Databases_, 
        Lee et al., 2013.
        Inputs: q - Graph to search for.
        Outputs: a list of solutions. Each solution is a dictionary
        of vid/vid mappings from query vertex to data graph vertex. Only the
        vertex label is used to find matches (not the vertex number).
        """
        logging.debug("In Graph.search")
        logging.debug("Searching for %s in %s" % (q, self))

        # matches is a dict of vid(query)->vid(data) mappings of which query
        # vertex is matched to which data graph vertex. 
        matches = dict()

        # Find candidates for each query vertex. Only search for subgraphs
        # if all query vertices have at least one data vertex candidate.
        self._solutions = []
        if self._findCandidates(q):
            self._subgraphSearch(matches, q)

        logging.debug("Out Graph.search")
        return self._solutions

    #--------------------------------------------------------------------------
    # PRIVATE METHODS - These aren't the methods you're looking for.
    #--------------------------------------------------------------------------
    def _filterCandidates(self, u):
        """
        Returns a list of data Vertices that have the same label as query
        Vertex u. This method should be called on the data graph.
        Input: Query Vertex u.
        Output: list of Vertices from self.
        """
        return [vertex for vertex in self.vertices if vertex.label == u.label]
        
    #--------------------------------------------------------------------------
    def _findCandidates(self, q):
        """
        For each query vertex in q, create a list of possible data vertices.
        Candidate vertices are stored in each vertex in a `candidates`
        list. Candidates are those that have the same label as a data graph 
        vertex.
        Input: query graph q
        Output: True if all query vertices have at least one candidate, 
        False otherwise.
        Side Effects: query vertices may have their candidates property
        updated.
        """
        logging.debug("In _findCandidates")
        if self.numVertices == 0 or q.numVertices == 0:
            logging.debug("No candidates")
            return False

        for u in q.vertices:
            u.candidates = self._filterCandidates(u)
            if len(u.candidates) == 0:
                logging.debug("No candidates")
                return False
        
        cand_str = ""
        for i in u.candidates:
            cand_str += str(i) + " "
        logging.debug('Raw candidates for %s are %s' % (u, cand_str))
        return True

    #--------------------------------------------------------------------------
    def _findMatchedNeighbors(self, u, matches):
        """
        Find the matched vertices adjacent to query vertex u. This method
        should be called on the query graph. "neighbor" here is irregardless
        of edge direction. Two vertices are considered neighbors if any
        edge connects them.
        Input: query Vertex u, dict of matches
        Output: List of neighbors of u that appear in matches.
        """
        if u is None or matches is None or len(matches) == 0:
            return []

        return [neighborVertex for neighborVertex in self._neighbors[u.id] \
            if neighborVertex.id in matches]

    #--------------------------------------------------------------------------
    def _isJoinable(self, u, v, q, matches):		
        """
        See if query Vertex u and data Vertex v are "joinable" (matchable
        for a solution). Iterates through all matched query 
        vertices adjacent to u. If some adjacent query vertex, n, is already 
        matched with a data vertex, m, then it checks whether there is a 
        corresponding edge between v and m in the data graph going in 
        the same direction as the edge between u and n.
        Inputs: 
            * query Vertex u
            * data Vertex v
            * query Graph q, 
            * list of previously matched query/data vertices
        Outputs: True if u and v can be matched, False otherwise
        """

        # If nothing has been matched, then we can join u and v.
        if len(matches) == 0:
            return True

        neighbors = q._findMatchedNeighbors(u, matches)
        for n in neighbors:
            m = self._vertices[matches[n.id]]
            if q.hasEdgeBetweenVertices(u.id, n.id) and \
               self.hasEdgeBetweenVertices(v.id, m.id):
                return True
            elif q.hasEdgeBetweenVertices(n.id, u.id) and \
               self.hasEdgeBetweenVertices(m.id, v.id):
                return True
            else:
                return False

        return False

    #--------------------------------------------------------------------------
    def _nextUnmatchedVertex(self, matches):
        """
        Returns a query vertex whose vid does not appear in matches. This 
        should be called on the query graph.
        Input: dictionary of matches
        Output: The next unmatched Vertex, or None.
        """
        for vertex in self.vertices:
            if vertex.id not in matches:
                return vertex
        return None

    #--------------------------------------------------------------------------
    def _refineCandidates(self, candidates, u, matches):
        """
        Given a query vertex u, removes candidate data vertices from the
        original candidate list (candidates) created by _filterCandidates()
        that are no longer obvious matches because they have a degree smaller
        than u. It also removes vertices that have already been matched.
        Input: 
            * candidates - list of candidate data Vertices
            * u - query vertex for which candidates is a list
            * matches - data/query vertices dictionary already matched
        Output: the revised list of candidate vertices.
        """
        #candidates = [c for c in candidates if (c.degree >= u.degree) and 
        #        (c.id not in matches)]
        new_candidates = []
        for c in candidates:
            #logging.debug('checking candidate %s' % str(c))
            #logging.debug('matches is %s' % matches)
            #logging.debug('candidate degree is %d' % c.degree)
            if c.degree >= u.degree and c.id not in matches.values():
                new_candidates.append(c)
                #logging.debug('%s is a candidate' % c.id)
            #else:
                #logging.debug('u degree is %d and c degree is %d' % (u.degree, c.degree))
                #logging.debug('%s not in matches.values is %s' % (c.id, c.id not in matches.values()))
        return new_candidates

    #--------------------------------------------------------------------------
    def _restoreState(self, matches):
        """
        Undoes the last vertex match by removing the last matching dict
        from _matchHistory and returning it.
        Input: dict of previous matches (stored as JSON strings)
        Output: previous match dict.
        """
        return pickle.loads(self._matchHistory.pop())

    #--------------------------------------------------------------------------
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
                s += "%s_%s" % (vertex.name, vertex.id)
        else:
            for vertexID,neighbors in self._edges.items():
                for neighbor in neighbors:
                    s += '%s_%s->%s_%s;\n' % (self._vertices[vertexID].name, 
                        self._vertices[vertexID].id, neighbor.name, neighbor.id)
                    #s += '%s->%s;\n' % (self._vertices[vertexID].name, 
                    #    neighbor.name)

        s = s + "\n}"
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
        logging.debug("In _subgraphSearch")

        # If every query vertex has been matched, then we're done. Store the
        # solution we found and return. 
        if len(matches) == len(q.vertices):
            logging.debug('found a solution %s' % matches)
            self._solutions.append(copy.deepcopy(matches))
            return 
        
        # Get the next query vertex that needs a match.
        u = q._nextUnmatchedVertex(matches)
        logging.debug('Next unmatched vertex is %s' % u)
        cand_str = ""
        for i in u.candidates:
            cand_str += str(i) + " "
        logging.debug('Raw candidates of %s are [%s]' % (u,cand_str))

        # Save the current candidates of u so we can restore them after we
        # try all existing mappings.
        old_candidates = u.candidates

        # Refine the list of candidate vertices from those obviously aren't
        # good candidates.
        u.candidates = self._refineCandidates(u.candidates, u, matches)
        cand_str = ""
        for i in u.candidates:
            cand_str += str(i) + " "
        logging.debug('Refined candidates are [%s]' % cand_str)

        # Check each candidate for a possible match.
        for v in u.candidates:
            logging.debug('Checking candidate %s for vertex %s' % (v,u))
            # Check to see u and v are joinable in self.
            if self._isJoinable(u, v, q, matches):
                logging.debug("%s is joinable to %s" % (v, u))

                # Yes they are, so store the mapping and try the next vertex.
                self._updateState(u, v, matches)
                logging.debug('Matches is now %s' % matches)
                self._subgraphSearch(matches, q)

                # Undo the last mapping.
                matches = self._restoreState(matches)

        # _refineCandidates() may have removed vertices. Restore them before
        # trying another solution (returning from this recursive call).
        u.candidates = old_candidates
        logging.debug("Out _subgraphSearch")


    #--------------------------------------------------------------------------
    def _updateState(self, u, v, matches):
        """
        Stores the current match of query Vertex u to data Vertex v as a
        possible solution. Each call to _updateState() also stores the previous
        set of matches to a stack of matches, so that _restoreState() can undo
        it.
        Inputs: 
            * u - query Vertex
            * v - data Vertex
            * matches - current matches
        Outputs: nothing
        """
        # Store the previous set of matches as a JSON string.
        self._matchHistory.append(pickle.dumps(matches))
        matches[u.id] = v.id
