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

# In[3]:


# TO DO

q1 = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ns: <http://somewhere#>

SELECT ?x
WHERE {
  ?x rdfs:subClassOf ns:LivingThing .
}
"""

# Visualize the results
for r in g.query(q1):
    print(r)


# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**
# 

# In[4]:


# TO DO
q2 = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ns: <http://somewhere#>

SELECT ?x
WHERE {
  ?x rdf:type/rdfs:subClassOf* ns:Person .
}
"""

# Visualize the result
for r in g.query(q2):
    print(r)


# **TASK 7.3: List all individuals of just "Person" or "Animal". You do not need to list the individuals of the subclasses of person (in SPARQL only)**
# 

# In[5]:


# TO DO
q3 = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ns: <http://somewhere#>

SELECT ?x
WHERE {
  ?x rdf:type ?type .
  FILTER(?type = ns:Person || ?type = ns:Animal)
}
"""

# Execute the query and visualize the results
for r in g.query(q3):
    print(r)
# Visualize the results


# **TASK 7.4:  List the name of the persons who know Rocky (in SPARQL only)**

# In[6]:


# Task 7.4: List the name of persons who know RockySmith
q4 = """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX ns: <http://somewhere#>

SELECT ?x
WHERE {
  ?xn foaf:knows ns:RockySmith .
}
"""

# Execute the query and visualize the results
for r in g.query(q4):
    print(r)


# **Task 7.5: List the name of those animals who know at least another animal in the graph (in SPARQL only)**

# In[7]:


# Task 7.5: List the names of animals who know at least another animal
q5 = """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX ns: <http://somewhere#>

SELECT ?x
WHERE {
  ?x rdf:type ns:Animal .
  ?x foaf:knows ?z .
  ?z rdf:type ns:Animal .
}
"""

# Execute the query and visualize the results
for r in g.query(q5):
    print(r)


# **Task 7.6: List the age of all living things in descending order (in SPARQL only)**

# In[8]:


# Task 7.6: List the age of all Persons and Animals in descending order
q6 = """
PREFIX ns: <http://somewhere#>

SELECT ?x ?age
WHERE {
  ?x rdf:type ?type .
  FILTER(?type = ns:Person || ?type = ns:Animal) .
  ?x ?predicate ?age .
  FILTER (datatype(?age) = xsd:integer || datatype(?age) = xsd:decimal) .
}
ORDER BY DESC(?age)
"""

# Execute the query and visualize the results
for r in g.query(q6):
    print(r)


# In[ ]:




