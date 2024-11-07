from rdflib import Graph
from rdflib.tools.rdfpipe import parse_and_serialize
rdf_dir = "path/to/rdf/"
file_name = "subset-graph-updated"
g = Graph()
g.parse(rdf_dir + file_name + ".nt")
g.serialize(format="ttl", destination=rdf_dir + file_name + ".ttl")
