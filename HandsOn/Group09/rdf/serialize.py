from rdflib import Graph
g = Graph()
g.parse("knowledge-graph.nt", format="nt")
g.serialize(destination="knowledge-graph.ttl")
