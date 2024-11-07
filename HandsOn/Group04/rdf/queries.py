from rdflib import Graph

# Carga del grafo
g = Graph()
g.parse("rdf/dataset.ttl", format="turtle")


#QUERY 1

query_1 = """
PREFIX vocab: <http://www.chargeAndParkMadrid.org/opendata/handsOn/group04/ontology/Ontology#> 
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 

SELECT (COUNT(?chargePoint) AS ?total)
WHERE {
    ?chargePoint rdf:type vocab:ChargePoint .
}
"""

print("___________________________________\nQUERY 1 RESULT:")
qres = g.query(query_1)
for row in qres:
        print(row.total)

#QUERY 2

query_2 = """
PREFIX vocab: <http://www.chargeAndParkMadrid.org/opendata/handsOn/group04/ontology/Ontology#> 
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 

SELECT ?chargePoint
WHERE {
    ?chargePoint rdf:type vocab:ChargePoint .
}
"""

print("___________________________________\nQUERY 2 RESULT:")
qres = g.query(query_2)
for row in qres:
        print(row.chargePoint)

#QUERY 3

query_3 = """
PREFIX vocab: <http://www.chargeAndParkMadrid.org/opendata/handsOn/group04/ontology/Ontology#> 
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 

SELECT ?chargePoint
WHERE {
    ?chargePoint vocab:managedBy ?operator .
    ?operator rdf:label ?name .
    FILTER( ?name = "GIC") .
}
"""

print("___________________________________\nQUERY 3 RESULT:")
qres = g.query(query_3)
for row in qres:
        print(row.chargePoint)


#QUERY 4

query_4 = """
PREFIX vocab: <http://www.chargeAndParkMadrid.org/opendata/handsOn/group04/ontology/Ontology#> 
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 

SELECT (COUNT(?parking) AS ?total)
WHERE {
    ?parking rdf:type vocab:Parking .
}
"""

print("___________________________________\nQUERY 4 RESULT:")
qres = g.query(query_4)
for row in qres:
        print(row.total)

#QUERY 5

query_5 = """
PREFIX vocab: <http://www.chargeAndParkMadrid.org/opendata/handsOn/group04/ontology/Ontology#> 
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 

SELECT ?parkings
WHERE {
    ?parkings vocab:locatedInStreet ?street .
    ?street rdf:label ?name .
    FILTER( ?name = "Calle Fuente De Lima") .
}
"""

print("___________________________________\nQUERY 5 RESULT:")
qres = g.query(query_5)
for row in qres:
        print(row.parkings)

#QUERY 6

query_6= """
PREFIX vocab: <http://www.chargeAndParkMadrid.org/opendata/handsOn/group04/ontology/Ontology#> 
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 

SELECT ?parkings
WHERE {
    ?parkings rdf:type vocab:Parking .
    ?parkings vocab:locatedInStreet ?street .
    ?street vocab:locatedInNeighborhood ?neighborhood .
    ?neighborhood vocab:isPartOf ?district .
    ?district rdf:label ?name .
    FILTER( ?name = "Retiro") .
}
"""

print("___________________________________\nQUERY 6 RESULT:")
qres = g.query(query_6)
for row in qres:
        print(row.parkings)


#QUERY 7

query_7= """
PREFIX vocab: <http://www.chargeAndParkMadrid.org/opendata/handsOn/group04/ontology/Ontology#> 
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 

SELECT (COUNT(?place) AS ?total)
WHERE {
    ?place rdf:type ?class .
    ?place vocab:locatedInStreet ?street .
    ?street vocab:locatedInNeighborhood ?neighborhood .
    ?neighborhood vocab:isPartOf ?district .
    ?district rdf:label ?name .
    FILTER(?name = "Retiro")
}
GROUP BY ?class
"""

print("___________________________________\nQUERY 7 RESULT:")
qres = g.query(query_7)
for row in qres:
        print(row.total)



