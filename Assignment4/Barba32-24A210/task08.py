# -*- coding: utf-8 -*-
"""Task08.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15ZuiS4-rukANyOAm8m7_6xSQtWGIqXlu

**Task 08: Completing missing data**
"""

!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2024-2025/master/Assignment4/course_materials"

from rdflib import Graph, Namespace, Literal, URIRef
g1 = Graph()
g2 = Graph()
g1.parse(github_storage+"/rdf/data01.rdf", format="xml")
g2.parse(github_storage+"/rdf/data02.rdf", format="xml")

print("Visualizar G1: ")
for s, p, o in g1:
  print(s,p,o) # Visualizar el gráfico

print("\nVisualizar G2: ")
for s, p, o in g2:
  print(s,p,o)

"""Tarea: lista todos los elementos de la clase Person en el primer grafo (data01.rdf) y completa los campos (given name, family name y email) que puedan faltar con los datos del segundo grafo (data02.rdf). Puedes usar consultas SPARQL o iterar el grafo, o ambas cosas.

## Primera parte
"""

from rdflib.namespace import RDF, RDFS

dt = Namespace("http://data.org#")
print("Iterar grafo de la clase Person de G1: ")
for s, p, o in g1.triples((None, RDF.type, dt.Person)):
  print(s)

"""## Segunda parte"""

# Segunda parte

VCARD = Namespace('http://www.w3.org/2001/vcard-rdf/3.0#')

print("Comprobar cuales faltan para cada propiedad: ")
propiedades = {"Given name": VCARD.Given,"Family name": VCARD.Family, "email":VCARD.EMAIL}
for propiedad, valor in propiedades.items():
  print("\nComprobación de "+propiedad+" :")
  for s, p, o in g2.triples((None, valor, None)):
    print(s)

"""### Añadir los valores faltantes"""

# Añadir a Harry Potter su Family name.

g2.add((dt.HarryPotter,VCARD.Family,Literal('Potter')))

print("Comprobar los resultados: ")
for s, p, o in g2.triples((None, VCARD.Family, None)):
  print(s)