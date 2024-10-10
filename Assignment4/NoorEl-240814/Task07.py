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


q1 = """
    SELECT ?subclass WHERE {
        ?subclass rdfs:subClassOf ns:LivingThing .
    }
"""

# Execute the query and visualize the results
for r in g.query(q1):
    print(r)


# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**
# 

# In[4]:


q2 = """
    SELECT ?individual WHERE {
        ?individual rdf:type ns:Person .
        ?individual rdf:type ?subclass .
    }
"""

# Execute the query and visualize the results
for r in g.query(q2):
    print(r)


# **TASK 7.3: List all individuals of just "Person" or "Animal". You do not need to list the individuals of the subclasses of person (in SPARQL only)**
# 

# In[7]:


q3 = """
    SELECT ?individual WHERE {
        { ?individual rdf:type ns:Person . }
        UNION
        { ?individual rdf:type ns:Animal . }
    }
"""

# Execute the query and visualize the results
for r in g.query(q3):
    print(r)




# **TASK 7.4:  List the name of the persons who know Rocky (in SPARQL only)**

# In[13]:


q4 = '''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ns: <http://somewhere#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?individual
WHERE {
  ?individual foaf:knows ns:RockySmith .
}
'''

# Visualize the results
for r in g.query(q4):
  print(r)


# **Task 7.5: List the name of those animals who know at least another animal in the graph (in SPARQL only)**

# In[14]:


q5 = """
    SELECT ?animal WHERE {
        ?animal rdf:type ns:Animal .
        ?animal foaf:knows ?otherAnimal .
        ?otherAnimal rdf:type ns:Animal .
    }
"""

# Execute the query and visualize the results
for r in g.query(q5):
    print(r)


# **Task 7.6: List the age of all living things in descending order (in SPARQL only)**

# In[17]:


q6 = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX ns: <http://somewhere#>
SELECT ?livingThing ?age
WHERE {{
    ?livingThing rdf:type ?subclass .
    ?subclass rdfs:subClassOf ns:LivingThing .
    ?livingThing foaf:age ?age.
  } UNION {
    ?livingThing rdf:type ns:LivingThing .
    ?livingThing foaf:age ?age.
  }}
ORDER BY DESC(?age)
"""



# Visualize the results
for r in g.query(q6):
  print(r)


# In[ ]:




