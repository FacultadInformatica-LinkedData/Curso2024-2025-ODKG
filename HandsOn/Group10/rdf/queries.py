from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS, XSD

graph = Graph()

# Cargar múltiples esquemas RDF

rdf_files = ['C:/Users/salgu/OneDrive/Escritorio/UPM/Data_Science/Open_Data_and_Knowledge_Graphs/Course-Open-Data-and-Knowledge-Graphs/HandsOn/Group10/rdf/free-places-graph.nt',
             'C:/Users/salgu/OneDrive/Escritorio/UPM/Data_Science/Open_Data_and_Knowledge_Graphs/Course-Open-Data-and-Knowledge-Graphs/HandsOn/Group10/rdf/stations-graph.nt',
             'C:/Users/salgu/OneDrive/Escritorio/UPM/Data_Science/Open_Data_and_Knowledge_Graphs/Course-Open-Data-and-Knowledge-Graphs/HandsOn/Group10/rdf/trips-graph_1.nt',
             'C:/Users/salgu/OneDrive/Escritorio/UPM/Data_Science/Open_Data_and_Knowledge_Graphs/Course-Open-Data-and-Knowledge-Graphs/HandsOn/Group10/rdf/trips-graph_2.nt',
             'C:/Users/salgu/OneDrive/Escritorio/UPM/Data_Science/Open_Data_and_Knowledge_Graphs/Course-Open-Data-and-Knowledge-Graphs/HandsOn/Group10/rdf/trips-graph_3.nt',
             'C:/Users/salgu/OneDrive/Escritorio/UPM/Data_Science/Open_Data_and_Knowledge_Graphs/Course-Open-Data-and-Knowledge-Graphs/HandsOn/Group10/rdf/trips-graph_4.nt']

for rdf_file in rdf_files:
    graph.parse(rdf_file, format='nt')

# Comprobar cuántos triples hay en el grafo
print(f"Total de triples cargados: {len(graph)}")

from rdflib import Namespace

query1 = """
SELECT ?trips ?stationName ?unlockDate ?lockDate ?bikeId
WHERE {
  ?trips <https://bicimap.com/ontology#endAt> <http://bicimap.com/places/Station170> .
  <http://bicimap.com/entity/Station170> <https://schema.org/address> ?address .
  ?address <https://schema.org/streetAddress> ?stationName .
  ?trips <https://bicimap.com/ontology#unlockDate> ?unlockDate .
  ?trips <https://bicimap.com/ontology#lockDate> ?lockDate .
  ?trips <https://bicimap.com/ontology#bikeId> ?bikeId .
}
LIMIT 10
"""
results1 = graph.query(query1)
print("Trips that ended at Station170:")
for result in results1:
    trip = result[0]
    station_name = result[1]
    unlock_date = result[2]
    lock_date = result[3]
    bike_id = result[4]
    print(f"Trip: {trip}, Station name: {station_name}, Start time: {unlock_date}, End time: {lock_date}, Bike id: {bike_id}")

query2 = """
SELECT ?trips ?stationName ?unlockDate ?lockDate ?bikeId
WHERE {
  ?trips <https://bicimap.com/ontology#endAt> <http://bicimap.com/places/FreePlace715> .
  <http://bicimap.com/entity/FreePlace715> <https://schema.org/address> ?address .
  ?address <https://schema.org/streetAddress> ?stationName .
  ?trips <https://bicimap.com/ontology#unlockDate> ?unlockDate .
  ?trips <https://bicimap.com/ontology#lockDate> ?lockDate .
  ?trips <https://bicimap.com/ontology#bikeId> ?bikeId .
}
LIMIT 10
"""
results2 = graph.query(query2)
print("Trips that ended at FreePlace715:")
for result in results2:
    trip = result[0]
    free_place_address = result[1]
    unlock_date = result[2]
    lock_date = result[3]
    bike_id = result[4]
    print(f"Trip: {trip}, Free place Address: {free_place_address}, Start time: {unlock_date}, End time: {lock_date}, Bike id: {bike_id}")


query3 = """

SELECT ?trips ?stationName ?unlockDate ?bikeId
WHERE {
  ?trips <https://bicimap.com/ontology#startAt> <http://bicimap.com/places/Station170> .
  <http://bicimap.com/entity/Station170> <https://schema.org/address> ?address .
  ?address <https://schema.org/streetAddress> ?stationName .
  ?trips <https://bicimap.com/ontology#unlockDate> ?unlockDate .
  ?trips <https://bicimap.com/ontology#bikeId> ?bikeId .
   
  FILTER (SUBSTR(STR(?unlockDate), 1, 10) = "2023-02-07")
}
LIMIT 10
"""
results3 = graph.query(query3)
print("Trips on the 2023-02-07:")
for result in results3:
    trip = result[0]
    start_address = result[1]
    unlock_date = result[2]
    bike_id = result[3]
    print(f"Trip: {trip}, Free place Address: {start_address}, Start time: {unlock_date},  Bike id: {bike_id}")

query4 = """

SELECT ?trips ?station ?unlockDate ?lockDate ?bikeId
WHERE {
  ?trips <https://bicimap.com/ontology#lockDock> ?lockDock .
  ?trips <https://bicimap.com/ontology#startAt> ?station .
  ?trips <https://bicimap.com/ontology#unlockDate> ?unlockDate .
  ?trips <https://bicimap.com/ontology#lockDate> ?lockDate .
  ?trips <https://bicimap.com/ontology#bikeId> ?bikeId .

  FILTER (SUBSTR(STR(?lockDock), 1, 2) = "24")
}
LIMIT 10
"""
results4 = graph.query(query4)
print("Trips with lockDock 24:")
for result in results4:
    trip = result[0]
    start_station = result[1]
    unlock_date = result[2]
    lock_date = result[3]
    bike_id = result[4]
    print(f"Trip: {trip}, Start Station: {start_station}, Start time: {unlock_date}, End Time: {lock_date}, Bike id: {bike_id}")


query5 = """
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?trips ?station ?unlockDate ?lockDate ?bikeId
WHERE {
  ?trips <https://bicimap.com/ontology#startAt> ?station .
  ?trips <https://bicimap.com/ontology#unlockDate> ?unlockDate .
  ?trips <https://bicimap.com/ontology#lockDate> ?lockDate .
  ?trips <https://bicimap.com/ontology#bikeId> ?bikeId .

  FILTER (?bikeId = "33"^^xsd:integer)
}
LIMIT 10
"""
results5 = graph.query(query5)
print("Trips with bikeId 33:")
for result in results5:
    trip = result[0]
    start_station = result[1]
    unlock_date = result[2]
    lock_date = result[3]
    bike_id = result[4]
    print(f"Trip: {trip}, Start Station: {start_station}, Start time: {unlock_date}, End Time: {lock_date}, Bike id: {bike_id}")



