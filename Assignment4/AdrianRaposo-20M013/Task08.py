# %% [markdown]
# **Task 08: Completing missing data**

# %%
#!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2024-2025/master/Assignment4/course_materials"

# %%
from rdflib import Graph, Namespace, Literal, URIRef
g1 = Graph()
g2 = Graph()
g1.parse(github_storage+"/rdf/data01.rdf", format="xml")
g2.parse(github_storage+"/rdf/data02.rdf", format="xml")

# %% [markdown]
# Tarea: lista todos los elementos de la clase Person en el primer grafo (data01.rdf) y completa los campos (given name, family name y email) que puedan faltar con los datos del segundo grafo (data02.rdf). Puedes usar consultas SPARQL o iterar el grafo, o ambas cosas.

# %%

from rdflib.namespace import RDF, RDFS
#  Namespaces
VCARD = Namespace('http://www.w3.org/2001/vcard-rdf/3.0#')
DATA = Namespace('http://data.org#')


# Print the persons with their properties
print("BEFORE UPDATING PROPERTIES")
for person in g1.subjects(RDF.type, DATA.Person):
    print(f"Person: {person}")
    for prop in [VCARD.Given, VCARD.Family, VCARD.EMAIL]:
        values = list(g1.objects(person, prop))
        prop_name = prop.split('#')[-1]
        if values:
            for value in values:
                print(f"  {prop_name}: {value}")
        else:
            print(f"  {prop_name}: [Not available]")
    print()
# Iterate over all persons in g1
for person in g1.subjects(RDF.type, DATA.Person):
    # List of properties to check
    properties = [VCARD.Given, VCARD.Family, VCARD.EMAIL]
    for prop in properties:
        # Check if the property is missing in g1
        if not g1.value(person, prop):
            # Try to get the property from g2
            value = g2.value(person, prop)
            if value:
                # Add the missing property to g1
                g1.add((person, prop, value))

# Print the updated persons with their properties
print("AFTER UPDATING PROPERTIES")
for person in g1.subjects(RDF.type, DATA.Person):
    print(f"Person: {person}")
    for prop in [VCARD.Given, VCARD.Family, VCARD.EMAIL]:
        values = list(g1.objects(person, prop))
        prop_name = prop.split('#')[-1]
        if values:
            for value in values:
                print(f"  {prop_name}: {value}")
        else:
            print(f"  {prop_name}: [Not available]")
    print()


