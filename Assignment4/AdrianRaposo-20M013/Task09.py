# %% [markdown]
# **Task 09: Data linking**

# %%
#!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2024-2025/master/Assignment4/course_materials/"

# %%
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, OWL
g1 = Graph()
g2 = Graph()
g3 = Graph()
g1.parse(github_storage+"rdf/data03.rdf", format="xml")
g2.parse(github_storage+"rdf/data04.rdf", format="xml")


# %% [markdown]
# Busca individuos en los dos grafos y enlázalos mediante la propiedad OWL:sameAs, inserta estas coincidencias en g3. Consideramos dos individuos iguales si tienen el mismo apodo y nombre de familia. Ten en cuenta que las URI no tienen por qué ser iguales para un mismo individuo en los dos grafos.

# %%


# Define the vCard namespace
VCARD = Namespace('http://www.w3.org/2001/vcard-rdf/3.0#')

# Create an empty graph for the links
g3 = Graph()

# Bind namespaces
g3.bind('owl', OWL)
g3.bind('vcard', VCARD)

# Create dictionaries to store individuals based on their given name and family name
individuals_g1 = {}
individuals_g2 = {}

def extract_names(graph, individuals_dict):
    for person in graph.subjects(RDF.type, None):
        given_names = list(graph.objects(person, VCARD.Given))
        family_names = list(graph.objects(person, VCARD.Family))
        # If family name is missing, try to extract from FN
        if not family_names:
            fnames = list(graph.objects(person, VCARD.FN))
            if fnames:
                for fn in fnames:
                    names = str(fn).split()
                    if len(names) > 1:
                        family_names = [Literal(names[-1])]
        if given_names and family_names:
            for given in given_names:
                for family in family_names:
                    key = (str(given).strip().lower(), str(family).strip().lower())
                    individuals_dict.setdefault(key, set()).add(person)

# Extract individuals from g1 and g2
extract_names(g1, individuals_g1)
extract_names(g2, individuals_g2)

# Find matches and link them using owl:sameAs
for key in individuals_g1:
    if key in individuals_g2:
        for uri1 in individuals_g1[key]:
            for uri2 in individuals_g2[key]:
                g3.add((uri1, OWL.sameAs, uri2))

# Optionally, print the linked individuals
for s, p, o in g3:
    print(f"{s} owl:sameAs {o}")


