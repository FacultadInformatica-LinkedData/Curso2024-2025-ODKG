#!/usr/bin/env python
# coding: utf-8

# **Task 06: Modifying RDF(s)**

# In[2]:


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


# TO DO
# Visualize the results
g.add((ns.University, RDF.type, RDFS.Class))
for s, p, o in g:
  print(s,p,o)


# **TASK 6.2: Add "Researcher" as a subclass of "Person"**

# In[6]:


# TO DO
# Visualize the results
g.add((ns.Researcher, RDFS.subClassOf, ns.Person))
for s, p, o in g:
  print(s,p,o)


# **TASK 6.3: Create a new individual of Researcher named "Jane Smithers"**

# In[7]:


# TO DO
# Visualize the results
g.add((ns.JaneSmithers, RDF.type, ns.Researcher))
g.add((ns.JaneSmithers, RDFS.label, Literal("Jane Smithers")))
for s, p, o in g:
  print(s,p,o)


# **TASK 6.4: Add to the individual JaneSmithers the email address, fullName, given and family names. Use the https://schema.org vocabulary**

# In[9]:


# TO DO
# Visualize the results
schema = Namespace("https://schema.org/")

g.add((ns.JaneSmithers, schema.email, Literal("jane.smithers@example.com")))
g.add((ns.JaneSmithers, schema.name, Literal("Jane Smithers")))
g.add((ns.JaneSmithers, schema.givenName, Literal("Jane")))
g.add((ns.JaneSmithers, schema.familyName, Literal("Smithers")))

for s, p, o in g:
    print(s, p, o)


# **TASK 6.5: Add UPM as the university where John Smith works. Use the "https://example.org/ namespace**

# In[11]:


# TO DO
# Visualize the results
ex = Namespace("https://example.org/")

g.add((ns.UPM, RDF.type, ns.University))
g.add((ns.UPM, RDFS.label, Literal("Universidad Politécnica de Madrid")))
g.add((ns.JohnSmith, ex.worksAt, Literal("UPM")))

for s, p, o in g:
    print(s, p, o)


# **Task 6.6: Add that Jown knows Jane using the FOAF vocabulary. Make sure the relationship exists.**

# In[13]:


# TO DO
# Visualize the results
foaf = Namespace("http://xmlns.com/foaf/0.1/")

g.add((ns.JohnSmith, foaf.knows, ns.JaneSmithers))

for s, p, o in g:
    print(s, p, o)

