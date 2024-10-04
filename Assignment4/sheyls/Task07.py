# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1u1lOXDR3qQHYLFIcrLsw6zbrEa784fmE

**Task 07: Querying RDF(s)**
"""

#!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2024-2025/master/Assignment4/course_materials"

"""First let's read the RDF file"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

"""**TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**"""

query = """
    SELECT ?subclass
    WHERE {
        ?subclass rdfs:subClassOf ns:LivingThing .
    }
"""

result = g.query(query)

for row in result:
    print(f"Subclass: {row.subclass}")

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

query = """
    SELECT DISTINCT ?individual
    WHERE {
        {
            ?individual rdf:type ns:Person .
        } UNION {
            ?subclass rdfs:subClassOf* ns:Person .
            ?individual rdf:type ?subclass .
        }
    }
"""

result = g.query(query)

for row in result:
    print(f"{row.individual}")

"""**TASK 7.3: List all individuals of just "Person" or "Animal". You do not need to list the individuals of the subclasses of person (in SPARQL only)**

"""

query_7_3 = """
  SELECT DISTINCT ?individual
  WHERE {
      {
          ?individual rdf:type ns:Person .
      }
      UNION {
          ?individual rdf:type ns:Animal .
      }
  }
"""

results_7_3 = g.query(query_7_3)

print("Individuals of Person or Animal")
for row in results_7_3:
    print(row.individual)

"""**TASK 7.4:  List the name of the persons who know Rocky (in SPARQL only)**"""

query_7_4_final = """
  SELECT ?person
  WHERE {
      ?person foaf:knows ns:RockySmith .
      ?person rdf:type ?type .
      ?type rdfs:subClassOf* ns:Person .
  }
"""

results_7_4_final = g.query(query_7_4_final)

print("Names of individuals who know Rocky:")
for row in results_7_4_final:
    print(row.person)

"""**Task 7.5: List the name of those animals who know at least another animal in the graph (in SPARQL only)**"""

query_7_5 = """
  SELECT DISTINCT ?animal
  WHERE {
      ?animal rdf:type ns:Animal .

      # Buscar si conocen a otro animal
      ?animal foaf:knows ?otherAnimal .
      ?otherAnimal rdf:type ns:Animal .
  }
"""

results_7_5 = g.query(query_7_5)

print("TASK 7.5: Names of animals who know at least another animal")
for row in results_7_5:
    print(row.animal)

"""**Task 7.6: List the age of all living things in descending order (in SPARQL only)**"""

query_7_6 = """
  SELECT ?livingThing ?age
  WHERE {
      # Buscar todos los seres vivos (LivingThing)
      ?livingThing rdf:type ?type .
      ?type rdfs:subClassOf* ns:LivingThing .

      # Obtener la edad de esos seres vivos
      ?livingThing foaf:age ?age .
  }
  ORDER BY DESC(?age)
"""

results_7_6 = g.query(query_7_6)

print("\nTASK 7.6: Ages of living things in descending order")
for row in results_7_6:
    print(row.age, row.livingThing)