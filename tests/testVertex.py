import unittest

from Vertex import Vertex

class TestVertexClass(unittest.TestCase):

    def testConstructorLabelNumber(self):
        v = Vertex('v1', 'label', 1)        # build vertex with everything
        self.assertEqual(v.id, 'v1')        # should get it all back
        self.assertEqual(v.label, 'label')
        self.assertEqual(v.number, 1)

    def testConstructorNoLabelNoNumber(self):
        v = Vertex('v1')                # build vertex with only an id
        self.assertEqual(v.id, 'v1')    # should get the id back
        self.assertIsNone(v.label)      # the rest should return None or empty string
        self.assertIsNone(v.number)

    def testConstructorLabelNoNumber(self):
        v = Vertex('v1', 'label')
        self.assertEqual(v.id, 'v1')
        self.assertIn(v.label, 'label')
        self.assertIsNone(v.number)

        # Try multiple labels.
        v2 = Vertex('v2', ['A', 'B'])
        self.assertTrue(v2.hasLabel('A'))
        self.assertTrue(v2.hasLabel('B'))
        
    def testConstructorNoLabelNumber(self):
        v = Vertex('v1', None, 1)
        self.assertEqual(v.id, 'v1')
        self.assertIsNone(v.label)
        self.assertEqual(v.number, 1)

    def testHasLabel(self):
        # No label.
        v = Vertex('v1')
        self.assertFalse( v.hasLabel('A') )

        # Simple string label.
        v.label = 'A'
        self.assertFalse( v.hasLabel('B') )
        self.assertTrue( v.hasLabel('A') )
        self.assertTrue( v.hasLabel(['B', 'A']) )

        # List of labels.
        v.label = ['A', 'C']
        self.assertFalse( v.hasLabel('B') )
        self.assertTrue( v.hasLabel('A') )
        self.assertTrue( v.hasLabel(['D', 'C']) )

if __name__ == '__main__':
    unittest.main()
