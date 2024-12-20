# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yPniC8cCIRK0ofpUQK_h0bcNOa4CroCF

**Task 07: Querying RDF(s)**
"""

!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2024-2025/master/Assignment4/course_materials"

"""First let's read the RDF file"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

"""**TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**"""

#with RDFLib
ns = Namespace("http://somewhere#")

for s,p,o in g.triples((None, RDFS.subClassOf, ns.LivingThing)):
  print(s)

# with SPARQL
from rdflib.plugins.sparql import prepareQuery

q1 = prepareQuery('''
  SELECT DISTINCT ?subclass WHERE {
    ?subclass rdfs:subClassOf ns:LivingThing.
  }
  ''',
  initNs = { "ns": ns, "rdfs": RDFS}
)

# Visualize the results
for r in g.query(q1):
    print(r)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

#with RDFLib
subjects = []
for s,p,o in g.triples((None, RDF.type, ns.Person)):
  subjects.append(s)

for s,p,o in g.triples((None, RDFS.subClassOf, ns.Person)):
  subjects.append(s)

final_subjects = set(subjects)
print(final_subjects)
#with SPARQL
q2 = prepareQuery('''
  SELECT DISTINCT ?subject WHERE {
    { ?subject rdf:type ns:Person . }
    UNION
    { ?subject rdf:type ?type .
      ?type rdfs:subClassOf ns:Person .}
  }
  ''',
  initNs = { "ns": ns, "rdf":RDF  ,"rdfs": RDFS}
)

# Visualize the results
for r in g.query(q2):
    print(r)

"""**TASK 7.3: List all individuals of just "Person" or "Animal". You do not need to list the individuals of the subclasses of person (in SPARQL only)**

"""

q3 = prepareQuery('''
  SELECT DISTINCT ?individual WHERE {
    { ?individual rdf:type ns:Person . }
    UNION
    { ?individual rdf:type ns:Animal . }
  }
  ''',
  initNs = { "ns": ns, "rdf":RDF }
)

# Visualize the results
for r in g.query(q3):
    print(r)

"""**TASK 7.4:  List the name of the persons who know Rocky (in SPARQL only)**"""

from rdflib import FOAF
VCARDFN = Namespace("http://www.w3.org/2001/vcard-rdf/3.0/FN")

q4 = prepareQuery('''
  SELECT DISTINCT ?personName
    WHERE {
      ?rocky vcard: ?rockyName .
      FILTER(STRSTARTS(?rockyName, "Rocky"))

      ?person rdf:type ns:Person .
      ?person foaf:knows ?rocky .
      ?person vcard: ?personName
    }
  ''',
  initNs = { "ns": ns, "rdf":RDF, "foaf":FOAF , "vcard":VCARDFN}
)

# Visualize the results
for r in g.query(q4):
    print(r)
"""**Task 7.5: List the name of those animals who know at least another animal in the graph (in SPARQL only)**"""

VCARDGiven = Namespace("http://www.w3.org/2001/vcard-rdf/3.0/Given")

q5 = prepareQuery('''
  SELECT DISTINCT ?animalName
    WHERE {
      ?animal rdf:type ns:Animal .
      ?animal vcard: ?animalName .
      ?animal foaf:knows ?otherAnimal .
      ?otherAnimal rdf:type ns:Animal .
    }
  ''',
  initNs = { "ns": ns, "rdf":RDF, "foaf":FOAF , "vcard":VCARDGiven}
)

# Visualize the results
for r in g.query(q5):
    print(r)

"""**Task 7.6: List the age of all living things in descending order (in SPARQL only)**"""

q6 = prepareQuery('''
  SELECT DISTINCT ?age
    WHERE {
      ?livingThing rdf:type ?type .
      ?type rdfs:subClassOf ns:LivingThing .
      ?livingThing foaf:age ?age
    }
    ORDER BY DESC(?age)
  ''',
  initNs = { "ns": ns, "rdf":RDF, "rdfs": RDFS, "foaf":FOAF }
)

# Visualize the results
for r in g.query(q6):
    print(r)
