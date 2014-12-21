import unittest

from PGC.Graph.Graph import Graph
from PGC.Graph.Vertex import Vertex

class TestGraphSearch(unittest.TestCase):
    """
    X _filterCandidates
    X _findCandidates
    X _nextUnmatchedVertex
    X _refineCandidates
    X _findMatchedNeighbors
    _isJoinable
    _updateState
    _restoreState
    _subgraphSearch
    search
    """

    def testFilterCandidates(self):
        # Filtering an empty graph should return an empty array.
        g = Graph()
        c = g._filterCandidates(None)
        self.assertEquals(len(c), 0)

        # Build a little graph with two 'A' labeled vertices.
        g.addEdge(Vertex('u1', 'A'), Vertex('u2', 'B'))
        g.addEdge('u1', Vertex('u3', 'A'))

        # Search the graph for all 'X' vertices (should return an empty array.)
        u = Vertex('x', 'X')
        c = g._filterCandidates(u)
        self.assertTrue(len(c) == 0)

        # Search for 'A' vertices. Should return two of them.
        u = Vertex('x', 'A')
        c = g._filterCandidates(u)
        self.assertTrue(len(c) == 2)
        self.assertTrue(c[0].label == 'A')
        self.assertTrue(c[1].label == 'A')

    def testFindCandidates(self):
        # Create empty data and query graphs.
        g = Graph()
        q = Graph()

        # Searching finds no candidates.
        self.assertFalse(g._findCandidates(q))

        # Add some data vertices.
        g.addEdge(Vertex('u1', 'A'), Vertex('u2', 'B'))

        # Empty query graph still finds no candidates.
        self.assertFalse(g._findCandidates(q))

        # Add some query vertices.
        q.addEdge(Vertex('u1', 'A'), Vertex('u2', 'B'))
        q.addEdge('u1', Vertex('u3', 'C'))

        # Data graph has no 'C', so still returns false.
        self.assertFalse(g._findCandidates(q))

        # Add a vertex for C, and now the test should succeeed.
        g.addEdge('u1', Vertex('u3', 'C'))
        self.assertTrue(g._findCandidates(q))
        
    def testFindMatchedNeighbors(self): 
        q = Graph()
        # No data should return an empty list.
        mn = q._findMatchedNeighbors(None, None)
        self.assertEquals(len(mn), 0)

        # No matching neighbors should return an empty list.
        q.addEdge(Vertex('u1', 'A'), Vertex('u2', 'B'))
        u2 = q._vertices['u2']
        mn = q._findMatchedNeighbors(u2, [])
        self.assertEquals(len(mn), 0)

        # Make a matching neighbor and make sure it is returned.
        matches = { 'u1':'v1', 'v1':'u1' }
        mn = q._findMatchedNeighbors(u2, matches)
        self.assertEquals(len(mn), 1)
        self.assertEquals(mn[0].id, 'u1')

    def testNextUnmamtchedVertex(self):
        matches = {}

        # Build a little graph with three nodes.
        q = Graph()
        q.addEdge(Vertex('u1'), Vertex('u2'))
        q.addEdge('u1', Vertex('u3'))

        # Call _nextUnmatchedVertex three times. Each time it returns a
        # vertex, add it to matches.
        for i in range(3):
            v = q._nextUnmatchedVertex(matches)
            self.assertTrue(v.id in ['u1', 'u2', 'u3'])
            matches[v.id] = 'XYZ'

        # Now that all of the vertices are labeled, _nextUnmatchedVertex() 
        # should return None.
        self.assertIsNone(q._nextUnmatchedVertex(matches))

    def testRefineCandidates(self):
        # An empty candidate list should return an empty list.
        g = Graph()
        c = g._refineCandidates([], None, {})
        self.assertEquals(len(c), 0)

        # Build a graph and some vertices for use later.
        u = Vertex('u1') # query vertex
        v = Vertex('v1') # data vertex

        # Test with unmatched candidate with the v.degree >= u.degree.
        u.degree = 1
        v.degree = 1
        c = [ v ]
        c = g._refineCandidates(c, u, {})
        self.assertEqual(len(c), 1)
        self.assertEqual(c[0].id, 'v1')

        # Test with matched candidate with v.degree >= u.degree.
        u.degree = 1
        v.degree = 1
        m = { 'v1', 'u1' }
        c = g._refineCandidates(c, u, m)
        self.assertEqual(len(c), 0)

        # Test with unmatched candidate with v.degree < u.degree.
        u.degree = 1
        v.degree = 0
        c = g._refineCandidates(c, u, {})
        self.assertEqual(len(c), 0)

        # Test with matched candidate with v.degree < u.degree.
        u.degree = 1
        v.degree = 0
        m = { 'v1', 'u1' }
        c = g._refineCandidates(c, u, m)
        self.assertEqual(len(c), 0)




    def XtestSearchEmptyQueryGraph(self):
            # Using an empty query graph should result in no solution.
            q = Graph()
            g = Graph()
            solutions = g.search(q)
            self.assertEquals(len(solutions), 0)

    def XtestSearchEmptyDataGraph(self):
            # Using an empty data graph should result in no solution.
            q = Graph()
            q.addEdge(Vertex('u1', 'A'), Vertex('u2', 'B'))
            q.addEdge('u1', Vertex('u3', 'C'))

            g = Graph()
            solutions = g.search(q)
            self.assertEquals(len(solutions), 0)

    def XtestOneSimpleSolution(self):
            q = Graph()
            q.addEdge(Vertex('u1', 'A'), Vertex('u2', 'B'))
            q.addEdge('u1', Vertex('u3', 'C'))

            # Create an exact replica of the query graph as the data graph. This
            # should result in a solution.
            g = Graph()
            g.addEdge(Vertex('v1', 'A'), Vertex('v2', 'B'))
            g.addEdge('v1', Vertex('v3', 'C'))

            solutions = g.search(q)

            self.assertEquals(len(solutions), 1)
            self.assertEquals(solutions[0]['u1'], 'v1')
            self.assertEquals(solutions[0]['u2'], 'v2')
            self.assertEquals(solutions[0]['u3'], 'v3')

    def XtestTwoSolutions(self):

            q = Graph()
            q.addEdge(Vertex('u1', 'A'), Vertex('u2', 'B'))
            q.addEdge('u1', Vertex('u3', 'C'))

            # Create an exact replica of the query graph as the data graph. Then
            # create another instance of the A->B,A->C query graph inside the
            # data graph. This should result in two solutions found.
            g = Graph()
            g.addEdge(Vertex('v1', 'A'), Vertex('v2', 'B'))
            g.addEdge('v1', Vertex('v3', 'C'))
            g.addEdge(Vertex('v4', 'A'), 'v3')
            g.addEdge('v4', Vertex('v5', 'B'))

            solutions = g.search(q)

            self.assertEquals(len(solutions), 2)
            self.assertEquals(solutions[1]['u1'], 'v4')
            self.assertEquals(solutions[1]['u2'], 'v5')
            self.assertEquals(solutions[1]['u3'], 'v3')

    def XtestThreeSolutions(self):

            q = Graph()
            q.addEdge(Vertex('u1', 'A'), Vertex('u2', 'B'))
            q.addEdge('u1', Vertex('u3', 'C'))

            # Create an exact replica of the query graph as the data graph. Then
            # create another instance of the A->B,A->C query graph inside the
            # data graph. Finally, connect v3(C) and v5(B) with a new v6(A). 
            # This should result in three solutions.
            g = Graph()
            g.addEdge(Vertex('v1', 'A'), Vertex('v2', 'B'))
            g.addEdge('v1', Vertex('v3', 'C'))
            g.addEdge(Vertex('v4', 'A'), 'v3')
            g.addEdge('v4', Vertex('v5', 'B'))
            g.addEdge(Vertex('v6', 'A'), 'v3')
            g.addEdge('v6', 'v5')

            solutions = g.search(q)

            self.assertEquals(len(solutions), 3)



    def XtestIsJoinable(self):
            # If u or v is None, then IsJoinable() should return False.
            g = Graph()
            self.assertFalse(g._isJoinable(None, None, None, None))

            # If there are no matched vertices yet (we just started the matching
            # process), then IsJoinable() should return True.
            g = Graph()
            q = Graph()
            u = Vertex('u1')
            v = Vertex('v1')
            self.assertTrue(g._isJoinable(u, v, q, []))

            # Create a query and data graph for some tests.
            q.addEdge(Vertex('u1', 'A'), Vertex('u2', 'B'))
            q.addEdge('u1', Vertex('u3', 'C'))

            g.addEdge(Vertex('v1', 'A'), Vertex('v2', 'B'))
            g.addEdge('v1', Vertex('v3', 'C'))
            g.addEdge('v3', 'v2')
            g.addEdge('v3', Vertex('v4', 'B'))
            g.addEdge('v3', Vertex('v5', 'C'))

            # Match u1 with v1. Then check to see if u2 and v4 are joinable.
            # They are not because there is no edge between v4 and v1 (draw out
            # the graphs on paper and this will make sense).
            matches = { 'u1':'v1', 'v1':'u1' }
            u = q.vertices['u2']
            v = g.vertices['v4']
            self.assertFalse(g._isJoinable(u, v, q, matches))

            # Test if u2 can be matched to v2. It can.
            u = q.vertices['u2']
            v = g.vertices['v2']
            self.assertTrue(g._isJoinable(u, v, q, matches))	    

    def XtestRestoreState(self):
            g = Graph()

            matches = {}
            u1 = Vertex('u1')
            v1 = Vertex('v1')
            g._updateState(u1, v1, matches)
            u2 = Vertex('u2')
            v2 = Vertex('v2')
            g._updateState(u2, v2, matches)
            self.assertEquals(len(matches), 2)

            matches = g._restoreState(matches)
            # RestoreState should have removed the last two matches.
            self.assertEquals(len(matches), 1)

            matches = g._restoreState(matches)
            # Now we should have nothing left.
            self.assertEquals(len(matches), 0)

    def XtestUpdateState(self):
            matches = {}
            u = Vertex('u1')
            v = Vertex('v1')
            g = Graph()
            g._updateState(u, v, matches)
            self.assertEquals(len(matches), 1)
            self.assertEquals(matches[u.id], 'v1')


