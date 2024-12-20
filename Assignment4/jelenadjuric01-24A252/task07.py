# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mDEbp9sFq8aYsGfwc-l8YIJedSoipQaj

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
for s,p,o in g:
  print(s,p,o)

"""**TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**"""

# TO DO
ns = Namespace("http://somewhere#")
classes = set()
classes.add(ns.LivingThing)
while True:
    new_classes = set()
    for item in classes:
        for s, p, o in g.triples((None, RDFS.subClassOf, item)):
            new_classes.add(s)
    if not new_classes.difference(classes):
        break
    classes.update(new_classes)
print(classes)
# Visualize the results
from rdflib.plugins.sparql import prepareQuery
q1 = prepareQuery('''
  SELECT ?Subject WHERE {
    ?Subject rdfs:subClassOf* ns:LivingThing.
  }
  ''',
  initNs = { "rdfs": RDFS, "ns":ns}
)
for r in g.query(q1):
  print(r)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

# TO DO
classes.clear()
classes.add(ns.Person)
while True:
    new_classes = set()
    for item in classes:
        for s, p, o in g.triples((None, RDFS.subClassOf, item)):
            new_classes.add(s)
    if not new_classes.difference(classes):
        break
    classes.update(new_classes)
for s in classes:
  for s1,p1,o1 in g.triples((None,RDF.type,s)):
    print(s1)
q1 = prepareQuery('''
  SELECT ?instance WHERE {
    ?Subject rdfs:subClassOf* ns:Person.
    ?instance a ?Subject
  }
  ''',
  initNs = { "rdfs": RDFS, "ns":ns}
)
for r in g.query(q1):
  print(r)
# Visualize the results

"""**TASK 7.3: List all individuals of just "Person" or "Animal". You do not need to list the individuals of the subclasses of person (in SPARQL only)**

"""

# TO DO
q1 = prepareQuery('''
  SELECT ?instance WHERE {
    {{?instance a ns:Person. }
    UNION
    {?instance a ns:Animal}
    }
  }
  ''',
  initNs = {  "ns":ns}
)
for r in g.query(q1):
  print(r)
# Visualize the results

"""**TASK 7.4:  List the name of the persons who know Rocky (in SPARQL only)**"""

# TO DO
from rdflib.namespace import FOAF
q1 = prepareQuery('''
  SELECT ?instance WHERE {
    ns:RockySmith foaf:knows ?instance.

  }
  ''',
  initNs = {  "ns":ns,"foaf":FOAF}
)
for r in g.query(q1):
  print(r)
# Visualize the results

"""**Task 7.5: List the name of those animals who know at least another animal in the graph (in SPARQL only)**"""

# TO DO
q1 = prepareQuery('''
  SELECT ?instance WHERE {
    ?instance1 foaf:knows ?instance.
    ?instance1 a ns:Animal .
    ?instance a ns:Animal .
    filter (?instance != ?instance1)

  }
  ''',
  initNs = {  "ns":ns,"foaf":FOAF}
)
for r in g.query(q1):
  print(r)
# Visualize the results

"""**Task 7.6: List the age of all living things in descending order (in SPARQL only)**"""

# TO DO
q1 = prepareQuery('''
  SELECT ?instance ?age WHERE {
    ?Subject rdfs:subClassOf* ns:LivingThing.
    ?instance a ?Subject .
    ?instance foaf:age ?age
  }
  order by desc(?age)
  ''',
  initNs = {  "ns":ns,"foaf":FOAF}
)
for r in g.query(q1):
  print(r)
# Visualize the results