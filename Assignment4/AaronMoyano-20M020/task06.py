"""
**Task 06: Modifying RDF(s)**
"""
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2024-2025/master/Assignment4/course_materials"

"""Read the RDF file as shown in class"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
from rdflib.plugins.sparql import prepareQuery
from rdflib import FOAF

g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example5.rdf", format="xml")

"""Create a new class named Researcher"""

ns = Namespace("http://somewhere#")
g.add((ns.Researcher, RDF.type, RDFS.Class))

""" **TASK 6.1: Create new classes for "School" and "University. Add an rdfs:label in Spanish"** """
# TO DO
# Create Class "School"
g.add((ns.School, RDF.type, RDFS.Class))
g.add((ns.School, RDFS.label, Literal("Escuela", lang="es")))

# Create Class "University"
g.add((ns.University, RDF.type, RDFS.Class))
g.add((ns.University, RDFS.label, Literal("Universidad", lang="es")))

# Visualize the results
q1 = prepareQuery('''SELECT ?Subject WHERE {
  ?Subject ?Property rdfs:Class.

  FILTER(?Subject=ns:School)
  }

  ''',
  initNs = { "ns": ns,"rdfs":RDFS}
)

print("Results for TASK 6.1:")
for r in g.query(q1):
  print(r)

"""**TASK 6.2: Add "Researcher" as a subclass of "Person"**"""

# TO DO
g.add((ns.Researcher, RDFS.subClassOf, ns.Person))

# Visualize the results
q2 = prepareQuery('''
  SELECT ?Subclass WHERE {
    ?Subclass rdfs:subClassOf ?Superclass .
    FILTER (?Subclass = ns:Researcher && ?Superclass = ns:Person)
  }
  ''',
  initNs = { "ns": ns, "rdfs": RDFS }
)

print("\nResults for TASK 6.2:")
for r in g.query(q2):
  print(r)

"""**TASK 6.3: Create a new individual of Researcher named "Jane Smithers"**"""

# TO DO
g.add((ns.JaneSmithers, RDF.type, ns.Researcher))

# Visualize the results
q3 = prepareQuery('''
  SELECT ?Subject ?Property WHERE {
    ?Subject ?Property ns:Researcher .
  }
  ''',
  initNs = { "ns": ns, "rdf": RDF }
)

print("\nResults for TASK 6.3:")
for r in g.query(q3):
  print(r)

"""**TASK 6.4: Add to the individual JaneSmithers the email address, fullName, given and family names. Use the https://schema.org vocabulary**"""

# TO DO
schema = schema = Namespace("http://schema.org/")

g.add((ns.JaneSmithers, schema.email, Literal("jane.smithers@example.com")))
g.add((ns.JaneSmithers, schema.givenName, Literal("Jane")))
g.add((ns.JaneSmithers, schema.familyName, Literal("Smithers")))
g.add((ns.JaneSmithers, schema.name, Literal("Jane Smithers")))

# Visualize the results
q4 = prepareQuery('''
  SELECT ?Property ?Value WHERE {
    ns:JaneSmithers ?Property ?Value .
    FILTER (?Property IN (schema:email, schema:givenName, schema:familyName, schema:name))
  }
  ''',
  initNs = { "ns": ns, "schema": schema }
)

print("\nResults for TASK 6.4:")
for r in g.query(q4):
  print(r)

"""**TASK 6.5: Add UPM as the university where John Smith works. Use the "https://example.org/ namespace**"""

# TO DO
EX = Namespace("http://example.org/")

g.add((ns.JohnSmith, EX.worksAt, Literal('UPM')))

# Visualize the results
q5 = prepareQuery('''
  SELECT ?Subject WHERE {
    ?Subject EX:worksAt 'UPM'
  }
  ''',
  initNs = { "ns": ns, "schema": schema, "EX": EX }
)

print("\nResults for TASK 6.5:")
for r in g.query(q5):
  print(r)

"""**Task 6.6: Add that Jown knows Jane using the FOAF vocabulary. Make sure the relationship exists.**"""

# TO DO
g.add((ns.JaneSmithers,FOAF.knows,ns.JohnSmith))

# Visualize the results
q6 = prepareQuery('''
  SELECT ?Subject ?Object WHERE {
    ?Subject FOAF:knows ?Object
  }
  ''',
  initNs = { "ns": ns, "FOAF": FOAF }
)

print("\nResults for TASK 6.6:")
for r in g.query(q6):
  print(r)