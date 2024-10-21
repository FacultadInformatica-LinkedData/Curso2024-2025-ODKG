from rdflib import Graph

# Carga del grafo
g = Graph()
g.parse("rdf/dataset.ttl", format="turtle")


#QUERY 1
#Show all charging stations with all properties
query = """
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
PREFIX ns: <https://datos.madrid/estaciones_carga_vehiculos_electricos/ontology#>

SELECT ?s ?o ?p
WHERE {
  ?s a ns:ChargingStation .
  ?s ?o ?p ;
}
"""

print("\n\nOutput Query 1:")
result = g.query(query)
for row in result:
        print(row.total)

#QUERY 2
#Show each charging station along with its operator
query= """
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
PREFIX ns: <https://datos.madrid/estaciones_carga_vehiculos_electricos/ontology#>

SELECT ?chargingStation ?operator
WHERE {
  ?chargingStation a ns:ChargingStation ;
                   ns:operator ?operator .
}
"""

print("\n\nOutput Query 2:")
result = g.query(query)
for row in result:
        print(row.total)

#QUERY 3
#Show each charging station with its address, neighborhood and district 
query = """
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
PREFIX ns: <https://datos.madrid/estaciones_carga_vehiculos_electricos/ontology#>
PREFIX schema: <https://schema.org/>

SELECT ?s ?address ?neighborhoodName ?districtName
WHERE {
  ?s a ns:ChargingStation .
  ?s ns:isLocated ?place .
  ?place a schema:Place ;
     	schema:address ?address ;
  		schema:containedInPlace ?neighborhood .
  ?neighborhood a ns:Neighborhood ;
    ns:neighborhoodName ?neighborhoodName ;
    schema:containedInPlace ?district .
  ?district a ns:District ;
    ns:districtName ?districtName .
}
"""

print("\n\nOutput Query 3:")
result = g.query(query)
for row in result:
        print(row.total)

#QUERY 4
#Show each station with its assigned dates
query = """
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
PREFIX ns: <https://datos.madrid/estaciones_carga_vehiculos_electricos/ontology#>

SELECT ?IDchargingStation ?openingdate ?editiondate ?registerdate
WHERE {
  ?chargingStation a ns:ChargingStation ;
                   ns:hasDates ?dates ;
                   ns:idPoint ?IDchargingStation .
  ?dates a ns:Dates ;
        ns:openingDate ?openingdate ;
        ns:editionDate ?editiondate ;
        ns:registerDate ?registerdate .
}
"""

print("\n\nOutput Query 4:")
result = g.query(query)
for row in result:
        print(row.total)

#QUERY 5
#Show the most recent edited stations
query = """
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
PREFIX ns: <https://datos.madrid/estaciones_carga_vehiculos_electricos/ontology#>

SELECT ?IDchargingStation ?editiondate 
WHERE {
  ?chargingStation a ns:ChargingStation ;
                   ns:hasDates ?dates ;
                   ns:idPoint ?IDchargingStation .
  ?dates a ns:Dates ;
        ns:openingDate ?openingdate ;
        ns:editionDate ?editiondate ;
        ns:registerDate ?registerdate .
}
ORDER BY DESC(?editiondate)
"""

print("\n\nOutput Query 5:")
result = g.query(query)
for row in result:
        print(row.total)

#QUERY 6
#See the number of neighborhoods from each disctrict orderer desc

query= """
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
PREFIX ns: <https://datos.madrid/estaciones_carga_vehiculos_electricos/ontology#>
PREFIX schema: <https://schema.org/>

SELECT ?district ?districtname (COUNT(DISTINCT ?neighborhood) as ?numberOfNeighborhoods)
WHERE {
    ?district a ns:District ;
              ns:districtName ?districtname .
    ?neighborhood schema:containedInPlace ?district .
}
GROUP BY ?district
ORDER BY DESC(?numberOfNeighborhoods)
"""

print("\n\nOutput Query 6:")
result = g.query(query)
for row in result:
        print(row.total)


#QUERY 7
#See the number of charging stations from each neighborhood

query= """
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
PREFIX ns: <https://datos.madrid/estaciones_carga_vehiculos_electricos/ontology#>
PREFIX schema: <https://schema.org/>

SELECT ?neighborhoodname (COUNT(?chargingStation) AS ?stationCount)
WHERE {
  ?chargingStation a ns:ChargingStation ;
        ns:isLocated ?place .
  ?place a schema:Place ;
        schema:containedInPlace ?neighborhood .
  ?neighborhood a ns:Neighborhood ;
        ns:neighborhoodName ?neighborhoodname .
}
GROUP BY ?neighborhood
"""

print("\n\nOutput Query 7:")
result = g.query(query)
for row in result:
        print(row.total)