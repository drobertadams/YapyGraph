"""
Vertex.py - A vertex in a graph.
Robert Adams (d.robert.adams@gmail.com)
"""

class Vertex(object):
    """
    A simple represention of a vertex in a graph. 
    A vertex has an id, and an optional label. A vertex also has a degree, 
    but it isn't automatically updated. Normally, Graph does that as a
    Vertex is added to the graph.
    """

    def __init__(self, id, label=None):
        """
        Builds a vertex with the given id (and optional label).
        Inputs:
            * id - vertex id (string)
            * label - optional vertex label (string)
        Outputs: n/a
        """
        self.id = id
        self.label = label
        self.degree = 0

    def __repr__(self):
        return str(self)

    def __str__(self):
        """
        Returns self as a string.
        """
        return '<%s,%s>' % (self.id, self.label)
