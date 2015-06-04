import unittest

from YapyGraph.Graph import Graph
from YapyGraph.Vertex import Vertex

class TestGraphSearch(unittest.TestCase):

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
        u1 = q._vertices['u1']
        self.assertTrue(g._findCandidates(q))
        self.assertEquals(len(u1.candidates), 1)
        
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

    def testIsJoinable(self):
        # If there are no matched vertices yet (we just started the matching
        # process), then should return True.
        g = Graph()
        self.assertTrue(g._isJoinable(None, None, None, {}))

        # If there are matches, but none adjacent to u, then should
        # return False.
        g = Graph()
        g.addEdge(Vertex('v1'), Vertex('v2'))
        v = g._vertices['v1']

        q = Graph()
        q.addEdge(Vertex('u1'), Vertex('u2'))
        u = q._vertices['u1']
        self.assertFalse(g._isJoinable(u, v, q, {'u3':'v3', 'v3':'u3'}))

        # If an edge exists between u and n, but the other direction between 
        # v and m, should return False
        g = Graph()
        g.addEdge(Vertex('v1'), Vertex('v2'))
        v = g._vertices['v1']

        q = Graph()
        q.addEdge(Vertex('u2'), Vertex('u1'))
        u = q._vertices['u1']
        self.assertFalse(g._isJoinable(u, v, q, {'u2':'v2', 'v2':'u2'}))

        # If an edge exists between n and u, but the other direction between 
        # m and v, should return False
        g = Graph()
        g.addEdge(Vertex('v2'), Vertex('v1'))
        v = g._vertices['v1']

        q = Graph()
        q.addEdge(Vertex('u1'), Vertex('u2'))
        u = q._vertices['u1']
        self.assertFalse(g._isJoinable(u, v, q, {'u2':'v2', 'v2':'u2'}))

        # Correct case 1. Edge between u and n, and between v and m.
        g = Graph()
        g.addEdge(Vertex('v1'), Vertex('v2'))
        v = g._vertices['v1']

        q = Graph()
        q.addEdge(Vertex('u1'), Vertex('u2'))
        u = q._vertices['u1']
        self.assertTrue(g._isJoinable(u, v, q, {'u2':'v2', 'v2':'u2'}))

        # Correct case 2. Edge between n and u, and between m and v.
        g = Graph()
        g.addEdge(Vertex('v2'), Vertex('v1'))
        v = g._vertices['v1']

        q = Graph()
        q.addEdge(Vertex('u2'), Vertex('u1'))
        u = q._vertices['u1']
        self.assertTrue(g._isJoinable(u, v, q, {'u2':'v2', 'v2':'u2'}))

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
        u = Vertex('g0') # query vertex
        v = Vertex('g0') # data vertex

        # Test with unmatched candidate with the v.degree >= u.degree. This
        # should return the id of v.
        u.degree = 1
        v.degree = 1
        c = [ v ]
        c = g._refineCandidates(c, u, {})
        self.assertEqual(len(c), 1)
        self.assertEqual(c[0].id, 'g0')

        # Test with matched candidate with v.degree >= u.degree. This should
        # return no candidates.
        u.degree = 1
        v.degree = 1
        m = { 'g0':'g0' }
        c = g._refineCandidates(c, u, m)
        self.assertEqual(len(c), 0)

        # Test with unmatched candidate with v.degree < u.degree. This should
        # return no candidates.
        u.degree = 1
        v.degree = 0
        c = g._refineCandidates(c, u, {})
        self.assertEqual(len(c), 0)

        # Test with matched candidate with v.degree < u.degree. This should
        # return no candidates.
        u.degree = 1
        v.degree = 0
        m = { 'g0':'g0' }
        c = g._refineCandidates(c, u, m)
        self.assertEqual(len(c), 0)

    def testRestoreState(self):
        # Save state with a couple calls to updateState() and then see that 
        # they are undone.
        g = Graph()
        matches = {}
        u1 = Vertex('u1')
        v1 = Vertex('v1')
        g._updateState(u1, v1, matches) # u1 matched with v1
        u2 = Vertex('u2')
        v2 = Vertex('v2')
        g._updateState(u2, v2, matches) # u2 matched with v2

        # Now we should get the dictionary with only the original set of 
        # matches.
        matches = g._restoreState(matches)
        self.assertEquals(len(matches), 1)
        self.assertTrue('u1' in matches)
        self.assertTrue(matches['u1'], 'v1')

        # Now we should have an empty dictionary.
        matches = g._restoreState(matches)
        self.assertEquals(len(matches), 0)

    def testSearchNoCandidates(self):
        # If there are no suitable candidate data vertices for every
        # query vertex, then the returned solutions list should be empty.
        g = Graph()
        g.addEdge(Vertex('v1', 'A'), Vertex('v2', 'B'))
        q = Graph()
        q.addEdge(Vertex('u1', 'Z'), Vertex('u2', 'Y'))
        solutions = g.search(q)
        self.assertEquals(len(solutions), 0)

    def testSearchOneSimpleSolution(self):
        g = Graph()
        g.addEdge(Vertex('v1', 'A'), Vertex('v2', 'B'))
        g.addEdge('v1', Vertex('v3', 'C'))

        # Query graph is exact replica.
        q = Graph()
        q.addEdge(Vertex('u1', 'A'), Vertex('u2', 'B'))
        q.addEdge('u1', Vertex('u3', 'C'))

        solutions = g.search(q)

        self.assertEquals(len(solutions), 1)
        self.assertEquals(solutions[0]['u1'], 'v1')
        self.assertEquals(solutions[0]['u2'], 'v2')
        self.assertEquals(solutions[0]['u3'], 'v3')

    def testSearchTwoSolutions(self):
        # A1_g0->B_g1->C_g2, A2_g3->B_g1
        g = Graph()
        g.addEdge(Vertex('g0', 'A'), Vertex('g1', 'B'))
        g.addEdge('g1', Vertex('g2', 'C'))
        g.addEdge(Vertex('g3', 'A'), 'g1')
        #g.addEdge('g3', 'g2')

        # A_g0->B_g1->C_g2
        q = Graph()
        q.addEdge(Vertex('g0', 'A'), Vertex('g1', 'B'))
        q.addEdge('g1', Vertex('g2', 'C'))

        solutions = g.search(q)

        self.assertEquals(len(solutions), 2)

        # First A->B,C is found.
        self.assertEquals(solutions[0]['g0'], 'g3')
        self.assertEquals(solutions[0]['g1'], 'g1')
        self.assertEquals(solutions[0]['g2'], 'g2')

        # Second A->B,C is found.
        self.assertEquals(solutions[1]['g0'], 'g0')
        self.assertEquals(solutions[1]['g1'], 'g1')
        self.assertEquals(solutions[1]['g2'], 'g2')

    def testSubgraphSearchSolutionFound(self):
        # Test that when the length of query=>data vertex matches is the 
        # same as the number of query vertices, then the solution is stored.
        g = Graph()
        q = Graph()
        q.addVertex(Vertex('u1', 'A')) # one query vertex
        matches = {'u1':'v1'} # one match
        g._subgraphSearch(matches, q)
        self.assertEqual(len(g._solutions), 1)

    def testSubgraphSearchSolutionNoCandidates(self):
        # Test when an umatched query vertex doesn't have any candidates, we
        # don't find any solutions.
        g = Graph()
        g.addVertex(Vertex('v1', 'A'))
        q = Graph()
        q.addVertex(Vertex('u1', 'B'))
        matches = {}
        self.assertEqual(len(g._solutions), 0)
        g._subgraphSearch(matches, q)
        self.assertEqual(len(g._solutions), 0)

    def testSubgraphSearchOneCandidateNotJoinable(self):
        # The query vertex has a candidate data vertex, but they aren't
        # "joinable" -- no solution.
        g = Graph()
        g.addVertex(Vertex('v1', 'A'))
        g.addVertex(Vertex('v2', 'B'))
        v1 = g._vertices['v1']

        q = Graph()
        q.addEdge(Vertex('u1', 'A'), Vertex('u2', 'B'))
        q._vertices['u1'].candidates = [v1]

        # u2 and v2 are already matched. There's an edge between u1 and
        # u2, but no edge between v1 and v2 so u1 and v1 cannot be matched.
        matches = {'u2':'v2'}
        self.assertEqual(len(g._solutions), 0)
        g._subgraphSearch(matches, q)
        self.assertEqual(len(g._solutions), 0)

    def testSubgraphSearchSimpleSolution(self):
        # One simple solution.
        g = Graph()
        g.addVertex(Vertex('v1', 'A'))
        v1 = g._vertices['v1']

        q = Graph()
        q.addVertex(Vertex('u1', 'A'))
        q._vertices['u1'].candidates = [v1]

        self.assertEqual(len(g._solutions), 0)
        g._subgraphSearch({}, q)
        self.assertEqual(len(g._solutions), 1)
        self.assertIn('u1', g._solutions[0])
        self.assertEquals(g._solutions[0]['u1'], 'v1')

    def testUpdateState(self):
        matches = {}
        u = Vertex('u1')
        v = Vertex('v1')
        g = Graph()
        g._updateState(u, v, matches)
        self.assertEquals(len(g._matchHistory), 1)
        self.assertEquals(len(matches), 1)
        self.assertEquals(matches[u.id], 'v1')
