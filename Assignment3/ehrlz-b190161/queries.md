# Advanced set of SPARQL queries 
1. Get all the properties that can be
  applied to instances of the Politician class
  (<http://dbpedia.org/ontology/Politician>)
```
SELECT DISTINCT ?a
WHERE {
 ?x a dbo:Politician.
 ?x ?a ?y
}
```

2. Get all the properties, except `rdf:type`, that can be applied to instances of the Politician class
```
SELECT DISTINCT ?a
WHERE {
 ?x a dbo:Politician.
 ?x ?a ?y.
 FILTER (?a != rdf:type)
}
```

3. Which different values exist for the properties, except for rdf:type, applicable to the instances of Politician?
```
SELECT DISTINCT ?y
WHERE {
 ?x a dbo:Politician.
 ?x ?a ?y.
 FILTER (?a != rdf:type)
}
```

4. For each of these applicable properties, except for rdf:type, which different values do they take globally for all those instances?
```
SELECT DISTINCT ?a ?y
WHERE {
  ?x a dbo:Politician.
  ?x ?a ?y.
  FILTER (?a != rdf:type)
}
```


5. For each of these applicable properties, except for rdf:type, how many distinct values do they take globally for all those instances?
```
SELECT ?a (COUNT(DISTINCT ?y) AS ?count)
WHERE {
  ?x a dbo:Politician.
  ?x ?a ?y.
  FILTER (?a != rdf:type)
}
GROUP BY ?a
```