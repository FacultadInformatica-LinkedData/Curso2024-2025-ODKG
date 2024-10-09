#!/usr/bin/env python
# coding: utf-8

# **Task 06: Modifying RDF(s)**

# In[1]:


get_ipython().system('pip install rdflib')
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2024-2025/master/Assignment4/course_materials"


# Read the RDF file as shown in class

# In[2]:


from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example5.rdf", format="xml")


# In[3]:


for s, p, o in g:
  print(s,p,o)


# Create a new class named Researcher

# In[4]:


ns = Namespace("http://somewhere#")
g.add((ns.Researcher, RDF.type, RDFS.Class))
for s, p, o in g:
  print(s,p,o)


# In[5]:


print(g.serialize(format="xml"))


# **TASK 6.1: Create a new class named "University"**
# 

# In[6]:


# TO DO

g.add((ns.University, RDF.type, RDFS.Class))
# Visualize the results
for s, p, o in g:
  print(s,p,o)


# **TASK 6.2: Add "Researcher" as a subclass of "Person"**

# In[7]:


# TO DO
g.add((ns.Researcher, RDFS.subClassOf, ns.Person))
# Visualize the results
for s, p, o in g:
  print(s,p,o)


# **TASK 6.3: Create a new individual of Researcher named "Jane Smithers"**

# In[8]:


# TO DO
jane_smithers = ns.JaneSmithers  
g.add((jane_smithers, RDF.type, ns.Researcher))
# Visualize the results
for s, p, o in g:
  print(s,p,o)


# **TASK 6.4: Add to the individual JaneSmithers the email address, fullName, given and family names. Use the https://schema.org vocabulary**

# In[9]:


# TO DO
schema = Namespace("https://schema.org/")
g.add((jane_smithers, schema.email, Literal("jane.smithers@email.com")))
g.add((jane_smithers, schema.name, Literal("Jane Smithers")))
g.add((jane_smithers, schema.givenName, Literal("Jane")))
g.add((jane_smithers, schema.familyName, Literal("Smithers")))
# Visualize the results
for s, p, o in g:
  print(s,p,o)


# **TASK 6.5: Add UPM as the university where John Smith works. Use the "https://example.org/ namespace**

# In[10]:


# TO DO
nsexample = Namespace("https://example.org/")
john_smith = ns.JohnSmith 
g.add((john_smith, RDF.type, ns.Researcher))
upm = nsexample.UPM
g.add((upm, RDF.type, ns.University))  
g.add((john_smith, nsexample.worksAt, upm)) 
# Visualize the result
for s, p, o in g:
  print(s,p,o)


# **Task 6.6: Add that Jown knows Jane using the FOAF vocabulary. Make sure the relationship exists.**

# In[11]:


# TO DO
foaf = Namespace("http://xmlns.com/foaf/0.1/")
g.add((john_smith, foaf.knows, jane_smithers))
# Visualize the results
for s, p, o in g:
  print(s,p,o)


# In[ ]:




