#!/usr/bin/env python
# coding: utf-8

# **Task 06: Modifying RDF(s)**

# In[4]:


get_ipython().system('pip install rdflib')
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2024-2025/master/Assignment4/course_materials"


# Read the RDF file as shown in class

# In[9]:


from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example5.rdf", format="xml")


# Create a new class named Researcher

# In[10]:


ns = Namespace("http://somewhere#")
g.add((ns.Researcher, RDF.type, RDFS.Class))
for s, p, o in g:
  print(s,p,o)


# **TASK 6.1: Create a new class named "University"**
# 

# In[13]:


# TO DO
g.add((ns.University, RDF.type, RDFS.Class))
# Visualize the results
for s, p, o in g:
  print(s,p,o)


# **TASK 6.2: Add "Researcher" as a subclass of "Person"**

# In[14]:


# TO DO
g.add((ns.Researcher, RDFS.subClassOf, ns.Person))
# Visualize the results
for s, p, o in g:
  print(s,p,o)


# **TASK 6.3: Create a new individual of Researcher named "Jane Smithers"**

# In[16]:


# TO DO
g.add((ns.JaneSmithers, RDF.type, ns.Researcher))
# Visualize the results
for s, p, o in g:
  print(s,p,o)


# **TASK 6.4: Add to the individual JaneSmithers the email address, fullName, given and family names. Use the https://schema.org vocabulary**

# In[19]:


# TO DO
schema = Namespace("https://schema.org/")
g.add((ns.JaneSmithers, schema.email, Literal("jane.smithers@example.com")))
g.add((ns.JaneSmithers, schema.name, Literal("Jane Smithers")))
g.add((ns.JaneSmithers, schema.givenName, Literal("Jane")))
g.add((ns.JaneSmithers, schema.familyName, Literal("Smithers")))
# Visualize the results
for s, p, o in g:
    print(s, p, o)


# **TASK 6.5: Add UPM as the university where John Smith works. Use the "https://example.org/ namespace**

# In[26]:


# TO DO
ns = Namespace("https://example.org/")
g.add((ns.UPM, RDF.type, ns.University))
g.add((ns.JohnSmith, ns.worksFor, ns.UPM))

# Visualize the results
for s, p, o in g:
    print(s, p, o)


# **Task 6.6: Add that Jown knows Jane using the FOAF vocabulary. Make sure the relationship exists.**

# In[25]:


# TO DO
foaf = Namespace("http://xmlns.com/foaf/spec/")
g.add((ns.JohnSmith, foaf.knows, ns.JaneSmithers))
# Visualize the results
for s, p, o in g:
    print(s, p, o)


# In[ ]:




