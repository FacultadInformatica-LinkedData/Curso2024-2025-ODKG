#!/usr/bin/env python
# coding: utf-8

# ## Task 07: Querying RDF(s)

# In[28]:


get_ipython().system('pip install rdflib')
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2024-2025/master/Assignment4/course_materials"


# In[29]:


# First let's read the RDF file
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")


# In[30]:


# TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL

# TO DO
from rdflib.plugins.sparql import prepareQuery

ns = Namespace("http://somewhere#")
#VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")

q1 = prepareQuery('''
  SELECT ?s WHERE {
    ?s rdfs:subClassOf ns:LivingThing.
  }
  ''',
  initNs={'ns': ns, 'rdfs': RDFS}
)

# Visualize the results
for r in g.query(q1):
    print(r.s)


# In[114]:


# TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)
# TO DO
ns= Namespace("http://somewhere#")
q1 = prepareQuery('''
  SELECT ?individual WHERE {
    {
      ?individual a ns:Person.
    }
    UNION
    {
      ?subclass rdfs:subClassOf ns:Person.
      ?individual a ?subclass.
    }
  }
  ''',
  initNs={'ns': ns, 'rdfs': RDFS}
)

# Execute the query and visualize the results
for r in g.query(q1):
    print(r.individual)


# In[115]:


# TASK 7.3: List all individuals of just "Person" or "Animal".
# You do not need to list the individuals of the subclasses of person (in SPARQL only)

# TO DO
ns = Namespace("http://somewhere#")
q1 = prepareQuery('''
  SELECT ?s WHERE {
    ?s rdf:type ?v.
    FILTER (?v = ns:Person || ?v = ns:Animal)
    }
  ''',
  initNs={'ns': ns, 'rdfs': RDFS}
)

# Execute the query and visualize the results
for r in g.query(q1):
    print(r.s)


# In[117]:


# TASK 7.4: List the name of the persons who know Rocky (in SPARQL only)
# TO DO
from rdflib.plugins.sparql import prepareQuery

ns = Namespace("http://somewhere#")
foaf = Namespace("http://xmlns.com/foaf/0.1/")
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")

q4 = prepareQuery('''
  SELECT ?v WHERE {
    ?s foaf:knows ns:RockySmith .
    ?s vcard:FN ?v.
  }
  ''',
  initNs={'ns': ns, 'foaf': foaf, 'vcard': vcard}
)

# Execute the query and visualize the results
for r in g.query(q4):
    print(r.v)


# In[118]:


# Task 7.5: List the name of those animals who know at least another animal in the graph (in SPARQL only)
# TO DO
from rdflib.plugins.sparql import prepareQuery

ns = Namespace("http://somewhere#")
foaf = Namespace("http://xmlns.com/foaf/0.1/")
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")

q1 = prepareQuery('''
  SELECT ?v WHERE {
    ?s rdf:type ns:Animal.
    ?s foaf:knows ?OtherAnimal .
    OPTIONAL { ?s vcard:FN ?v. }
    OPTIONAL { ?s vcard:Given ?v. }  
  }
  ''',
  initNs={'ns': ns, 'rdf': RDF, 'foaf': foaf, 'vcard': vcard}
)

# Execute the query and visualize the results
for r in g.query(q1):
    print(r.v)


# In[131]:


from rdflib import Namespace
from rdflib.plugins.sparql import prepareQuery
# TO DO
ns = Namespace("http://somewhere#")
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")
rdf = Namespace("http://www.w3.org/2000/01/rdf-schema#")

q1 = prepareQuery('''
SELECT ?individual ?age WHERE {
  {
    
      ?individual a ns:Person.
      OPTIONAL { ?individual ns:age ?age. } 
    }
    UNION
    {
      ?subclass rdf:subClassOf ns:Person.
      ?individual a ?subclass.
      OPTIONAL { ?individual ns:age ?age. } 
    }
  }
ORDER BY DESC(?age)
''',
  initNs={'ns': ns, 'rdf': rdf, 'vcard': vcard}
)

# Execute the query and visualize the results
for r in g.query(q1):
    print(r.individual)


# In[ ]:




