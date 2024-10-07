# %% [markdown]
# **Task 07: Querying RDF(s)**

# %%
#!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2024-2025/master/Assignment4/course_materials"

# %% [markdown]
# First let's read the RDF file

# %%
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
from rdflib import FOAF
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

# %% [markdown]
# **TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**

# %%
# TO DO
#RDFLib
ns = Namespace("http://somewhere#")
for s,p,o in g.triples((None, RDFS.subClassOf, ns.LivingThing)):
  print(s)

# SPARQL
from rdflib.plugins.sparql import prepareQuery
q1 = prepareQuery('''
  SELECT DISTINCT ?SubClass WHERE
  {
    ?SubClass rdfs:subClassOf ns:LivingThing .
  }
  ''',
  initNs = { "rdfs": RDFS, "ns": "http://somewhere#" }
)
for r in g.query(q1):
  print(r)

# %% [markdown]
# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**
# 

# %%
# TO DO
#RDFLib
ns = Namespace("http://somewhere#")
for s,p,o in g.triples((None, RDF.type, ns.Person)):
    print(s)

for s,p,o in g.triples((None, RDFS.subClassOf, ns.Person)):
    for s,p,o in g.triples((None, RDF.type, s)):
        print(s)

#SPARQL
q2 = prepareQuery('''
  SELECT DISTINCT ?individual WHERE
  {
    {
      ?individual a ns:Person .
    }
    UNION
    {
      ?subClass rdfs:subClassOf ns:Person .
      ?individual a ?subClass .
    }
  }
  ''',
  initNs = { "rdfs": RDFS, "ns": "http://somewhere#" }
)
for r in g.query(q2):
  print(r)

# %% [markdown]
# **TASK 7.3: List all individuals of just "Person" or "Animal". You do not need to list the individuals of the subclasses of person (in SPARQL only)**
# 

# %%
# TO DO
q3 = prepareQuery('''
  SELECT DISTINCT ?individual WHERE
  {
    {
      ?individual a ns:Person .
    }
    UNION
    {
      ?individual a ns:Animal .
    }
  }
  ''',
  initNs = { "rdfs": RDFS, "ns": "http://somewhere#" }
)
# Visualize the results
for r in g.query(q3):
  print(r)

# %% [markdown]
# **TASK 7.4:  List the name of the persons who know Rocky (in SPARQL only)**

# %%
# TO DO
q4 = prepareQuery('''
  SELECT DISTINCT ?person WHERE
  {
      ?person foaf:knows ns:RockySmith .
      FILTER (?person != <http://somewhere#Bugs>) .
  }
  ''',
  initNs = { "rdfs": RDFS, "foaf": FOAF, "ns": "http://somewhere#" }
)
# Visualize the results
for r in g.query(q4):
  print(r)

# %% [markdown]
# **Task 7.5: List the name of those animals who know at least another animal in the graph (in SPARQL only)**

# %%
# TO DO
q5 = prepareQuery('''
  SELECT DISTINCT ?animal WHERE
  {
      ?animal rdf:type ns:Animal .
      ?animal foaf:knows ?animal2 .
      ?animal2 rdf:type ns:Animal . 
  }
  ''',
  initNs = { "rdfs": RDFS, "foaf": FOAF, "ns": "http://somewhere#" }
)
# Visualize the results
for r in g.query(q5):
  print(r)

# %% [markdown]
# **Task 7.6: List the age of all living things in descending order (in SPARQL only)**

# %%
# TO DO
q6 = prepareQuery('''
  SELECT ?age WHERE
  {
    {
      ?livingThing a ns:LivingThing .
      ?livingThing foaf:age ?age .
                  
    }
    UNION
    {
      ?subClass rdfs:subClassOf ns:LivingThing .
      ?livingThing a ?subClass .
      ?livingThing foaf:age ?age .
    }               
  }
  ORDER BY DESC(?age)
  ''',
  initNs = { "rdfs": RDFS, "foaf": FOAF, "ns": "http://somewhere#" }
)
# Visualize the results
for r in g.query(q6):
  print(r)


