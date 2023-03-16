"""
Vertex.py - A vertex in a graph.
Robert Adams (d.robert.adams@gmail.com)
"""

class Vertex(object):
    """
    A simple representation of a vertex in a graph.  A vertex has an id,
    optional string labels, and optional number. A vertex also has a degree, but it isn't
    automatically updated. Normally, Graph does that as a Vertex is added to
    the graph.
    """

    def __init__(self, id:str, label:str or list=None, number:int=None):
        """
        Builds a vertex with the given id (and optional label and number).
        Inputs:
            * id - vertex id (string)
            * label - optional vertex label (string or list of strings)
            * number - optional vertex number (int)
        Outputs: n/a
        """
        self.id    = id
        self.label = label
        self.number = number
        self.degree = 0      # used by Graph
        self.candidates = [] # used for Graph.search

    # =========================================================================
    def hasLabel(self, label:str or list) -> bool:
        """
        Returns true if this vertex has the given label. If a list of labels
        if given, then this method returns true if at least one of this vertex's
        labels appears in the list.
        """
        if self.label is None:
            return False
        
        if isinstance(label, str):
            return label in self.label
        else:
            for l in label:
                if l in self.label:
                    return True
        
        return False
    
    # =========================================================================
    @staticmethod
    def makeName(label:str or list=None, number:int=None) -> str:
        name = ''

        # Attach all the labels.
        if label is not None:
            if isinstance(label, str):
                name += label
            else:
                for l in label:
                    name += l

        # Attach the number, if there is one.
        if number is not None:
            name += number
       
        # If there is no label or number, return "None".
        if len(name) == 0:
            name = 'None'

        return name   
    
    # =========================================================================
    def name(self) -> str:
        """
        Returns the "name" of this vertex, which is simply the concatenation of
        the label (or all the labels if "label" is a list) and number. Note this 
        is different than __str__ which is mostly used for debugging.
        """
        return Vertex.makeName(self.label, self.number)

    # =========================================================================
    def __str__(self) -> str:
        """
        Returns self as a string of the form \"id,label,number\"
        """
        return '"%s,%s,%s"' % (self.id, 
                              str(self.label) if self.label is not None else "", 
                              str(self.number) if self.number is not None else "")
