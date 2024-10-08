#   [markdown]
# **Task 07: Querying RDF(s)**

#  
#!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2024-2025/master/Assignment4/course_materials"

#   [markdown]
# First let's read the RDF file

#  
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS, FOAF
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

#   [markdown]
# **TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**

#  
# TO DO
# Visualize the results

from rdflib.plugins.sparql import prepareQuery

# Define the SPARQL query to get all subclasses of LivingThing
query = prepareQuery("""
    SELECT ?subclass WHERE {
        ?subclass rdfs:subClassOf <http://somewhere#LivingThing> .
    }
""", initNs={"rdfs": RDFS})

# Execute the query and print results
print("SPARQL")
for row in g.query(query):
    print(row.subclass)

ns = Namespace("http://somewhere#")
print("RDFLib")
for subclass in g.subjects(RDFS.subClassOf, ns.LivingThing):
    print(subclass)

#for r in g.query(q1):
#  print(r)

#   [markdown]
# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**
# 

#  
# TO DO
# Visualize the results

query = prepareQuery("""
    SELECT ?individual WHERE {
        ?individual rdf:type/rdfs:subClassOf* <http://somewhere#Person> .
    }
""", initNs={"rdf": RDF, "rdfs": RDFS})

# Execute the query and print results
print("SPARQL")
for row in g.query(query):
    print(row.individual)

ns = Namespace("http://somewhere#")
print("RDFLib")
for person in g.subjects(RDF.type, ns.Person):
    print(person)

for subclass in g.subjects(RDFS.subClassOf, ns.Person):
    for individual in g.subjects(RDF.type, subclass):
        print(individual)

#   [markdown]
# **TASK 7.3: List all individuals of just "Person" or "Animal". You do not need to list the individuals of the subclasses of person (in SPARQL only)**
# 

#  
# TO DO
# Visualize the results

query = prepareQuery("""
    SELECT ?individual WHERE {
        ?individual rdf:type ?type .
        FILTER(?type IN (<http://somewhere#Person>, <http://somewhere#Animal>))
    }
""", initNs={"rdf": RDF})

# Execute the query and print results
print("SPARQL")
for row in g.query(query):
    print(row.individual)

#   [markdown]
# **TASK 7.4:  List the name of the persons who know Rocky (in SPARQL only)**

#  
# TO DO
# Visualize the results

query = prepareQuery("""
    SELECT ?person WHERE {
        ?person rdf:type/rdfs:subClassOf* <http://somewhere#Person> .
        ?person foaf:knows <http://somewhere#RockySmith> .
    }
""", initNs={"rdf": RDF, "foaf": FOAF})

# Execute the query and print results
print("SPARQL")
for row in g.query(query):
    print(row.person)

#   [markdown]
# **Task 7.5: List the name of those animals who know at least another animal in the graph (in SPARQL only)**

#  
# TO DO
# Visualize the results

vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")

query = prepareQuery("""
    SELECT DISTINCT ?animal ?name WHERE {
        ?animal rdf:type <http://somewhere#Animal> .
        ?animal foaf:knows ?anotherAnimal .
        ?anotherAnimal rdf:type <http://somewhere#Animal> .
        ?animal vcard:FN ?name .
    }
""", initNs={"rdf": RDF, "foaf": FOAF, "vcard": vcard})

# Execute the query and print results
print("SPARQL")
for row in g.query(query):
    print(row.name)

#   [markdown]
# **Task 7.6: List the age of all living things in descending order (in SPARQL only)**

#  
# TO DO
# Visualize the results

vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")

query = prepareQuery("""
    SELECT ?name ?age WHERE {
        ?livingThing vcard:FN ?name .
        ?livingThing <http://xmlns.com/foaf/0.1/age> ?age .
    }
    ORDER BY DESC(?age)
""", initNs={"rdf": RDF, "foaf": FOAF, "vcard": vcard})

# Execute the query and print results
print("SPARQL")
for row in g.query(query):
    print(f"Living Thing: {row.name}, Age: {row.age}")


