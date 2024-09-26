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

**Question 2**

```
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dbo: <http://dbpedia.org/ontology/>

SELECT DISTINCT ?property
WHERE {
  ?instance rdf:type dbo:Politician .
  ?instance ?property ?value .
  FILTER (?property != rdf:type)
}
```

**Question 3**

```
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dbo: <http://dbpedia.org/ontology/>

SELECT (COUNT(DISTINCT ?property) AS ?propertyCount)
WHERE {
  ?instance rdf:type dbo:Politician .
  ?instance ?property ?value .
  FILTER (?property != rdf:type)
}
```

**Question 4**

```
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dbo: <http://dbpedia.org/ontology/>

SELECT ?property (GROUP_CONCAT(DISTINCT ?value; separator=", ") AS ?uniqueValues)
WHERE {
  ?instance rdf:type dbo:Politician .
  ?instance ?property ?value .
  FILTER (?property != rdf:type)
}
GROUP BY ?property
```

**Question 5**

```
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dbo: <http://dbpedia.org/ontology/>

SELECT ?property (COUNT(DISTINCT ?value) AS ?count)
WHERE {
  ?instance rdf:type dbo:Politician .
  ?instance ?property ?value .
  FILTER (?property != rdf:type)
}
GROUP BY ?property
ORDER BY ?property
```
