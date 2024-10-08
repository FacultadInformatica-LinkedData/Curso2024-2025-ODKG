#   [markdown]
# **Task 09: Data linking**

#  
#!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2024-2025/master/Assignment4/course_materials/"

#  
from rdflib import Graph, Namespace, Literal, URIRef
g1 = Graph()
g2 = Graph()
g3 = Graph()
g1.parse(github_storage+"rdf/data03.rdf", format="xml")
g2.parse(github_storage+"rdf/data04.rdf", format="xml")

#   [markdown]
# Busca individuos en los dos grafos y enlázalos mediante la propiedad OWL:sameAs, inserta estas coincidencias en g3. Consideramos dos individuos iguales si tienen el mismo apodo y nombre de familia. Ten en cuenta que las URI no tienen por qué ser iguales para un mismo individuo en los dos grafos.

#  
from rdflib.plugins.sparql import prepareQuery
from rdflib import FOAF, RDF
from rdflib.namespace import OWL

ns1 = Namespace("http://data.three.org#")
ns2 = Namespace("http://data.four.org#")
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")

for s,p,o in g1.triples((None,RDF.type,ns1.Person)):
    for s1,p1,o1 in g1.triples((s,VCARD.FN,None)):
        for s_g2,p_g2,o_g2 in g2.triples((None,RDF.type,ns2.Person)):
            for s1_g2,p1_g2,o1_g2 in g2.triples((s_g2,VCARD.FN,None)):
                if o1==o1_g2:
                    g3.add((s1,OWL.sameAs,s1_g2))

print("Linking graph")
for s,p,o in g3.triples((None,None,None)):
    print(s,p,o)



