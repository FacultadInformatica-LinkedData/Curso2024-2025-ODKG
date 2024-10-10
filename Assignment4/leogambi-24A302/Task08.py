#   [markdown]
# **Task 08: Completing missing data**

#  
#!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2024-2025/master/Assignment4/course_materials"

#  
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS
g1 = Graph()
g2 = Graph()
g1.parse(github_storage+"/rdf/data01.rdf", format="xml")
g2.parse(github_storage+"/rdf/data02.rdf", format="xml")

#   [markdown]
# Tarea: lista todos los elementos de la clase Person en el primer grafo (data01.rdf) y completa los campos (given name, family name y email) que puedan faltar con los datos del segundo grafo (data02.rdf). Puedes usar consultas SPARQL o iterar el grafo, o ambas cosas.

#  
ns = Namespace("http://data.org#")
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")

for s,p,o in g1.triples((None,  RDF.type , ns.Person)):
  for s1,p1,o1 in g2.triples((s,vcard.Given, None )):
    g1.add((s,vcard.Given,o1))
  for s1,p1,o1 in g2.triples((s,vcard.Family, None )):
    g1.add((s,vcard.Family,o1))
  for s1,p1,o1 in g2.triples((s,vcard.EMAIL,None)):
    g1.add((s,vcard.EMAIL,o1))

print("Complete graph")
for s,p,o in g1.triples((None, RDF.type , ns.Person)):
  for s1,p1,o1 in g1.triples((s, None, None)):
    print(s,p1,o1)

#  
from rdflib import Graph, Namespace, RDF, Literal
from rdflib.namespace import FOAF

# Create namespaces for the graphs
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")

# Bind namespaces
g1.namespace_manager.bind('vcard', vcard)
g2.namespace_manager.bind('vcard', vcard)

#  
def complete_person_data(person, g1, g2):
    # Look for the person in g2 based on the URI
    for person2 in g2.subjects(RDF.type, FOAF.Person):
        if person == person2:
            # Complete missing Given name
            given_name_g1 = g1.value(person, vcard.Given)
            given_name_g2 = g2.value(person2, vcard.Given)
            if not given_name_g1 and given_name_g2:
                g1.add((person, vcard.Given, given_name_g2))

            # Complete missing Family name
            family_name_g1 = g1.value(person, vcard.Family)
            family_name_g2 = g2.value(person2, vcard.Family)
            if not family_name_g1 and family_name_g2:
                g1.add((person, vcard.Family, family_name_g2))

            # Complete missing EMAIL
            email_g1 = g1.value(person, vcard.EMAIL)
            email_g2 = g2.value(person2, vcard.EMAIL)
            if not email_g1 and email_g2:
                g1.add((person, vcard.EMAIL, email_g2))


#  
for person in g1.subjects(RDF.type, FOAF.Person):
    complete_person_data(person, g1, g2)

# Print the completed data from graph g1
for s, p, o in g1:
    print(s, p, o)



