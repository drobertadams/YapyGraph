import unittest

from PGC.Graph.Graph import Graph
from PGC.Graph.Vertex import Vertex

class TestGraphClass(unittest.TestCase):

    def setUp(self):
        self.g = Graph();

    def testConstructor(self):
        """New graphs should be empty."""
        self.assertTrue(len(self.g.vertices) == 0)
        self.assertTrue(len(self.g._edges) == 0)
        self.assertTrue(len(self.g.neighbors) == 0)
 
    def testAddVertexWithoutVertex(self):
        """Trying to addVertex() without a Vertex object."""
        self.assertRaises(TypeError, self.g.addVertex, None)

    def testAddVertex(self):
        a = self.g.addVertex(Vertex('u1'))
        self.assertTrue('u1' in self.g.vertices)

    def testAddVertexAlreadyExists(self):
        """Adding an existing vertex should raise an exception."""
        v = self.g.addVertex(Vertex('u1'))
        self.assertRaises(IndexError, self.g.addVertex, v)

    def testAddEdge(self):
        # Add an edge between a vertex that already exists and one that 
        # doesn't.
        a = self.g.addVertex(Vertex('u1', 'A'))
        self.g.addEdge('u1', Vertex('u2', 'B'))
        b = self.g.vertices['u2']

        # Make sure 'A' points to 'B'
        self.assertTrue(b in self.g._edges['u1'])

        # Make sure 'A' and 'B' are neighbors of each other.
        self.assertTrue(b in self.g.neighbors['u1'])
        self.assertTrue(a in self.g.neighbors['u2'])

        # Make sure the vertex degrees were updated.
        self.assertEquals(self.g.vertices['u1'].degree, 1)
        self.assertEquals(self.g.vertices['u2'].degree, 1)

    def testDeleteEdge(self):
        # Deleting an edge that doesn't exist should return False.
        self.assertFalse(self.g.deleteEdge('aaa', 'bbb'))

        self.g.addEdge(Vertex('u1', 'A'), Vertex('u2', 'B'))
        self.g.addEdge('u1', Vertex('u3', 'C'))
        u1 = self.g.vertices['u1']
        u2 = self.g.vertices['u2']
        u3 = self.g.vertices['u3']

        self.g.deleteEdge('u1', 'u2')

        # u2 should not appear in the list of edges from u1.
        self.assertTrue(u2 not in self.g._edges['u1'])

        # u2 should not appear in the list of neighbors of u1.
        self.assertTrue(u2 not in self.g.neighbors['u1'])

        # Since u2 isn't linked to anyone, it shouldn't even appear in the
        # neighbors dict.
        self.assertTrue(u2 not in self.g.neighbors)

        # Both vertex degress should be decremented.
        self.assertEquals(u1.degree, 1)
        self.assertEquals(u2.degree, 0)

        self.g.deleteEdge('u1', 'u3')
        
        # Since we just removed the last egde from u1, u1 should not appear
        # in the _edges of neighbors dict.
        self.assertTrue('u1' not in self.g._edges)
        self.assertTrue('u1' not in self.g.neighbors)
        self.assertTrue('u3' not in self.g.neighbors)

    def testDeleteVertex(self):
        # Deleting a non-existing vertex raises an exception.
    	self.assertRaises(KeyError, self.g.deleteVertex, 'X')

        # Build a graph and then remove 'A'.
        # Build A->B
        self.g.addEdge(Vertex('u1', 'A'), Vertex('u2', 'B'))
        # Build B->A. This allows us to test that A is removed from the edges
        # leading out of B.
        self.g.addEdge('u2', 'u1')
        # Build B->C, otherwise B gets removed from _edges when then the last
        # edge from B is removed.
        self.g.addEdge('u2', Vertex('u3', 'C'))

        self.g.deleteVertex('u1')

        self.assertTrue('u1' not in self.g.vertices)
        self.assertTrue('u1' not in self.g._edges)
        self.assertTrue('u1' not in self.g._edges['u2'])
        self.assertTrue('u1' not in self.g.neighbors)
        self.assertTrue('u1' not in self.g.neighbors['u2'])

# TODO: LEFT OFF HERE

    def testEdgeExistsBewtweenLabels(self):
         # Add a vertex "A".
        a = self.g.addVertex(Vertex('u1', 'A'))

        # "Manually" add a vertex 'B', then connect it with 'A'.
        b = self.g.addVertex(Vertex('u2', 'B'))
        self.g.addEdge('u1', 'u2')

        self.assertFalse(self.g.edgeExistsBetweenLabels('X', 'Y'))
        self.assertTrue(self.g.edgeExistsBetweenLabels('A', 'B'))

    def testEdgesProperty(self):
         # Add a vertex "A".
        a = self.g.addVertex(Vertex('u1'))

        # "Manually" add a vertex 'B', then connect it with 'A'.
        b = self.g.addVertex(Vertex('u2', 'B'))
        self.g.addEdge('u1', 'u2')

        # Add an edge from u1 to a new vertex 'C'
        c = Vertex('u3', 'C')
        self.g.addEdge('u2', c)

        for e in self.g.edges:
        	if e[0].id == 'u1':
	        	self.assertEquals(e[1].id, 'u2')
	        elif e[0].id == 'u2':
	        	self.assertEquals(e[1].id, 'u3')
	        else:
	        	self.assertFalse(True)

    def testHasEdgeBetween(self):
        # Build a little graph: A->B,A->C.
        self.g.addEdge(Vertex('u0', 'A'), Vertex('u1', 'B'))
        self.g.addEdge('u0', Vertex('u2', 'C'))

        self.assertTrue(self.g.hasEdgeBetween('u0','u1'))
        self.assertTrue(self.g.hasEdgeBetween('u0','u2'))
        self.assertFalse(self.g.hasEdgeBetween('u1','u2'))
        self.assertFalse(self.g.hasEdgeBetween('u99','u2'))
        

    def testLabelsProperty(self):
        self.g.addVertex(Vertex('u1', 'A'))
        self.g.addVertex(Vertex('u2', 'B'))
        self.g.addVertex(Vertex('u3', 'C'))
        self.assertEquals(len(self.g.labels), 3)
        self.assertTrue('A' in self.g.labels)		
        self.assertTrue('B' in self.g.labels)		
        self.assertTrue('C' in self.g.labels)		

    def testNumVertices(self):
        # Empty graph.
        self.assertEquals(self.g.numVertices, 0)

        # One vertex.
        a = self.g.addVertex(Vertex('u1'))
        self.assertEquals(self.g.numVertices, 1)

if __name__ == '__main__':
    unittest.main()
