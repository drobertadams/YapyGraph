import unittest

from YapyGraph.Vertex import Vertex

class TestVertexClass(unittest.TestCase):

    def testConstructorLabelNumber(self):
        """Building a vertex with an id, label, and number should store all."""
        v = Vertex('v1', 'label', 1)
        self.assertEqual(v.id, 'v1')
        self.assertEqual(v.label, 'label')
        self.assertEqual(v.number, 1)
        self.assertEqual(v.name, 'label1')

    def testConstructorNoLabelNoNumber(self):
        """Building a vertex with only an id should have None for the label,
        and number."""
        v = Vertex('v1')
        self.assertEqual(v.id, 'v1')
        self.assertIsNone(v.label)
        self.assertIsNone(v.number)
        self.assertEqual(v.name, '')

    def testConstructorLabelNoNumber(self):
        v = Vertex('v1', 'label')
        self.assertEqual(v.id, 'v1')
        self.assertEqual(v.label, 'label')
        self.assertIsNone(v.number)
        self.assertEqual(v.name, 'label')

    def testConstructorNoLabelNumber(self):
        v = Vertex('v1', None, 1)
        self.assertEqual(v.id, 'v1')
        self.assertIsNone(v.label)
        self.assertEqual(v.number, 1)
        self.assertEqual(v.name, '1')

    def testMakeName(self):
        name = Vertex.makeName('A', 1)
        self.assertEqual(name, 'A1')

if __name__ == '__main__':
    unittest.main()
