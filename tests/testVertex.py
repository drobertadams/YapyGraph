import unittest

from YapyGraph.Vertex import Vertex

class TestVertexClass(unittest.TestCase):

    def testConstructorWithLabel(self):
        """Building a vertex with an id, label, and number should store all."""
        v = Vertex('v1', 'label', 1)
        self.assertEqual(v.id, 'v1')
        self.assertEqual(v.label, 'label')
        self.assertEqual(v.number, 1)

    def testConstructorWithoutLabel(self):
        """Building a vertex with only an id should have None for the label,
        and number."""
        v = Vertex('v1')
        self.assertEqual(v.id, 'v1')
        self.assertIsNone(v.label)
        self.assertIsNone(v.number)

if __name__ == '__main__':
    unittest.main()
