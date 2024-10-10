# -*- coding: utf-8 -*-
"""Task08.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/10D7bovCgWqzryjdzQgLR828j1ArRa5tu

**Task 08: Completing missing data**
"""

!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2024-2025/master/Assignment4/course_materials"

from rdflib import Graph, Namespace, Literal, URIRef
g1 = Graph()
g2 = Graph()
g1.parse(github_storage+"/rdf/data01.rdf", format="xml")
g2.parse(github_storage+"/rdf/data02.rdf", format="xml")

"""Tarea: lista todos los elementos de la clase Person en el primer grafo (data01.rdf) y completa los campos (given name, family name y email) que puedan faltar con los datos del segundo grafo (data02.rdf). Puedes usar consultas SPARQL o iterar el grafo, o ambas cosas."""

# TO DO
from rdflib.plugins.sparql import prepareQuery

d = Namespace("http://data.org#")
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")

q1 = prepareQuery('''
  SELECT ?Subject ?Given ?Family ?Email WHERE {
    ?Subject rdf:type d:Person.
    OPTIONAL {?Subject vcard:Family ?Family}.
    OPTIONAL {?Subject vcard:Given ?Given}.
    OPTIONAL {?Subject vcard:EMAIL ?Email}.
  }
  ''',
  initNs={'d': d, 'vcard': vcard}
)

r2_results = g2.query(q1)

for r1 in g1.query(q1):
  for r2 in r2_results:
    if r1.Subject == r2.Subject:
      if r1.Given is None and r2.Given:
        g1.add((r1.Subject, vcard.Given, r2.Given))
      if r1.Family is None and r2.Family:
        g1.add((r1.Subject, vcard.Family, r2.Family))
      if r1.Email is None and r2.Email:
        g1.add((r1.Subject, vcard.EMAIL, r2.Email))

# Visualize the results
for r in g1.query(q1):
  print(r.Subject, r.Given, r.Family, r.Email)
print("-----------")
for r in g2.query(q1):
  print(r.Subject, r.Given, r.Family, r.Email)