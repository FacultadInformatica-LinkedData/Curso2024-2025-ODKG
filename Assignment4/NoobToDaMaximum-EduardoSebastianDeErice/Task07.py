#!/usr/bin/env python
# coding: utf-8

# **Task 07: Querying RDF(s)**

# In[1]:


#!pip install rdflib
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

# In[36]:


# TO DO
# Visualize the results
ns = Namespace("http://somewhere#")

query = """
PREFIX ns: <http://somewhere#>

    SELECT ?subclass WHERE {
        ?subclass rdfs:subClassOf ns:LivingThing .
    }
"""

subclasses = g.query(query)
for row in subclasses:
  print(row)


# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**
# 

# In[37]:


# TO DO
# Visualize the results
query = """
PREFIX ns: <http://somewhere#>

    SELECT ?individual WHERE {
        {
            ?individual rdf:type ns:Person .
        }
        UNION
        {
            ?subclass rdfs:subClassOf ns:Person .
            ?individual rdf:type ?subclass .
        }
    }
"""

# Execute the query
individuals = g.query(query)

# Output the results
for row in individuals:
    print(f"Individual: {row.individual}")


# **TASK 7.3: List all individuals of just "Person" or "Animal". You do not need to list the individuals of the subclasses of person (in SPARQL only)**
# 

# In[38]:


# TO DO
# Visualize the results
query = """
PREFIX ns: <http://somewhere#>

SELECT ?individual WHERE {
    {
        ?individual rdf:type ns:Person .
    }
    UNION
    {
        ?individual rdf:type ns:Animal .
    }
}
"""

# Execute the query
individualsPA = g.query(query)

# Output the results
for row in individualsPA:
    print(f"IndividualPA: {row.individual}")


# **TASK 7.4:  List the name of the persons who know Rocky (in SPARQL only)**

# In[39]:


# TO DO
# Visualize the results
query = """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX vcard: <http://www.w3.org/2001/vcard-rdf/3.0/>
PREFIX ns: <http://somewhere#>

SELECT ?name WHERE {
    ?person foaf:knows ns:RockySmith .
    ?person vcard:FN ?name .
}
"""

# Execute the query
personKnowsRocky = g.query(query)

# Output the results
for row in personKnowsRocky:
    print(row.name)


# **Task 7.5: List the name of those animals who know at least another animal in the graph (in SPARQL only)**

# In[97]:


# TO DO
# Visualize the results
query = """
PREFIX ns: <http://somewhere#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX vcard: <http://www.w3.org/2001/vcard-rdf/3.0/>

SELECT ?animalName ?knownAnimalName
WHERE {
    ?animal a ns:Animal .
    ?animal vcard:Given ?animalName .  # Get the name of the animal
    ?animal foaf:knows ?knownAnimal .  # Find whom the animal knows
    ?knownAnimal a ns:Animal .        # Ensure the known entity is also an Animal
    ?knownAnimal vcard:Given ?knownAnimalName .  # Get the name of the known animal
}
"""

# Execute the query
animal_knowings = g.query(query)

# Output the results
if not animal_knowings:
    print("No animals that know other animals.")
else:
    for row in animal_knowings:
        print(f"Animal: {row.animalName} knows {row.knownAnimalName}")


# **Task 7.6: List the age of all living things in descending order (in SPARQL only)**

# In[104]:


# TO DO
# Visualize the results
query = """
PREFIX ns: <http://somewhere#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX vcard: <http://www.w3.org/2001/vcard-rdf/3.0/>

SELECT ?name ?age
WHERE {
    { ?thing a ns:Animal . }
    UNION
    { ?thing a ns:Person . }
    UNION
    { ?thing a ns:Researcher . }
    UNION
    { ?thing a ns:Professor . }
    ?thing foaf:age ?age .
    ?thing vcard:Given ?name .
}
ORDER BY DESC(?age)
"""

# Execute the query
ages = g.query(query)

# Output the results
for row in ages:
    print(f"Name: {row.name}, Age: {row.age}")


# In[ ]:




