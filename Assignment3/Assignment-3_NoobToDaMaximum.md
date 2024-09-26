# Assignment 3 SPARQL Queries

**Question 1**

```
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dbo: <http://dbpedia.org/ontology/>

SELECT DISTINCT ?property
WHERE {
  ?instance rdf:type dbo:Politician .
  ?instance ?property ?value .
}
```
