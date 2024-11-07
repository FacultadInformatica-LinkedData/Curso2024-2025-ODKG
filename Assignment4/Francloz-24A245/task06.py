# -*- coding: utf-8 -*-
"""Task06.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nyR-tTtqy8h8yv5vyeslI7oljBQElfoi

**Task 06: Modifying RDF(s)**
"""

github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2024-2025/master/Assignment4/course_materials"

"""Read the RDF file as shown in class"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
from rdflib import FOAF

g = Graph()
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
schema = Namespace("http://schema.org/")
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage + "/rdf/example5.rdf", format="xml")

"""Create a new class named Researcher"""

ns = Namespace("http://somewhere#")
g.add((ns.Researcher, RDF.type, RDFS.Class))
for s, p, o in g:
    print(s, p, o)
print()
"""**TASK 6.1: Create new classes for "School" and "University. Add an rdfs:label in Spanish"**

"""

new_triples = [
    (ns.School, RDF.type, RDFS.Class),  # (namespace.School, rdfs.isType, rdfs.Class)
    (ns.University, RDF.type, RDFS.Class),  # (namespace.School, rdfs.isType, rdfs.Class)
    (ns.School, RDFS.label, Literal("Escuela")),  # (namespace.University, rdfs.label, "Escuela")
    (ns.University, RDFS.label, Literal("Universidad"))  # (namespace.University, rdfs.label, "Universidad")
]

for triple in new_triples:
    g.add(triple)

# Visualize the results
for s, p, o in g:
    print(s, p, o)
print()
"""**TASK 6.2: Add "Researcher" as a subclass of "Person"**"""

new_triples = [
    (ns.Researcher, RDFS.subClassOf, schema.Person),
]

for triple in new_triples:
    g.add(triple)

# TO DO
# Visualize the results
for s, p, o in g:
    print(s, p, o)
print()
"""**TASK 6.3: Create a new individual of Researcher named "Jane Smithers"**"""

new_triples = [
    (ns.JaneSmithers, RDF.type, ns.Researcher),
    (ns.JaneSmithers, RDFS.label, Literal("Jane Smithers")),
]

for triple in new_triples:
    g.add(triple)

# Visualize the results
for s, p, o in g:
    print(s, p, o)
print()
"""**TASK 6.4: Add to the individual JaneSmithers the email address, fullName, given and family names. Use the https://schema.org vocabulary**"""

new_triples = [
    (ns.JaneSmithers, schema.name, Literal("Jane Smithers")),
    (ns.JaneSmithers, schema.email, Literal("jane.smithers@upm.es")),
    (ns.JaneSmithers, schema.givenName, Literal("Jane")),
    (ns.JaneSmithers, schema.familyName, Literal("Smithers")),
]

for triple in new_triples:
    g.add(triple)

# Visualize the results
for s, p, o in g:
    print(s, p, o)
print()

"""**TASK 6.5: Add UPM as the university where John Smith works. Use the "https://example.org/ namespace**"""

# I assume we should use ns for the university, but not the property.
# Thus, using vcard.organization_name, as it is usually done that way.
# If not, we could use ns.worksAt
new_triples = [
    (ns.JohnSmith, vcard.organization_name, ns.UPM),
    # (ns.JohnSmith, vcard.worksAt, ns.UPM),
]

for triple in new_triples:
    g.add(triple)

for s, p, o in g:
    print(s, p, o)

"""**Task 6.6: Add that John knows Jane using the FOAF vocabulary. Make sure the relationship exists.**"""

new_triples = [
    (ns.JohnSmith, FOAF.knows, ns.JaneSmithers),
]

for triple in new_triples:
    g.add(triple)

# Visualize the results
for s, p, o in g:
    print(s, p, o)