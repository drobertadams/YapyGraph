# Yet Another Python Graph Implementation

A relatively simple Python graph. Besides the basic graph creation methods
this one also perform subgraph searching.

## Package Contents

`Vertex.py` is a class that represents a simple vertex. It stores a unique
vertex id, an optional label, and the total degree (in-degree + out-degree) of
the vertex.

`Graph.py` is the graph class itself. Besides methods to add/delete vertices
and edges, it also has methods to query the graph for vertices matching a
given label, as well as a subgraph search method.

## Unit Testing

Unit tests are located in `tests`. Run `nosetests` to run all the unit tests.
