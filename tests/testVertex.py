import unittest

from PGC.Graph.Graph import Graph
from PGC.Graph.Vertex import Vertex

class TestVertexClass(unittest.TestCase):

    def testConstructorWithLabel(self):
        """Building a vertex with an id and label should store both."""
        v = Vertex('v1', 'label')
        self.assertTrue(v.id == 'v1')
        self.assertTrue(v.label == 'label')

    def testConstructorWithoutLabel(self):
        """Building a vertex with only an id should have None for the label."""
        v = Vertex('v1')
        self.assertTrue(v.id == 'v1')
        self.assertTrue(v.label is None)

if __name__ == '__main__':
    unittest.main()
