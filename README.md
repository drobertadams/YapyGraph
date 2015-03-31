# Yet Another Python Graph Implementation

A relatively simple Python graph. Besides the basic graph creation methods this one also performs subgraph searching.

## Package Contents

`Vertex.py` is a class that represents a simple vertex. It stores a unique vertex id, an optional string label, an optional numeric identifier, and the total degree (in-degree + out-degree) of the vertex. Thus vertices can be identified by the tuple `<ID, LABEL, NUMBER>` as in `<3, 'A', 1>`. The concatenation of the label and number is called a vertex's "name". So in the example above, the "name" would be "A1".

`Graph.py` is the graph class itself. Besides methods to add/delete vertices and edges, it also has methods to query the graph for vertices matching a given label, as well as a subgraph search method.

## Unit Testing

Unit tests are located in `tests`. Run `nosetests` to run all the unit tests.