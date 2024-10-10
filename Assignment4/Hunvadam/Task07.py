#!/usr/bin/env python
# coding: utf-8

# **Task 07: Querying RDF(s)**

# In[1]:


get_ipython().system('pip install rdflib')
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2024-2025/master/Assignment4/course_materials"


# First let's read the RDF file

# In[2]:


from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")


# **TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**

# In[8]:


# TO DO
ns = Namespace("http://somewhere#")
from rdflib.plugins.sparql import prepareQuery

q1 = prepareQuery("""
SELECT ?subclass
WHERE {
  ?subclass rdfs:subClassOf ns:LivingThing .
}
""", initNs={"rdfs": RDFS, "ns": ns})

subclasses = g.query(q1)
# Visualize the results

for r in g.query(q1):
  print(r)


# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**
# 

# In[13]:


# TO DO
ns = Namespace("http://somewhere#")
from rdflib.plugins.sparql import prepareQuery

q1 = prepareQuery("""
SELECT ?individual
WHERE {
  ?class rdfs:subClassOf* ns:Person .
  ?individual rdf:type ?class 
   }
""", initNs={"rdfs": RDFS, "ns": ns})

subclasses = g.query(q1)
# Visualize the results

for r in g.query(q1):
  print(r)


# **TASK 7.3: List all individuals of just "Person" or "Animal". You do not need to list the individuals of the subclasses of person (in SPARQL only)**
# 

# In[16]:


# TO DO
ns = Namespace("http://somewhere#")
from rdflib.plugins.sparql import prepareQuery

q1 = prepareQuery("""
SELECT ?individual
WHERE {
  ?individual rdf:type ?class .
  FILTER (?class = ns:Person || ?class = ns:Animal)
}
""", initNs={"rdfs": RDFS, "ns": ns})

subclasses = g.query(q1)
# Visualize the results

for r in g.query(q1):
  print(r)


# **TASK 7.4:  List the name of the persons who know Rocky (in SPARQL only)**

# In[32]:


# TO DO
ns = Namespace("http://somewhere#")
from rdflib import FOAF
from rdflib.plugins.sparql import prepareQuery

q1 = prepareQuery("""
SELECT ?Name 
WHERE {
    ?Name foaf:knows ns:RockySmith
  }
  """,
  initNs = { "rdfs": RDFS, "foaf": FOAF, "ns": ns }
  )

subclasses = g.query(q1)
# Visualize the results

for r in g.query(q1):
  print(r)


# **Task 7.5: List the name of those animals who know at least another animal in the graph (in SPARQL only)**

# In[40]:


# TO DO
ns = Namespace("http://somewhere#")
from rdflib import FOAF
from rdflib.plugins.sparql import prepareQuery

q1 = prepareQuery("""
SELECT ?Name 
WHERE {
    ?Name foaf:knows ?AnotherAnimal .
    ?Name rdf:type ns:Animal .
    ?AnotherAnimal rdf:type ns:Animal
  }
  """,
  initNs = { "rdfs": RDFS, "foaf": FOAF, "ns": ns }
  )

subclasses = g.query(q1)
# Visualize the results

for r in g.query(q1):
  print(r)


# **Task 7.6: List the age of all living things in descending order (in SPARQL only)**

# In[46]:


# TO DO
ns = Namespace("http://somewhere#")
from rdflib import FOAF
from rdflib.plugins.sparql import prepareQuery

q1 = prepareQuery("""
SELECT ?LivingThing ?age
WHERE {
    ?LivingThing foaf:age ?age .
  }
ORDER BY DESC(?age)
  """,
  initNs = { "rdfs": RDFS, "foaf": FOAF, "ns": ns }
  )



subclasses = g.query(q1)
# Visualize the results

for r in g.query(q1):
  print(r)


# In[ ]:




