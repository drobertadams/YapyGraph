# Yet Another Python Graph Implementation

YapyGraph is a relatively simple directed graph implemented in Python. Besides the basic graph creation methods this one also performs subgraph searching.

## Vertex Class

`Vertex.py` is the class that represents a simple vertex. Properties include: 

* `id` - the vertex identifier. Uniqueness isn't enforced by Vertex.
* `label` - an optional string label for the vertex (for those applications that need to assign string labels vertices)
* `number` - an option number for the vertex (for those applications that need to assign numeric identifiers to vertices)
* `degree` - the total degree (in-degree + out-degree). The Graph class maintains this.

Only one method is available. Besides this, a Vertex doesn't "do" anything.

* `name()` - returns the "name" of the vertex. The "name" is defined as the concatenation of the label and number.

## Graph Class

`Graph.py` defines a directed graph class. Methods include:

* `__init__` - constructor that builds an empty graph
* `addEdge` - adds an edge between two vertices (either new Vertex objects, or existing vertex ids)
* `addVertex` - adds a new vertex, if the vertex id doesn't already exist
* `deleteEdge` - removes the edge between the vertices with the given vertex ids
* `deleteVertex` - deletes the vertex with the given id, along with all edges connected to it
* `edges` - iterates over all edges, returning (Vertex,Vertex) tuples
* `findVertex` - returns the first Vertex that has the given name, or None
* `hasEdgeBetweenVertices` - returns true if an edge exists between vertices with the given ids
* `labels` - iterates over all labels in the graph
* `names` - iterates over all names in the graph
* `numVertices` - returns the number of vertices
* `__rep__` - returns a [dot](http://www.graphviz.org/content/dot-language) representation of the graph
* `search` - searches for every instances of a given subgraph
* `vertices` - returns a list of vertices

## Unit Testing

Unit tests are located in `tests`. Run `nosetests` to run all the unit tests.

nosetests --with-path=.. tests/testGraph.py

# Setup

1. `git clone` this repo
2. Create a virtual environment: `python3 -m venv PATH_TO_YAPYGRAPH`
3. `cd PATH_TO_YAPYGRAPH`
4. "Activate" the venv: `source bin/activate`
5. Install nose: `pip install nose`
6. Install pathmunge for nose: `pip install nose-pathmunge`