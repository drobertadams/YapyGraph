import unittest

from src.Graph import Graph
from src.Vertex import Vertex

class TestGraphClass(unittest.TestCase):

    # =========================================================================
    def setUp(self):
        # Build empty data and query graphs.
        self.g = Graph()
        self.q = Graph()

        # Build data and query graphs with vertices and edges.
        self.g2 = Graph()
        self.g2.addVertex( Vertex('v1', 'A') )
        self.g2.addVertex( Vertex('v2', 'B') )
        self.g2.addVertex( Vertex('v3', 'A') )
        self.g2.addVertex( Vertex('v4', 'A') )
        self.g2.addVertex( Vertex('v5', ['B','D']) )
        self.g2.addVertex( Vertex('v6', 'A') )
        self.g2.addVertex( Vertex('v7', ['B','C']) )
        self.g2.addVertex( Vertex('v8', 'B') )
        self.g2.addVertex( Vertex('v9', 'C') )
        self.g2.addEdge('v1', 'v4', True)
        self.g2.addEdge('v2', 'v4', True)
        self.g2.addEdge('v2', 'v5', True)
        self.g2.addEdge('v3', 'v5', True)
        self.g2.addEdge('v3', 'v6', True)
        self.g2.addEdge('v4', 'v5', True)
        self.g2.addEdge('v4', 'v8', True)
        self.g2.addEdge('v5', 'v6', True)
        self.g2.addEdge('v5', 'v9', True)
        self.g2.addEdge('v7', 'v8', True)

        self.q2 = Graph()
        self.q2.addVertex( Vertex('u1', 'A'))
        self.q2.addVertex( Vertex('u2', 'B'))
        self.q2.addVertex( Vertex('u3', 'C'))
        self.q2.addVertex( Vertex('u4', 'A'))
        self.q2.addEdge('u1', 'u2', True)
        self.q2.addEdge('u1', 'u4', True)
        self.q2.addEdge('u2', 'u4', True)
        self.q2.addEdge('u2', 'u3', True)

    # =========================================================================
    def testAddVertex(self):
        # Adding a new vertex.
        v = self.g.addVertex(Vertex('u1'))

        self.assertTrue('u1' in self.g._vertices)           # u1 is in the list of vertices ?
        self.assertTrue(len(self.g._edges['u1']) == 0)      # u1 has no edges ?
        # self.assertTrue(len(self.g._neighbors['u1']) == 0)  # u1 has no neighbors ?

        # Trying to add an existing vertex should return the existing vertex.
        self.assertEquals(self.g.addVertex(v), v)

    # =========================================================================
    def testAddEdge(self):
        # Add edge between two existing vertices.
        u1 = self.g.addVertex(Vertex('u1', 'A'))
        u2 = self.g.addVertex(Vertex('u2', 'B'))
        self.g.addEdge('u1', 'u2')                      # u1 -> u2

        self.assertTrue(u2 in self.g._edges['u1'])      # u1 -> u2 ?
        self.assertTrue(u1 not in self.g._edges['u2'])  # u2 !-> u1 ?
        # self.assertTrue(u2 in self.g._neighbors['u1'])  # u1 and u2 are neighbors?
        # self.assertTrue(u1 in self.g._neighbors['u2'])  # u2 and u1 are neighbors?

        # Add edge between one existing vid and one new Vertex.
        self.g.addEdge('u1', Vertex('u3', 'C'))         # u1 -> u3
        u3 = self.g._vertices['u3']

        self.assertTrue(u3 in self.g._edges['u1'])      # u1 -> u3 ?
        self.assertTrue(u1 not in self.g._edges['u3'])  # u3 !-> u1 ?
        # self.assertTrue(u3 in self.g._neighbors['u1'])  # u1 and u3 are neighbors?
        # self.assertTrue(u1 in self.g._neighbors['u3'])  # u3 and u1 are neighbors?

        # Add edge with one new Vertex object and one existing vid (opposite of the previous case)
        self.g.addEdge(Vertex('u4', 'D'), 'u1')         # u4 -> u1
        u4 = self.g._vertices['u4']

        self.assertTrue(u1 in self.g._edges['u4'])      # u4 -> u1 ?
        self.assertTrue(u4 not in self.g._edges['u1'])  # u1 !-> u1 ?
        # self.assertTrue(u4 in self.g._neighbors['u1'])  # u1 and u4 are neighbors?
        # self.assertTrue(u1 in self.g._neighbors['u4'])  # u4 and u1 are neighbors?

        # Add edge with two new Vertex objects.
        self.g.addEdge( Vertex('u5', 'E'), Vertex('u6', 'F') )
        u5 = self.g._vertices['u5']
        u6 = self.g._vertices['u6']

        self.assertTrue(u6 in self.g._edges['u5'])      # u5 -> u6 ?
        self.assertTrue(u5 not in self.g._edges['u6'])  # u6 !-> u5 ?
        # self.assertTrue(u5 in self.g._neighbors['u6'])  # u5 and u6 are neighbors?
        # self.assertTrue(u6 in self.g._neighbors['u5'])  # u6 and u5 are neighbors?
    
        # Make sure the vertex degrees were updated.
        self.assertEquals(self.g._vertices['u1'].degree, 3)
        self.assertEquals(self.g._vertices['u2'].degree, 1)
        self.assertEquals(self.g._vertices['u3'].degree, 1)
        self.assertEquals(self.g._vertices['u4'].degree, 1)
        self.assertEquals(self.g._vertices['u5'].degree, 1)
        self.assertEquals(self.g._vertices['u6'].degree, 1)

        # Try a bi-directional edge.
        u11 = self.g.addVertex(Vertex('u11', 'A'))
        u12 = self.g.addVertex(Vertex('u12', 'B'))
        self.g.addEdge('u11', 'u12', True) 
        self.assertTrue(u12 in self.g._edges['u11'])      # u1 -> u2 ?
        self.assertTrue(u11 in self.g._edges['u12'])      # u2 -> u1 ?
        # self.assertTrue(u12 in self.g._neighbors['u11'])  # u1 and u2 are neighbors?
        # self.assertTrue(u11 in self.g._neighbors['u12'])  # u2 and u1 are neighbors?

    # =========================================================================
    def testDeleteEdge(self):
        # Referencing non-existing vertices should return False
        self.assertFalse(self.g.deleteEdge('aaa', 'bbb'))

        # Build u1->u2.
        self.g.addEdge(Vertex('u1', 'A'), Vertex('u2', 'B'))
        u1 = self.g._vertices['u1']
        u2 = self.g._vertices['u2']

        # Trying to delete u2->u1 should fail because there's
        # no edge running that way.
        self.assertFalse(self.g.deleteEdge('u2', 'u1'))

        # Deleting a non-existent edge should return False.
        self.assertFalse(self.g.deleteEdge('u1', 'bbb'))

        # Add an edge running u2->u1.
        self.g.addEdge('u2', 'u1')

        # Deleting an existing edge should return True.
        self.assertTrue(self.g.deleteEdge('u1', 'u2'))

        # u2 should not appear in the list of edges from u1 anymore.
        self.assertTrue(u2 not in self.g._edges['u1'])

        # u2 should still appear in the list of neighbors of u1.
        # self.assertTrue(u2 in self.g._neighbors['u1'])

        # Both vertex degrees should be decremented.
        self.assertEquals(u1.degree, 1)
        self.assertEquals(u2.degree, 1)

        # Delete the last edge between u1 and u2.
        self.assertTrue(self.g.deleteEdge('u2', 'u1'))
        self.assertTrue(u1 not in self.g._edges['u2'])  # edge is gone ?
        # self.assertFalse(u1 in self.g._neighbors['u2']) # no longer neighbors ?
        # self.assertFalse(u2 in self.g._neighbors['u1'])
        self.assertEquals(u1.degree, 0)                 # no neighbors at all ?
        self.assertEquals(u2.degree, 0)

    # =========================================================================
    def testDeleteVertex(self):
        # Deleting a non-existing vertex returns None.
        self.assertIsNone(self.g.deleteVertex('X'))

        # Build A->B, B->A
        self.g.addEdge(Vertex('u1', 'A'), Vertex('u2', 'B'), True)

        # Delete u1.
        self.g.deleteVertex('u1')

        # u1 shouldn't appear anywhere in edges.
        self.assertTrue('u1' not in self.g._edges)
        self.assertTrue('u1' not in self.g._edges['u2'])

        # u1 isn't a vertex anymore.
        self.assertTrue('u1' not in self.g._vertices)

    # =========================================================================
    def testEdgesProperty(self):
        # Build u1->u2, u2->u3
        self.g.addEdge(Vertex('u1'), Vertex('u2'))
        self.g.addEdge('u2', Vertex('u3'))

        # Make sure that edges returns u1->u2 and u2->u3
        for e in self.g.edges():
            if e[0].id == 'u1':
                self.assertEquals(e[1].id, 'u2')
            elif e[0].id == 'u2':
                self.assertEquals(e[1].id, 'u3')
            else:
                self.assertFalse(True)

    # =========================================================================
    def testFindVertex(self):
        self.assertIsNone(self.g.hasVertex('X'))       # there is no "X" in empty graph

        # Add a single vertex with name "A1".
        u1 = self.g.addVertex(Vertex('u1', 'A', 1))

        self.assertIsNone(self.g.hasVertex('X'))       # there is no "X"
        self.assertIsNone(self.g.hasVertex('A2'))      # there is no "A2"
        self.assertIsNone(self.g.hasVertex('X1'))      # there is no "X1"
        self.assertEqual(self.g.hasVertex('A1'), u1)   # but there is an A1
    
    # =========================================================================
    def testHasEdge(self):
        # Build u0 -> u1 -> u2
        self.g.addEdge(Vertex('u0', 'A'), Vertex('u1', 'B'))
        self.g.addEdge('u1', Vertex('u2', 'C'))

        self.assertTrue(self.g.hasEdge('u0','u1'))   # should be true
        self.assertFalse(self.g.hasEdge('u0','u2'))  # should be false
        self.assertFalse(self.g.hasEdge('XX','XX'))  # non-existent vertices
        self.assertFalse(self.g.hasEdge('u0','XX'))  # non-existent vertex
        
    # =========================================================================
    def testNumVertices(self):
        self.assertEquals(self.g.numVertices(), 0)    # empty graph has no vertices

        a = self.g.addVertex(Vertex('u1'))
        self.assertEquals(self.g.numVertices(), 1)    # one vertex

        self.g.addVertex(Vertex('u2', 'B', 2))
        self.assertEquals(self.g.numVertices(), 2)    # two vertices

    # =========================================================================
    def testRepr(self):
        # Test of the output function (__repr__).

        # No vertices.
        self.assertEquals(self.g.__repr__(), "digraph {\n\n}")

        # A
        self.g.addVertex(Vertex('u1', 'A'))
        self.assertEquals(self.g.__repr__(), 'digraph {\n"u1,A,"\n}')

        # A->B
        self.g.addEdge('u1', Vertex('u2', 'B'))
        self.assertEquals(self.g.__repr__(), 'digraph {\n"u1,A,"->"u2,B,";\n\n}')

        # A->B->C
        self.g.addEdge('u2', Vertex('u3', 'C'))
        self.assertEquals(self.g.__repr__(), 'digraph {\n"u1,A,"->"u2,B,";\n"u2,B,"->"u3,C,";\n\n}')

        # A->B->C, A->D
        self.g.addEdge('u1', Vertex('u4', 'D'))
        self.assertEquals(self.g.__repr__(), 'digraph {\n"u1,A,"->"u2,B,";\n"u1,A,"->"u4,D,";\n"u2,B,"->"u3,C,";\n\n}')

    # =========================================================================
    def testVertices(self):
        self.assertEquals( len(self.g.vertices()), 0 ) # empty graph has no vertices

        u1 = Vertex('u1')   # add three vertices
        u2 = Vertex('u2')
        u3 = Vertex('u3')
        self.g.addVertex(u1)
        self.g.addVertex(u2)
        self.g.addVertex(u3)

        vertices = self.g.vertices()
        self.assertEquals(len(vertices), 3)
        self.assertTrue(u1 in vertices)		
        self.assertTrue(u2 in vertices)		
        self.assertTrue(u3 in vertices)			
        
    # =========================================================================
    def test_filterCandidates(self):
        # Empty graph produces no results.
        c = self.g._filterCandidates(Vertex('u1', 'A'))
        self.assertTrue( len(c) == 0 )

        # Build A(u0) -> B(u1) -> C(u2) -> A(u3) -> D(u4)
        self.g.addEdge(Vertex('u0', 'A'), Vertex('u1', 'B'))
        self.g.addEdge('u1', Vertex('u2', 'C'))
        self.g.addEdge('u2', Vertex('u3', 'A'))
        self.g.addEdge('u3', Vertex('u4', 'D'))

        # Use the full graph to search for 'A' with degree 1. Should find 4 vertices.
        c = self.g2._filterCandidates( Vertex('x', 'A') )
        self.assertEquals( len(c), 4 )

        # Grab vertex u1 from the sample query graph. It has degree 2.
        a = self.q2._vertices['u1']
        # u1 should have 3 candidates in g2.
        c = self.g2._filterCandidates(a)
        self.assertEquals( len(c), 3 )

    # =========================================================================
    def test_findCandidates(self):
        # Empty data and query graphs produce no results.
        c = self.g._findCandidates( self.q )
        self.assertEquals( len(c) , 0 )

        # Empty data graph produces no results.
        c = self.g._findCandidates( self.q2 )
        self.assertEquals( len(c) , 0 )

        # Empty query graph produces no results.
        c = self.g2._findCandidates( self.q )
        self.assertEquals( len(c) , 0 )

        # Find candidates for q2 in g2. We should get four candidates, at least
        # one for each V(q)
        c = self.g2._findCandidates( self.q2 )
        self.assertEquals( len(c), 4 )
        self.assertEquals( len(c['u1']), 3 ) # u1 has 3 candidates
        self.assertEquals( len(c['u2']), 1 ) # u2 has 1 candidate
        self.assertEquals( len(c['u3']), 2 ) # u3 has 2 candidates
        self.assertEquals( len(c['u4']), 3 ) # u4 has 3 candidates

    # =========================================================================
    def test_findMatchedNeighbors(self):
        # No query vertex returns no results.
        self.assertEquals( len(self.q2._findMatchedNeighbors(None, self.q2, {})), 0 )

        # Searching for u1 returns nothing because nothing has been matched.
        u1 = self.q2._vertices['u1']
        self.assertEquals( len(self.q2._findMatchedNeighbors(u1, self.q2, {})), 0 )

        # After we match u2, then we get 1 result back.
        self.assertEquals( len(self.q2._findMatchedNeighbors(u1, self.q2, {'u2':'v2'})), 1 )

        # After we match u2 and u3, then we get 2 results back.
        self.assertEquals( len(self.q2._findMatchedNeighbors(u1, self.q2, {'u2':'v2', 'u3':'v3'})), 1 )

    # =========================================================================
    def test_isJoinable(self):
        u1 = self.q2._vertices['u1']
        v3 = self.g2._vertices['v3']

        # Joining u1 and v3 is true because nothing has been matched yet.
        self.assertTrue( self.g2._isJoinable(u1, v3, self.q2, {}) )

    # =========================================================================
    def test_isMatched(self):
        v = Vertex('v4')

        # v4 does not appear in the matches.
        self.assertFalse( self.g2._isMatched(v, {}))

        # v4 is in the keys of the matches.
        self.assertTrue( self.g2._isMatched(v, {'u1':'v1', 'u2':'v2', 'u3':'v3', 'v4':'u4'}))

        # v4 is in the values of the matches.
        self.assertTrue( self.g2._isMatched(v, {'u1':'v1', 'u2':'v2', 'u3':'v3', 'u4':'v4'}))

    # =========================================================================
    def test_nextQueryVertex(self):
        # Empty data graph returns None.
        q = Graph()
        self.assertIsNone( self.g._nextQueryVertex(q, {}) )

        # Empty query graph returns None.
        self.assertIsNone( self.g2._nextQueryVertex(q, {}) )

        # Running this on g2 and q2 should result in u1 being returned.
        u = self.g2._nextQueryVertex(self.q2, {}) 
        self.assertEquals(u.id, 'u1')

        # "Match" u1 and try again.
        u = self.g2._nextQueryVertex(self.q2, {'u1':'v1'}) 
        self.assertEquals(u.id, 'u2')

        # "Match" all query vertices should return None.
        u = self.g2._nextQueryVertex(self.q2, {'u1':'v1', 'u2':'v2', 'u3':'v3', 'u4':'v4'}) 
        self.assertIsNone(u)
    
    # =========================================================================
    def test_search(self):
        # Searching with an empty data graph returns nothing.
        self.assertEquals( len(self.g.search(self.q2)), 0 )

        # Searching with an empty query graph returns nothing.
        self.assertEquals( len(self.g2.search(self.q)), 0 )

        # Test our pre-defined problem, which has two solutions.
        self.assertEquals( len(self.g2.search(self.q2)), 2 )

if __name__ == '__main__':
    unittest.main()
