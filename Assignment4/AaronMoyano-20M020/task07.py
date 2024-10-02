"""
**Task 07: Querying RDF(s)**
"""

github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2024-2025/master/Assignment4/course_materials"

"""First let's read the RDF file"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
from rdflib.plugins.sparql import prepareQuery
from rdflib import FOAF

g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

"""**TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**"""

# TO DO
ns = Namespace("http://somewhere#")

# Task 7.1 : SPARQL
q1_sparql = prepareQuery('''
  SELECT ?Subclass WHERE {
    ?Subclass rdfs:subClassOf ns:LivingThing .
  }
  ''',
  initNs={"ns": ns, "rdfs": RDFS}
)

print("Results for TASK 7.1 (SPARQL):")
for r in g.query(q1_sparql):
  print(r)

# Task 7.1: RDFLib
print("\nResults for TASK 7.1 (RDFLib):")
for s, p, o in g.triples((None,RDFS.subClassOf,ns.LivingThing)):
    print(s)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

# TO DO

# Task 7.2: SPARQL
q2_sparql = prepareQuery('''
  SELECT ?Subject WHERE {
    ?Subject rdf:type ?Type .
    ?Type rdfs:subClassOf* ns:LivingThing .
    FILTER(?Type != ns:Animal)
  }
  ''',
  initNs={"ns": ns, "rdfs": RDFS, "rdf": RDF}
)

print("\nResults for TASK 7.2 (SPARQL):")
for r in g.query(q2_sparql):
  print(r)

# Task 7.2: RDFLib
print("\nResults for TASK 7.2 (RDFLib):")
for person_type in g.subjects(RDFS.subClassOf, ns.Person):
    for individual in g.subjects(RDF.type, person_type):
        print(individual)
    for individual in g.subjects(RDF.type, ns.Person): 
        print(individual)

"""**TASK 7.3: List all individuals of just "Person" or "Animal". You do not need to list the individuals of the subclasses of person (in SPARQL only)**
"""

# TO DO
# Task 7.3: SPARQL
q3_sparql = prepareQuery('''
  SELECT ?Subject WHERE {
    ?Subject rdf:type ?Type .
    FILTER(?Type IN (ns:Person, ns:Animal))
  }
  ''',
  initNs={"ns": ns, "rdf": RDF}
)

print("\nResults for TASK 7.3 (SPARQL):")
for r in g.query(q3_sparql):
  print(r)

# Task 7.3: RDFLib
print("\nResults for TASK 7.3 (RDFLib):")
for individual in g.subjects(RDF.type, ns.Person):
    print(individual)
for individual in g.subjects(RDF.type, ns.Animal):
    print(individual)


"""**TASK 7.4:  List the name of the persons who know Rocky (in SPARQL only)**"""

# TO DO
# Task 7.4: SPARQL, added JaneSmith which is a Researcher -> Subclass of Person
q4_sparql = prepareQuery('''
  SELECT ?Subject WHERE {
    ?Subject foaf:knows ns:RockySmith .
    ?Subject rdf:type ?Type .
    ?Type rdfs:subClassOf* ns:Person .
  }
  ''',
  initNs={"ns": ns, "foaf": FOAF}
)

print("\nResults for TASK 7.4 (SPARQL):")
for r in g.query(q4_sparql):
  print(r)

"""**Task 7.5: List the name of those animals who know at least another animal in the graph (in SPARQL only)**"""

# TO DO
q5_sparql = prepareQuery('''
  SELECT DISTINCT ?Subject WHERE {
    ?Subject rdf:type ns:Animal .
    ?Subject foaf:knows ?OtherAnimal .

  }
  ''',
  initNs={"ns": ns, "foaf": FOAF}
)

print("\nResults for TASK 7.5 (SPARQL):")
for r in g.query(q5_sparql):
    print(r)


"""**Task 7.6: List the age of all living things in descending order (in SPARQL only)**"""

# TO DO
q6_sparql = prepareQuery('''
  SELECT ?Subject WHERE {
    ?Object rdf:type ?Type .
    ?Type rdfs:subClassOf* ns:LivingThing .      
    ?Object foaf:age ?Subject .
  }
  ORDER BY DESC(?Subject)
  ''',
  initNs={"ns": ns, "foaf": FOAF}
)

print("\nResults for TASK 7.6 (SPARQL):")
for r in g.query(q6_sparql):
    print(r.Subject)

