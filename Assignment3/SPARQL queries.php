Create the SPARQL query and the result for the following queries expressed in natural language. The endpoint
that you can use for this exercise is: http://es.dbpedia.org/sparql
1. Get all the properties that can be applied to instances of the Politician class (<http://dbpedia.org/ontology/Politician>)
select distinct ?property
where {
?politician a <http://dbpedia.org/ontology/Politician>;
?property ?value.
}
2. Get all the properties, except rdf:type, that can be applied to instances of the Politician class
select distinct ?property
where {
?politician a <http://dbpedia.org/ontology/Politician>;
?property ?value.
filter(?property != rdf:type)
}
3. Which different values exist for the properties, except for rdf:type, applicable to the instances of
Politician?
select distinct ?property ?value
where {
?politician a <http://dbpedia.org/ontology/Politician>;
?property ?value.
filter(?property != rdf:type)
}
4. For each of these applicable properties, except for rdf:type, which different values do they take globally
for all those instances?
select distinct ?property ?value
where {
?politician a <http://dbpedia.org/ontology/Politician>;
?property ?value.
filter(?property != rdf:type)
}
group by ?property
5. For each of these applicable properties, except for rdf:type, how many distinct values do they take
globally for all those instances?
select ?property (count(distinct ?value) AS ?valueCount)
where {
 ?politician a <http://dbpedia.org/ontology/Politician> ;
 ?property ?value .
 filter(?property != rdf:type)
}
group by ?property 