import unittest

from Graph import Graph
from Vertex import Vertex

class TestGraphClass(unittest.TestCase):

    # =========================================================================
    def setUp(self):
        self.g = Graph();

    # =========================================================================
    def testConstructor(self):
        # New graphs should be empty.
        self.assertTrue(len(self.g._vertices) == 0)
        self.assertTrue(len(self.g._edges) == 0)
        self.assertTrue(len(self.g._neighbors) == 0)
 
    # =========================================================================
    def testAddVertex(self):
        # Adding a new vertex.
        v = self.g.addVertex(Vertex('u1'))

        self.assertTrue('u1' in self.g._vertices)           # u1 is in the list of vertices ?
        self.assertTrue(len(self.g._edges['u1']) == 0)      # u1 has no edges ?
        self.assertTrue(len(self.g._neighbors['u1']) == 0)  # u1 has no neighbors ?

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
        self.assertTrue(u2 in self.g._neighbors['u1'])  # u1 and u2 are neighbors?
        self.assertTrue(u1 in self.g._neighbors['u2'])  # u2 and u1 are neighbors?

        # Add edge between one existing vid and one new Vertex.
        self.g.addEdge('u1', Vertex('u3', 'C'))         # u1 -> u3
        u3 = self.g._vertices['u3']

        self.assertTrue(u3 in self.g._edges['u1'])      # u1 -> u3 ?
        self.assertTrue(u1 not in self.g._edges['u3'])  # u3 !-> u1 ?
        self.assertTrue(u3 in self.g._neighbors['u1'])  # u1 and u3 are neighbors?
        self.assertTrue(u1 in self.g._neighbors['u3'])  # u3 and u1 are neighbors?

        # Add edge with one new Vertex object and one existing vid (opposite of the previous case)
        self.g.addEdge(Vertex('u4', 'D'), 'u1')         # u4 -> u1
        u4 = self.g._vertices['u4']

        self.assertTrue(u1 in self.g._edges['u4'])      # u4 -> u1 ?
        self.assertTrue(u4 not in self.g._edges['u1'])  # u1 !-> u1 ?
        self.assertTrue(u4 in self.g._neighbors['u1'])  # u1 and u4 are neighbors?
        self.assertTrue(u1 in self.g._neighbors['u4'])  # u4 and u1 are neighbors?

        # Add edge with two new Vertex objects.
        self.g.addEdge( Vertex('u5', 'E'), Vertex('u6', 'F') )
        u5 = self.g._vertices['u5']
        u6 = self.g._vertices['u6']

        self.assertTrue(u6 in self.g._edges['u5'])      # u5 -> u6 ?
        self.assertTrue(u5 not in self.g._edges['u6'])  # u6 !-> u5 ?
        self.assertTrue(u5 in self.g._neighbors['u6'])  # u5 and u6 are neighbors?
        self.assertTrue(u6 in self.g._neighbors['u5'])  # u6 and u5 are neighbors?
    
        # Make sure the vertex degrees were updated.
        self.assertEquals(self.g._vertices['u1'].degree, 3)
        self.assertEquals(self.g._vertices['u2'].degree, 1)
        self.assertEquals(self.g._vertices['u3'].degree, 1)
        self.assertEquals(self.g._vertices['u4'].degree, 1)
        self.assertEquals(self.g._vertices['u5'].degree, 1)
        self.assertEquals(self.g._vertices['u6'].degree, 1)

    # =========================================================================
    def testDeleteEdge(self):
        # Referencing non-existing vertices should return False
        self.assertFalse(self.g.deleteEdge('aaa', 'bbb'))

        # Build A->B and B->A
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
        self.assertTrue(u2 in self.g._neighbors['u1'])

        # Both vertex degrees should be decremented.
        self.assertEquals(u1.degree, 1)
        self.assertEquals(u2.degree, 1)

        # Delete the last edge between u1 and u2.
        self.assertTrue(self.g.deleteEdge('u2', 'u1'))
        self.assertTrue(u1 not in self.g._edges['u2'])  # edge is gone ?
        self.assertFalse(u1 in self.g._neighbors['u2']) # no longer neighbors ?
        self.assertFalse(u2 in self.g._neighbors['u1'])
        self.assertEquals(u1.degree, 0)                 # no neighbors at all ?
        self.assertEquals(u2.degree, 0)

    # =========================================================================
    def testDeleteVertex(self):
        # Deleting a non-existing vertex returns None.
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

    # =========================================================================
    def testEdgesProperty(self):
        # Build u1->u2, u2->u3
        self.g.addEdge(Vertex('u1'), Vertex('u2'))
        self.g.addEdge('u2', Vertex('u3'))

        # Make sure that edges returns u1->u2 and u2->u3
        for e in self.g.edges:
            if e[0].id == 'u1':
                self.assertEquals(e[1].id, 'u2')
            elif e[0].id == 'u2':
                self.assertEquals(e[1].id, 'u3')
            else:
                self.assertFalse(True)

    # =========================================================================
    def testFindVertex(self):
        u1 = self.g.addVertex(Vertex('u1', 'A', 1))
        self.assertIsNone(self.g.findVertex('X'))       # vertex X does not exist?
        self.assertIsNone(self.g.findVertex('A2'))      # vertex A2 does not exist?
        self.assertEqual(self.g.findVertex('A1'), u1)   # vertex A1 does exist?

    # =========================================================================
    def testHasEdgeBetweenVertices(self):
        # Build u0 -> u1 -> u2
        self.g.addEdge(Vertex('u0', 'A'), Vertex('u1', 'B'))
        self.g.addEdge('u1', Vertex('u2', 'C'))

        self.assertTrue(self.g.hasEdgeBetweenVertices('u0','u1'))   # should be true
        self.assertFalse(self.g.hasEdgeBetweenVertices('u0','u2'))  # should be false
        self.assertFalse(self.g.hasEdgeBetweenVertices('XX','XX'))  # non-existent vertices
        self.assertFalse(self.g.hasEdgeBetweenVertices('u0','XX'))  # non-existent vertex
        
    # =========================================================================
    def testLabelsProperty(self):
        self.g.addVertex(Vertex('u1', 'A'))
        self.g.addVertex(Vertex('u2', 'B'))
        self.g.addVertex(Vertex('u3', 'C'))

        labels = self.g.labels
        self.assertEquals(len(labels), 3)
        self.assertTrue('A' in labels)		
        self.assertTrue('B' in labels)		
        self.assertTrue('C' in labels)		

    # =========================================================================
    def testNamesProperty(self):
        self.g.addVertex(Vertex('u1', 'A', 1))
        self.g.addVertex(Vertex('u2', 'B', 2))
        self.g.addVertex(Vertex('u3', 'C', 3))

        names = self.g.names
        self.assertEquals(len(names), 3)
        self.assertTrue('A1' in names)		
        self.assertTrue('B2' in names)		
        self.assertTrue('C3' in names)		
    
    # =========================================================================
    def testNumVertices(self):
        self.assertEquals(self.g.numVertices, 0)    # empty graph has no vertices

        a = self.g.addVertex(Vertex('u1'))
        self.assertEquals(self.g.numVertices, 1)    # one vertex

        self.g.addVertex(Vertex('u2', 'B', 2))
        self.assertEquals(self.g.numVertices, 2)    # two vertices

    # =========================================================================
    def testVerticesProperty(self):
        self.assertEquals( len(self.g.vertices), 0 ) # empty graph has no vertices

        u1 = Vertex('u1')   # add three vertices
        u2 = Vertex('u2')
        u3 = Vertex('u3')
        self.g.addVertex(u1)
        self.g.addVertex(u2)
        self.g.addVertex(u3)

        vertices = self.g.vertices
        self.assertEquals(len(vertices), 3)
        self.assertTrue(u1 in vertices)		
        self.assertTrue(u2 in vertices)		
        self.assertTrue(u3 in vertices)			
        
    # =========================================================================
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
