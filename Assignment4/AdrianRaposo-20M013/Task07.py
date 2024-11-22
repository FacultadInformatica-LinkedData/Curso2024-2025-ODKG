# %% [markdown]
# **Task 07: Querying RDF(s)**

# %%
#!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2024-2025/master/Assignment4/course_materials"

# %% [markdown]
# First let's read the RDF file

# %%
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

# %% [markdown]
# **TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**

# %%
#The namespaces
ns = Namespace("http://somewhere#")
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")

"""**TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**"""

# TO DO

subclasses = []

# Iterate using RDFLib over all subclasses of ns.LivingThing
for subclass in g.subjects(RDFS.subClassOf, ns.LivingThing):
    subclasses.append(subclass)


# SPARQL query to find subclasses of LivingThing
q1 = """
PREFIX ns: <http://somewhere#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?subclass WHERE {
    ?subclass rdfs:subClassOf ns:LivingThing .
}
"""



# Visualize the results
print("Subclasses of LivingThing using RDFLib:")
for sc in subclasses:
    print(sc)

print("Subclasses of LivingThing using SPARQL:")
for row in g.query(q1):
    print(row.subclass)   

#for r in g.query(q1):
#  print(r)

# %% [markdown]
# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**
# 

# %%
# TO DO

# Function to get all subclasses recursively
def get_subclasses(graph, class_uri):
    subclasses = set()
    for subclass in graph.subjects(RDFS.subClassOf, class_uri):
        subclasses.add(subclass)
        subclasses.update(get_subclasses(graph, subclass))
    return subclasses

# Get all subclasses of Person (including Person itself)
all_person_classes = get_subclasses(g, ns.Person)
all_person_classes.add(ns.Person)

# Get all individuals of Person and its subclasses
individuals = set()
for person_class in all_person_classes:
    for individual in g.subjects(RDF.type, person_class):
        individuals.add(individual)

# SPARQL query to find individuals of Person and its subclasses
q2 = """
PREFIX ns: <http://somewhere#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?individual WHERE {
    ?individual rdf:type ?class .
    ?class rdfs:subClassOf* ns:Person .
}
"""

# Visualize the results
print("Individuals of Person (including subclasses) using RDFLib:")
for ind in individuals:
    print(ind)

print("Individuals of Person (including subclasses) using SPARQL:")
for row in g.query(q2):
    print(row.individual)



# %% [markdown]
# **TASK 7.3: List all individuals of just "Person" or "Animal". You do not need to list the individuals of the subclasses of person (in SPARQL only)**
# 

# %%
# TO DO
q3 = """
PREFIX ns: <http://somewhere#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT DISTINCT ?individual WHERE {
    { ?individual rdf:type ns:Person . }
    UNION
    { ?individual rdf:type ns:Animal . }
}
"""
# Visualize the results

print("Individuals of Person or Animal (excluding subclasses) using SPARQL:")
for row in g.query(q3):
    print(row.individual)

# %% [markdown]
# **TASK 7.4:  List the name of the persons who know Rocky (in SPARQL only)**

# %%
# TO DO
from rdflib import FOAF
g.namespace_manager.bind('foaf', FOAF)

# SPARQL query to find names of persons who know Rocky
q4 = """
PREFIX ns: <http://somewhere#>
PREFIX vcard: <http://www.w3.org/2001/vcard-rdf/3.0/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT DISTINCT ?fullName WHERE {
    ?person foaf:knows ?someone .
    ?someone vcard:Given ?name .
    FILTER(?name = "Rocky") .
    ?person rdf:type ns:Person .
    ?person vcard:FN ?fullName
}
"""

# Visualize the results
print("Names of persons who know Rocky:")
for row in g.query(q4):
    print(row.fullName)


# %% [markdown]
# **Task 7.5: List the name of those animals who know at least another animal in the graph (in SPARQL only)**

# %%
# TO DO
q5 = """
PREFIX ns: <http://somewhere#>
PREFIX vcard: <http://www.w3.org/2001/vcard-rdf/3.0/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT DISTINCT ?animal WHERE {
    ?animal rdf:type ns:Animal .
    ?animal foaf:knows ?otherAnimal .
    ?otherAnimal rdf:type ns:Animal .
    FILTER(?animal != ?otherAnimal) .
}
"""



# Visualize the results
print("Names of animals who know at least another animal:")
for row in g.query(q5):
    print(row.animal)

# %% [markdown]
# **Task 7.6: List the age of all living things in descending order (in SPARQL only)**

# %%
# TO DO
q6 = """
PREFIX ns: <http://somewhere#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?livingThing ?age WHERE {
    ?livingThing rdf:type ?class .
    ?class rdfs:subClassOf* ns:LivingThing .
    ?livingThing foaf:age ?age .
} ORDER BY DESC(?age)
"""


# Visualize the results
print("Ages of all living things in descending order:")
for row in g.query(q6):
    print(f"{row.livingThing} : {row.age}")


