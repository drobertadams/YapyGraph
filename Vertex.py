"""
Vertex.py - A vertex in a graph.
Robert Adams (d.robert.adams@gmail.com)
"""

class Vertex(object):
    """
    A simple represention of a vertex in a graph.  A vertex has an id, and an
    optional label and number. A vertex also has a degree, but it isn't
    automatically updated. Normally, Graph does that as a Vertex is added to
    the graph.
    """

    def __init__(self, id, label=None, number=None):
        """
        Builds a vertex with the given id (and optional label and number).
        Inputs:
            * id - vertex id (string)
            * label - optional vertex label (string)
            * number - optional vertex number (int)
        Outputs: n/a
        """
        self.id    = id
        self.label = label
        self.number = number
        self.degree = 0      # used by Graph
        self.candidates = [] # used for Graph.search

    @property
    def name(self):
        if self.label is None and self.number is None:
            return ''
        if self.number is None:
            return self.label
        elif self.label is None:
            return str(self.number)
        else:
            return '%s%s' % (self.label, self.number)

    def __repr__(self):
        return str(self)

    def __str__(self):
        """
        Returns self as a string.
        """
        return '<%s,%s%s>' % (self.id, self.label, self.number if self.number is not None else "")
