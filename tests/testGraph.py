import unittest

from YapyGraph.Graph import Graph
from YapyGraph.Vertex import Vertex

class TestGraphClass(unittest.TestCase):

    def setUp(self):
        self.g = Graph();

    def testConstructor(self):
        # New graphs should be empty.
        self.assertTrue(len(self.g._vertices) == 0)
        self.assertTrue(len(self.g._edges) == 0)
        self.assertTrue(len(self.g._neighbors) == 0)
 
    def testAddVertex(self):
        # Correct add.
        v = self.g.addVertex(Vertex('u1'))
        self.assertTrue('u1' in self.g._vertices)

        # Adding an existing vertex should return the existing vertex.
        self.assertEquals(self.g.addVertex(v), v)

    def testAddEdge(self):
        # Add edge with two vid's
        a = self.g.addVertex(Vertex('u1', 'A'))
        b = self.g.addVertex(Vertex('u2', 'B'))
        self.g.addEdge('u1', 'u2')

        # Add edge with one vid and one Vertex.
        self.g.addEdge('u1', Vertex('u3', 'C'))
        c = self.g._vertices['u3']

        # Add edge with one Vertex and one vid.
        self.g.addEdge(Vertex('u4', 'D'), 'u1')
        d = self.g._vertices['u4']

        # Add edge with two Vertics.
        self.g.addEdge(Vertex('u5', 'E'), Vertex('u6', 'F'))
        e = self.g._vertices['u5']
        f = self.g._vertices['u6']

        # Make sure A points to B and C.
        self.assertTrue(b in self.g._edges['u1'])
        self.assertTrue(c in self.g._edges['u1'])
        self.assertTrue(a in self.g._edges['u4'])
        self.assertTrue(f in self.g._edges['u5'])

        # Make sure neighbors all reference each other.
        self.assertTrue(b in self.g._neighbors['u1'])
        self.assertTrue(c in self.g._neighbors['u1'])
        self.assertTrue(d in self.g._neighbors['u1'])

        self.assertTrue(a in self.g._neighbors['u2'])
        self.assertTrue(a in self.g._neighbors['u3'])
        self.assertTrue(a in self.g._neighbors['u4'])

        self.assertTrue(e in self.g._neighbors['u6'])
        self.assertTrue(f in self.g._neighbors['u5'])

        # Make sure the vertex degrees were updated.
        self.assertEquals(self.g._vertices['u1'].degree, 3)
        self.assertEquals(self.g._vertices['u2'].degree, 1)
        self.assertEquals(self.g._vertices['u3'].degree, 1)
        self.assertEquals(self.g._vertices['u4'].degree, 1)
        self.assertEquals(self.g._vertices['u5'].degree, 1)
        self.assertEquals(self.g._vertices['u6'].degree, 1)

    def testDeleteEdge(self):
        # Referencing non-existing vertices should return False
        self.assertFalse(self.g.deleteEdge('aaa', 'bbb'))

        # Build A->B
        self.g.addEdge(Vertex('u1', 'A'), Vertex('u2', 'B'))
        u1 = self.g._vertices['u1']
        u2 = self.g._vertices['u2']

        # Deleting a non-existant edge should return False.
        self.assertFalse(self.g.deleteEdge('u1', 'bbb'))

        # Deleting an existing edge should return True.
        self.assertTrue(self.g.deleteEdge('u1', 'u2'))

        # u2 should not appear in the list of edges from u1.
        self.assertTrue(u2 not in self.g._edges['u1'])

        # u2 should not appear in the list of neighbors of u1.
        self.assertTrue(u2 not in self.g._neighbors['u1'])

        # Both vertex degress should be decremented.
        self.assertEquals(u1.degree, 0)
        self.assertEquals(u2.degree, 0)

    def testDeleteVertex(self):
        # Deleting a non-existing vertex raises an exception.
    	self.assertIsNone(self.g.deleteVertex('X'))

        # Build A->B, B->A
        self.g.addEdge(Vertex('u1', 'A'), Vertex('u2', 'B'))
        self.g.addEdge('u2', 'u1')
        u1 = self.g._vertices['u1']
        u2 = self.g._vertices['u2']

        self.g.deleteVertex('u1')

        # u1 shouldn't appear anywhere as an edge or neighbor.
        self.assertTrue('u1' not in self.g._edges)
        self.assertTrue('u1' not in self.g._neighbors)
        self.assertTrue('u1' not in self.g._edges['u2'])
        self.assertTrue('u1' not in self.g._neighbors['u2'])

        # u1 isn't a vertex anymore.
        self.assertTrue('u1' not in self.g._vertices)

    def testEdgesProperty(self):
        # Build A->B, B->C
        self.g.addEdge(Vertex('u1', 'A'), Vertex('u2', 'B'))
        self.g.addEdge('u2', Vertex('u3', 'C'))

        for e in self.g.edges:
            if e[0].id == 'u1':
                self.assertEquals(e[1].id, 'u2')
            elif e[0].id == 'u2':
                self.assertEquals(e[1].id, 'u3')
            else:
                self.assertFalse(True)

    def testFindVertex(self):
        u1 = self.g.addVertex(Vertex('u1', 'A', 1))
        self.assertIsNone(self.g.findVertex('X'))
        self.assertIsNone(self.g.findVertex('A2'))
        self.assertEqual(self.g.findVertex('A1'), u1)

    def testHasEdgeBetweenVertices(self):
        self.g.addEdge(Vertex('u0', 'A'), Vertex('u1', 'B'))
        self.g.addEdge('u1', Vertex('u2', 'C'))

        self.assertTrue(self.g.hasEdgeBetweenVertices('u0','u1'))
        self.assertFalse(self.g.hasEdgeBetweenVertices('u0','u2'))
        self.assertFalse(self.g.hasEdgeBetweenVertices('XX','XX'))
        self.assertFalse(self.g.hasEdgeBetweenVertices('u0','XX'))
        
    def testLabelsProperty(self):
        self.g.addVertex(Vertex('u1', 'A'))
        self.g.addVertex(Vertex('u2', 'B'))
        self.g.addVertex(Vertex('u3', 'C'))
        labels = self.g.labels
        self.assertEquals(len(labels), 3)
        self.assertTrue('A' in labels)		
        self.assertTrue('B' in labels)		
        self.assertTrue('C' in labels)		

    def testNamesProperty(self):
        self.g.addVertex(Vertex('u1', 'A', 1))
        self.g.addVertex(Vertex('u2', 'B', 2))
        self.g.addVertex(Vertex('u3', 'C', 3))
        names = self.g.names
        self.assertEquals(len(names), 3)
        self.assertTrue('A1' in names)		
        self.assertTrue('B2' in names)		
        self.assertTrue('C3' in names)		

    def testNumVertices(self):
        # Empty graph.
        self.assertEquals(self.g.numVertices, 0)

        # One vertex.
        a = self.g.addVertex(Vertex('u1'))
        self.assertEquals(self.g.numVertices, 1)

    def testRepr(self):
        # Test of the output function (__repr__).

        # No vertices.
        self.assertEquals(self.g.__repr__(), "digraph {\n\n}")

        # A
        self.g.addVertex(Vertex('u1', 'A'))
        self.assertEquals(self.g.__repr__(), "digraph {\nA_u1\n}")

        # A->B
        self.g.addEdge('u1', Vertex('u2', 'B'))
        self.assertEquals(self.g.__repr__(), "digraph {\nA_u1->B_u2;\n\n}")

        # A->B->C
        self.g.addEdge('u2', Vertex('u3', 'C'))
        self.assertEquals(self.g.__repr__(), "digraph {\nA_u1->B_u2;\nB_u2->C_u3;\n\n}")

        # A->B->C, A->D
        self.g.addEdge('u1', Vertex('u4', 'D'))
        self.assertEquals(self.g.__repr__(), "digraph {\nA_u1->B_u2;\nA_u1->D_u4;\nB_u2->C_u3;\n\n}")

if __name__ == '__main__':
    unittest.main()
