#!/usr/bin/env python
# coding: utf-8

# **Task 06: Modifying RDF(s)**

# In[1]:


get_ipython().system('pip install rdflib')
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2024-2025/master/Assignment4/course_materials"


# Read the RDF file as shown in class

# In[3]:


from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example5.rdf", format="xml")


# Create a new class named Researcher

# In[4]:


ns = Namespace("http://somewhere#")
g.add((ns.Researcher, RDF.type, RDFS.Class))
for s, p, o in g:
  print(s,p,o)


# **TASK 6.1: Create a new class named "University"**
# 

# In[5]:


# Create a new class named University
g.add((ns.University, RDF.type, RDFS.Class))

# Visualize the results
for s, p, o in g:
  print(s, p, o)


# **TASK 6.2: Add "Researcher" as a subclass of "Person"**

# In[6]:


# Add "Researcher" as a subclass of "Person"
g.add((ns.Researcher, RDFS.subClassOf, ns.Person))

# Visualize the results
for s, p, o in g:
  print(s, p, o)


# **TASK 6.3: Create a new individual of Researcher named "Jane Smithers"**

# In[7]:


# Create a new individual of Researcher named "Jane Smithers"
jane = ns["JaneSmithers"]
g.add((jane, RDF.type, ns.Researcher))

# Visualize the results
for s, p, o in g:
  print(s, p, o)


# **TASK 6.4: Add to the individual JaneSmithers the email address, fullName, given and family names. Use the https://schema.org vocabulary**

# In[8]:


# Use the https://schema.org vocabulary for Jane's details
SCHEMA = Namespace("https://schema.org/")
g.bind("schema", SCHEMA)

g.add((jane, SCHEMA.email, Literal("jane.smithers@example.com")))
g.add((jane, SCHEMA.givenName, Literal("Jane")))
g.add((jane, SCHEMA.familyName, Literal("Smithers")))
g.add((jane, SCHEMA.name, Literal("Jane Smithers")))

# Visualize the results
for s, p, o in g:
  print(s, p, o)


# **TASK 6.5: Add UPM as the university where John Smith works. Use the "https://example.org/ namespace**

# In[9]:


# Add UPM as the university where John Smith works using example.org namespace
EX = Namespace("https://example.org/")
g.bind("ex", EX)

john = ns["JohnSmith"]
upm = EX["UPM"]

g.add((john, SCHEMA.affiliation, upm))

# Visualize the results
for s, p, o in g:
  print(s, p, o)


# **Task 6.6: Add that Jown knows Jane using the FOAF vocabulary. Make sure the relationship exists.**

# In[10]:


# Use FOAF to indicate that John knows Jane
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
g.bind("foaf", FOAF)

g.add((john, FOAF.knows, jane))

# Visualize the results
for s, p, o in g:
  print(s, p, o)


# In[ ]:




