import zipfile
import pickle
from rdflib import Graph

zip_filename = 'graph-with-links.ttl.zip'
ttl_filename = 'graph.ttl'
pickle_filename = 'graph.pkl'

try:
    with open(pickle_filename, 'rb') as f:
        g = pickle.load(f)
    print("Graph loaded from Pickle file.")

except FileNotFoundError:
    print("Pickle file not found. Loading Graph from TTL file in ZIP...")
    with zipfile.ZipFile(zip_filename, 'r') as zip_file:
        with zip_file.open(ttl_filename) as ttl_file:
            g = Graph()
            g.parse(ttl_file, format="ttl")

    with open(pickle_filename, 'wb') as f:
        pickle.dump(g, f)
    print("Graph saved in Pickle File.")

print(f"Graph loaded with {len(g)} triples.")


query_classes = """
SELECT DISTINCT ?class
WHERE {
  ?instance a ?class .
}
LIMIT 10
"""

for row in g.query(query_classes):
    print(f"Class found: {row['class']}")

query_properties = """
SELECT DISTINCT ?property
WHERE {
  ?s ?property ?o .
}
LIMIT 10
"""

for row in g.query(query_properties):
    print(f"Property found: {row['property']}")


query_trips = """
SELECT DISTINCT ?trips
WHERE {
  ?trips a <https://BiciMad.es/ontology#BikeTrip> .
}
LIMIT 10
"""

for row in g.query(query_trips):
    print(f"Trip found: {row['trips']}")



query_stations= """
SELECT DISTINCT ?stations
WHERE {
  ?stations a <https://BiciMad.es/ontology#BikeStation> .
}
LIMIT 10
"""
for row in g.query(query_stations):
    print(f"Station found: {row['stations']}")

query_distric= """

PREFIX bici: <https://BiciMad.es/ontology#>
PREFIX schema: <https://schema.org/>

SELECT ?station
WHERE {
  ?station a bici:BikeStation .
  ?station schema:address ?address .
  ?address schema:containedInPlace <http://www.BiciMad.es/entity/Place/Centro> .
}
LIMIT 10
"""
for row in g.query(query_distric):
    station = row['station']
    print(f"Stations in Centro: {station}")


query_freePlaces_in_postalCode= """

PREFIX schema: <https://schema.org/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?freePlace ?postalCode
WHERE {
    ?freePlace a schema:Place .
    ?freePlace schema:address ?address .
    ?address schema:postalCode ?postalCode .
    ?freePlace schema:id ?freePlaceId . 
    FILTER(?postalCode= "28050"^^xsd:int) 
}
LIMIT 10
"""

for row in g.query(query_freePlaces_in_postalCode):
    freePlace = row['freePlace']
    postalCode = row['postalCode']
    print(f"freePlace in 28050: {freePlace} {postalCode}")

query1 = """

PREFIX schema: <https://schema.org/>
PREFIX bici: <https://BiciMad.es/ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT ?trips ?stationName ?unlockDate ?lockDate ?bikeId ?stationId
WHERE {
  ?trips bici:endAt ?station .
  ?station schema:id ?stationId .
  ?station schema:address ?address .
  ?address schema:streetAddress ?stationName .
  ?trips bici:unlockDate ?unlockDate .
  ?trips bici:lockDate ?lockDate .
  ?trips bici:bikeId ?bikeId .
  
  FILTER(?stationId = "Station170"^^xsd:string)
}
LIMIT 10
"""
results1 = g.query(query1)
print("Trips that ended at Station170:")
for result in results1:
    trip = result[0]
    station_name = result[1]
    unlock_date = result[2]
    lock_date = result[3]
    bike_id = result[4]
    station_id = result[5]
    print(
        f"Trip: {trip}, Station name: {station_name}, Start time: {unlock_date}, End time: {lock_date}, Bike id: {bike_id}, Station Id: {station_id}")

query2 = """

PREFIX schema: <https://schema.org/>
PREFIX bici: <https://BiciMad.es/ontology#>
SELECT ?trips ?stationName ?unlockDate ?bikeId
WHERE {
  ?trips bici:startAt ?station .
  ?station schema:id ?stationId .
  ?station schema:address ?address .
  ?address schema:streetAddress ?stationName .
  ?trips bici:unlockDate ?unlockDate .
  ?trips bici:bikeId ?bikeId .

  FILTER (SUBSTR(STR(?unlockDate), 1, 10) = "2023-02-07")
}
LIMIT 10
"""
results2 = g.query(query2)
print("Trips on the 2023-02-07:")
for result in results2:
    trip = result[0]
    start_address = result[1]
    unlock_date = result[2]
    bike_id = result[3]
    print(f"Trip: {trip}, Free place Address: {start_address}, Start time: {unlock_date},  Bike id: {bike_id}")

query3 = """

PREFIX bici: <https://BiciMad.es/ontology#>
SELECT ?trips ?station ?unlockDate ?lockDate ?bikeId
WHERE {
  ?trips bici:lockDock ?lockDock .
  ?trips bici:startAt ?station .
  ?trips bici:unlockDate ?unlockDate .
  ?trips bici:lockDate ?lockDate .
  ?trips bici:bikeId ?bikeId .

  FILTER (SUBSTR(STR(?lockDock), 1, 2) = "24")
}
LIMIT 10
"""
results3 = g.query(query3)
print("Trips with lockDock 24:")
for result in results3:
    trip = result[0]
    start_station = result[1]
    unlock_date = result[2]
    lock_date = result[3]
    bike_id = result[4]
    print(
        f"Trip: {trip}, Start Station: {start_station}, Start time: {unlock_date}, End Time: {lock_date}, Bike id: {bike_id}")

query4 = """

PREFIX bici: <https://BiciMad.es/ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?trips ?station ?unlockDate ?lockDate ?bikeId
WHERE {
  ?trips bici:startAt ?station .
  ?trips bici:unlockDate ?unlockDate .
  ?trips bici:lockDate ?lockDate .
  ?trips bici:bikeId ?bikeId .

  FILTER (?bikeId = "33"^^xsd:integer)
}
LIMIT 10
"""
results4 = g.query(query4)
print("Trips with bikeId 33:")
for result in results4:
    trip = result[0]
    start_station = result[1]
    unlock_date = result[2]
    lock_date = result[3]
    bike_id = result[4]
    print(
        f"Trip: {trip}, Start Station: {start_station}, Start time: {unlock_date}, End Time: {lock_date}, Bike id: {bike_id}")
