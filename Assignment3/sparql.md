# SPARQL QUERIES - Federico Castejón Lozano
## 1. Get all the properties that can be applied to instances of the Politician class (<http://dbpedia.org/ontology/Politician>)

```s
prefix db:<http://dbpedia.org/ontology/>

select distinct ?properties where {
?individuals a db:Politician .
?individuals ?properties ?values .
} 
```

https://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query=prefix+db%3A%3Chttp%3A%2F%2Fdbpedia.org%2Fontology%2F%3E%0D%0A%0D%0Aselect+distinct+%3Fproperties+where+%7B%0D%0A%3Findividuals+a+db%3APolitician+.%0D%0A%3Findividuals+%3Fproperties+%3Fvalues+.%0D%0A%7D+%0D%0A%0D%0A&format=text%2Fhtml&timeout=30000&signal_void=on&signal_unconnected=on

## 2. Get all the properties, except rdf:type, that can be applied to instances of the Politician class

```s
prefix db:<http://dbpedia.org/ontology/>

select distinct ?properties where {
?individuals a db:Politician .
?individuals ?properties ?values .
filter ( ?properties != rdf:type )
}
```

https://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query=prefix+db%3A%3Chttp%3A%2F%2Fdbpedia.org%2Fontology%2F%3E%0D%0A%0D%0Aselect+distinct+%3Fproperties+where+%7B%0D%0A%3Findividuals+a+db%3APolitician+.%0D%0A%3Findividuals+%3Fproperties+%3Fvalues+.%0D%0Afilter+%28+%3Fproperties+%21%3D+rdf%3Atype+%29%0D%0A%7D&format=text%2Fhtml&timeout=30000&signal_void=on&signal_unconnected=on

## 3. Which different values exist for the properties, except for rdf:type, applicable to the instances of Politician?

```s
prefix db:<http://dbpedia.org/ontology/>

select distinct ?value where {
?individuals a db:Politician .
?individuals ?properties ?value .
filter ( ?properties != rdf:type )
}
```

https://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query=%0D%0Aprefix+db%3A%3Chttp%3A%2F%2Fdbpedia.org%2Fontology%2F%3E%0D%0A%0D%0Aselect+distinct+%3Fvalue+where+%7B%0D%0A%3Findividuals+a+db%3APolitician+.%0D%0A%3Findividuals+%3Fproperties+%3Fvalue+.%0D%0Afilter+%28+%3Fproperties+%21%3D+rdf%3Atype+%29%0D%0A%7D&format=text%2Fhtml&timeout=30000&signal_void=on&signal_unconnected=on

## 4. For each of these applicable properties, except for rdf:type, which different values do they take globally for all those instances?

```s
prefix db:<http://dbpedia.org/ontology/>

select distinct ?properties ?values where {
?individuals a db:Politician .
?individuals ?properties ?values .
filter ( ?properties != rdf:type )
}
```

https://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query=prefix+db%3A%3Chttp%3A%2F%2Fdbpedia.org%2Fontology%2F%3E%0D%0A%0D%0Aselect+distinct+%3Fproperties+%3Fvalues+where+%7B%0D%0A%3Findividuals+a+db%3APolitician+.%0D%0A%3Findividuals+%3Fproperties+%3Fvalues+.%0D%0Afilter+%28+%3Fproperties+%21%3D+rdf%3Atype+%29%0D%0A%7D%0D%0A&format=text%2Fhtml&timeout=30000&signal_void=on&signal_unconnected=on


## 5. For each of these applicable properties, except for rdf:type, how many distinct values do they take globally for all those instances?
```s
prefix db:<http://dbpedia.org/ontology/>

select distinct ?properties count(distinct ?value) as ?distinct_values where {
?individuals a db:Politician .
?individuals ?properties ?value .
filter ( ?properties != rdf:type )
}
```
https://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query=prefix+db%3A%3Chttp%3A%2F%2Fdbpedia.org%2Fontology%2F%3E%0D%0A%0D%0Aselect+distinct+%3Fproperties+count%28distinct+%3Fvalue%29+as+%3Fdistinct_values+where+%7B%0D%0A%3Findividuals+a+db%3APolitician+.%0D%0A%3Findividuals+%3Fproperties+%3Fvalue+.%0D%0Afilter+%28+%3Fproperties+%21%3D+rdf%3Atype+%29%0D%0A%7D&format=text%2Fhtml&timeout=30000&signal_void=on&signal_unconnected=on
