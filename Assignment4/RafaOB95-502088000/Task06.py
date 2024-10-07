#!/usr/bin/env python
# coding: utf-8

# ## Task 06: Modifying RDF(s)

# In[18]:


get_ipython().system('pip install rdflib')
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2024-2025/master/Assignment4/course_materials"


# In[19]:


# Read the RDF file as shown in class
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example5.rdf", format="xml")


# In[20]:


# Create a new class named Researcher
ns = Namespace("http://somewhere#")
g.add((ns.Researcher, RDF.type, RDFS.Class))
for s, p, o in g:
  print(s,p,o)


# In[21]:


# TASK 6.1: Create a new class named "University"
# TO DO
ns = Namespace("http://somewhere#")
g.add((ns.University, RDF.type, RDFS.Class))
# Visualize the results
for s, p, o in g:
  print(s,p,o)


# In[22]:


# TASK 6.2: Add "Researcher" as a subclass of "Person"
# TO DO
g.add((ns.Person, RDF.type, RDFS.Class))
g.add((ns.Researcher, RDFS.subClassOf, ns.Person))
# Visualize the results
for s, p, o in g:
  print(s,p,o)


# In[23]:


# ASK 6.3: Create a new individual of Researcher named "Jane Smithers"
# TO DO
fullName = Literal("Jane Smithers")
EX = Namespace("http://somewhere#")
janeURI = EX.JaneSmithers
g.add((janeURI, RDF.type, ns.Researcher))
# Visualize the results
for s, p, o in g:
  print(s,p,o)


# In[25]:


# TASK 6.4: Add to the individual JaneSmithers the email address, fullName, given and family names. 
# Use the https://schema.org vocabulary
# TO DO
schema = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
g.add((janeURI, vcard.FN, Literal("Jane Smithers")))
g.add((janeURI, vcard.Given, Literal("Jane")))
g.add((janeURI, vcard.Family, Literal("Smithers")))
g.add((janeURI, vcard.EMAIL, Literal("jane.smithers@example.com")))
# Visualize the results
for s, p, o in g:
  print(s,p,o)


# In[29]:


# TASK 6.5: Add UPM as the university where John Smith works. Use the "https://example.org/namespace
# TO DO
ex = Namespace("https://example.org/")
univURI = ex.UPM

johnURI = ns.JohnSmith
g.add((johnURI, ex.worksAt, univURI))
# Visualize the results
for s, p, o in g:
  print(s,p,o)


# In[31]:


# Task 6.6: Add that Jown knows Jane using the FOAF vocabulary. Make sure the relationship exists.
# TO DO
foaf = Namespace("http://xmlns.com/foaf/spec/")

g.add((johnURI, foaf.knows, janeURI))
# Visualize the results
for s, p, o in g:
  print(s,p,o)


# In[ ]:




