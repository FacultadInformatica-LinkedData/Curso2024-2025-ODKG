from flask import  jsonify, Blueprint, request
import requests
import json


api = Blueprint('api', __name__)


SPARQL_ENDPOINT = "http://localhost:9000/api/sparql"

# SPARQL query for retrieving charge points
SPARQL_QUERY_CHARGE_POINTS = (
    "PREFIX es: <http://eulersharp.sourceforge.net/2003/03swap/log-rules#> "
    "PREFIX vocab: <http://www.chargeAndParkMadrid.org/opendata/handsOn/group04/ontology/Ontology#> "
    "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
    "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> "
    "PREFIX base: <http://www.chargeAndParkMadrid.org/opendata/handsOn/group04/> "
    "PREFIX esadm: <http://vocab.linkeddata.es/datosabiertos/def/sector-publico/territorio#/> "
    "PREFIX esadm2: <http://vocab.linkeddata.es/datosabiertos/def/urbanismo-infraestructuras/callejero#/> "
    "SELECT ?nameCP ?nameSt WHERE { "
    "?chp rdf:type vocab:ChargePoint. "
    "?chp vocab:locatedInStreet ?street . "
    "?chp rdf:label ?nameCP . "
    "?street rdf:label ?nameSt . "
    "}"
)
# SPARQL query for retrieving parkings
SPARQL_QUERY_PARKINGS= (
    "PREFIX es: <http://eulersharp.sourceforge.net/2003/03swap/log-rules#> "
    "PREFIX vocab: <http://www.chargeAndParkMadrid.org/opendata/handsOn/group04/ontology/Ontology#> "
    "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
    "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> "
    "PREFIX base: <http://www.chargeAndParkMadrid.org/opendata/handsOn/group04/> "
    "PREFIX esadm: <http://vocab.linkeddata.es/datosabiertos/def/sector-publico/territorio#/> "
    "PREFIX esadm2: <http://vocab.linkeddata.es/datosabiertos/def/urbanismo-infraestructuras/callejero#/> "
    "SELECT ?nameP ?nameSt WHERE { "
    "?p rdf:type vocab:Parking. "
    "?p vocab:locatedInStreet ?street . "
    "?p rdf:label ?nameP . "
    "?street rdf:label ?nameSt . "
    "}"
)

# SPARQL query for retrieving districts
SPARQL_QUERY_DISTRICTS= (
    "PREFIX es: <http://eulersharp.sourceforge.net/2003/03swap/log-rules#> "
    "PREFIX vocab: <http://www.chargeAndParkMadrid.org/opendata/handsOn/group04/ontology/Ontology#> "
    "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
    "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> "
    "PREFIX base: <http://www.chargeAndParkMadrid.org/opendata/handsOn/group04/> "
    "PREFIX esadm: <http://vocab.linkeddata.es/datosabiertos/def/sector-publico/territorio#/> "
    "PREFIX esadm2: <http://vocab.linkeddata.es/datosabiertos/def/urbanismo-infraestructuras/callejero#/> "
    "SELECT ?nameD WHERE { "
    "?d rdf:type esadm:Distrito. "
    "?d rdf:label ?nameD . "
    "} ORDER BY ?nameD"
)
# SPARQL query for retrieving neighborhoods
SPARQL_QUERY_NEIGHBORHOODS = (
    "PREFIX es: <http://eulersharp.sourceforge.net/2003/03swap/log-rules#> "
    "PREFIX vocab: <http://www.chargeAndParkMadrid.org/opendata/handsOn/group04/ontology/Ontology#> "
    "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
    "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> "
    "PREFIX base: <http://www.chargeAndParkMadrid.org/opendata/handsOn/group04/> "
    "PREFIX esadm: <http://vocab.linkeddata.es/datosabiertos/def/sector-publico/territorio#/> "
    "PREFIX esadm2: <http://vocab.linkeddata.es/datosabiertos/def/urbanismo-infraestructuras/callejero#/> "
    "SELECT ?nameNeig WHERE { "
    "?n rdf:type esadm:Barrio. "
    "?n rdf:label ?nameNeig . "
    "} ORDER BY ?nameNeig"
)

# SPARQL query for retrieving neighborhoods in a disctrict
SPARQL_QUERY_NEIGHBORHOODS_WITH_DISTRICTS = (
    "PREFIX es: <http://eulersharp.sourceforge.net/2003/03swap/log-rules#>"
    "PREFIX vocab: <http://www.chargeAndParkMadrid.org/opendata/handsOn/group04/ontology/Ontology#>"
    "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>"
    "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>"
    "PREFIX base: <http://www.chargeAndParkMadrid.org/opendata/handsOn/group04/>"
    "PREFIX esadm: <http://vocab.linkeddata.es/datosabiertos/def/sector-publico/territorio#/>"
    "PREFIX esadm2: <http://vocab.linkeddata.es/datosabiertos/def/urbanismo-infraestructuras/callejero#/>"
    "SELECT ?nameNeig WHERE { "
    "?n rdf:type esadm:Barrio. "
    "?n rdf:label ?nameNeig. "
    "?d rdf:type esadm:Distrito. "
    "?d rdf:label ?nameD. "
    "?n esadm:distrito ?d. "
    "FILTER(?nameD = \"district_name\")"
    "}"
)

# SPARQL query for retrieving charge points in a disctrict
SPARQL_QUERY_DISTRICTS_CHARGING_POINTS= (
    "PREFIX es: <http://eulersharp.sourceforge.net/2003/03swap/log-rules#> "
    "PREFIX vocab: <http://www.chargeAndParkMadrid.org/opendata/handsOn/group04/ontology/Ontology#> "
    "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
    "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> "
    "PREFIX base: <http://www.chargeAndParkMadrid.org/opendata/handsOn/group04/> "
    "PREFIX esadm: <http://vocab.linkeddata.es/datosabiertos/def/sector-publico/territorio#/> "
    "PREFIX esadm2: <http://vocab.linkeddata.es/datosabiertos/def/urbanismo-infraestructuras/callejero#/> "
    "SELECT ?nameCP ?nameSt WHERE { "
    "?chp rdf:type vocab:ChargePoint. "
    "?chp vocab:locatedInStreet ?street . "
    "?chp rdf:label ?nameCP . "
    "?street rdf:label ?nameSt . "
    "?street esadm:barrio ?neighborhood ." 
    "?neighborhood esadm:distrito ?district ."
    "?district rdf:label ?nameDistr . "
    "FILTER(?nameDistr = \"district_name\")"
    "}"
)
# SPARQL query for retrieving parkings in a disctrict
SPARQL_QUERY_DISTRICTS_PARKING= (
    "PREFIX es: <http://eulersharp.sourceforge.net/2003/03swap/log-rules#> "
    "PREFIX vocab: <http://www.chargeAndParkMadrid.org/opendata/handsOn/group04/ontology/Ontology#> "
    "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
    "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> "
    "PREFIX base: <http://www.chargeAndParkMadrid.org/opendata/handsOn/group04/> "
    "PREFIX esadm: <http://vocab.linkeddata.es/datosabiertos/def/sector-publico/territorio#/> "
    "PREFIX esadm2: <http://vocab.linkeddata.es/datosabiertos/def/urbanismo-infraestructuras/callejero#/> "
    "SELECT ?nameP ?nameSt WHERE { "
    "?chp rdf:type vocab:Parking. "
    "?chp vocab:locatedInStreet ?street . "
    "?chp rdf:label ?nameP . "
    "?street rdf:label ?nameSt . "
    "?street esadm:barrio ?neighborhood ." 
    "?neighborhood esadm:distrito ?district ."
    "?district rdf:label ?nameDistr . "
    "FILTER(?nameDistr = \"district_name\")"
    "}"
)

# SPARQL query for retrieving charge points in a neighborhood
SPARQL_QUERY_NEIGHBORHOODS_CHARGING_POINTS= (
    "PREFIX es: <http://eulersharp.sourceforge.net/2003/03swap/log-rules#> "
    "PREFIX vocab: <http://www.chargeAndParkMadrid.org/opendata/handsOn/group04/ontology/Ontology#> "
    "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
    "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> "
    "PREFIX base: <http://www.chargeAndParkMadrid.org/opendata/handsOn/group04/> "
    "PREFIX esadm: <http://vocab.linkeddata.es/datosabiertos/def/sector-publico/territorio#/> "
    "PREFIX esadm2: <http://vocab.linkeddata.es/datosabiertos/def/urbanismo-infraestructuras/callejero#/> "
    "SELECT ?nameCP ?nameSt WHERE { "
    "?chp rdf:type vocab:ChargePoint. "
    "?chp vocab:locatedInStreet ?street . "
    "?chp rdf:label ?nameCP . "
    "?street rdf:label ?nameSt . "
    "?street esadm:barrio ?neighborhood ." 
    "?neighborhood rdf:label ?nameNeigh . "
    "FILTER(?nameNeigh = \"neighborhood_name\")"
    "}"
)
# SPARQL query for retrieving parking in a neighborhood
SPARQL_QUERY_NEIGHBORHOODS_PARKING= (
    "PREFIX es: <http://eulersharp.sourceforge.net/2003/03swap/log-rules#> "
    "PREFIX vocab: <http://www.chargeAndParkMadrid.org/opendata/handsOn/group04/ontology/Ontology#> "
    "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
    "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> "
    "PREFIX base: <http://www.chargeAndParkMadrid.org/opendata/handsOn/group04/> "
    "PREFIX esadm: <http://vocab.linkeddata.es/datosabiertos/def/sector-publico/territorio#/> "
    "PREFIX esadm2: <http://vocab.linkeddata.es/datosabiertos/def/urbanismo-infraestructuras/callejero#/> "
    "SELECT ?nameP ?nameSt WHERE { "
    "?chp rdf:type vocab:Parking. "
    "?chp vocab:locatedInStreet ?street . "
    "?chp rdf:label ?nameP . "
    "?street rdf:label ?nameSt . "
    "?street esadm:barrio ?neighborhood ." 
    "?neighborhood rdf:label ?nameNeigh . "
    "FILTER(?nameNeigh = \"neighborhood_name\")"
    "}"
)

# SPARQL query for retrieving details of charge points
SPARQL_QUERY_DETAIL_CHARGING_POINTS = (
    "PREFIX es: <http://eulersharp.sourceforge.net/2003/03swap/log-rules#> "
    "PREFIX vocab: <http://www.chargeAndParkMadrid.org/opendata/handsOn/group04/ontology/Ontology#> "
    "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
    "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> "
    "PREFIX base: <http://www.chargeAndParkMadrid.org/opendata/handsOn/group04/> "
    "PREFIX esadm: <http://vocab.linkeddata.es/datosabiertos/def/sector-publico/territorio#/> "
    "PREFIX esadm2: <http://vocab.linkeddata.es/datosabiertos/def/urbanismo-infraestructuras/callejero#/> "

    "SELECT ?nameCP ?nameSt ?dischargeDate ?numberOfEquipments ?listMennekesKw ?listChademoKw ?listCcsKw "
    "?nMennekesConnectors ?nChademoConnectors ?nCcsConnectors ?locationCP "
    "WHERE { "
        "?chp rdf:type vocab:ChargePoint. "
        "?chp vocab:locatedInStreet ?street. "
        "?chp rdf:label ?nameCP. "
        "?street rdf:label ?nameSt. "
        
        "OPTIONAL { ?chp vocab:dischargeDate ?dischargeDate. } "
        "OPTIONAL { ?chp vocab:numberOfEquipments ?numberOfEquipments. } "
        "OPTIONAL { ?chp vocab:mennekesKw ?listMennekesKw. } "
        "OPTIONAL { ?chp vocab:chademoKw ?listChademoKw. } "
        "OPTIONAL { ?chp vocab:ccsKw ?listCcsKw. } "
        "OPTIONAL { ?chp vocab:mennekesConnectors ?nMennekesConnectors. } "
        "OPTIONAL { ?chp vocab:chademoConnectors ?nChademoConnectors. } "
        "OPTIONAL { ?chp vocab:ccsConnectors ?nCcsConnectors. } "
        "OPTIONAL { ?chp vocab:openingHours ?openingHours. } "
        "OPTIONAL { ?chp vocab:location ?locationCP. } "

        "FILTER(?nameCP = \"chargepoint_name\")"
    "}"
)
# SPARQL query for retrieving details of parkings
SPARQL_QUERY_DETAIL_PARKING = (
    "PREFIX es: <http://eulersharp.sourceforge.net/2003/03swap/log-rules#> "
    "PREFIX vocab: <http://www.chargeAndParkMadrid.org/opendata/handsOn/group04/ontology/Ontology#> "
    "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
    "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> "
    "PREFIX base: <http://www.chargeAndParkMadrid.org/opendata/handsOn/group04/> "
    "PREFIX esadm: <http://vocab.linkeddata.es/datosabiertos/def/sector-publico/territorio#/> "
    "PREFIX esadm2: <http://vocab.linkeddata.es/datosabiertos/def/urbanismo-infraestructuras/callejero#/> "

    "SELECT ?nameP ?nameSt ?accesibility ?numberOfTotalPlaces ?openingHours "
    "WHERE { "
        "?p rdf:type vocab:Parking. "
        "?p vocab:locatedInStreet ?street. "
        "?p rdf:label ?nameP. "
        "?street rdf:label ?nameSt. "
        
        "OPTIONAL { ?p vocab:accesibility ?accesibility. } "
        "OPTIONAL { ?p vocab:numberOfTotalPlaces ?numberOfTotalPlaces. } "
        "OPTIONAL { ?p vocab:openingHours ?openingHours. } "
 
        "FILTER(?nameP = \"parking_name\")"
    "}"
)

# Endpoint for retrieving all charge points
@api.route('/api/charging_points', methods=['GET'])
def get_charging_points():
    try:
        headers = {'Accept': 'application/sparql-results+json'}
        response = requests.get(SPARQL_ENDPOINT, params={'query': SPARQL_QUERY_CHARGE_POINTS}, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()  
            return jsonify(data)    # Return the JSON response
        else:
            print("Error:", response.text)
            return jsonify({"error": "Failed to fetch data from SPARQL endpoint"}), response.status_code
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "An error occurred while processing the request"}), 500

# Endpoint for retrieving all parking locations
@api.route('/api/parkings', methods=['GET'])
def get_parkings():
    try:
        headers = {'Accept': 'application/sparql-results+json'}
        response = requests.get(SPARQL_ENDPOINT, params={'query': SPARQL_QUERY_PARKINGS}, headers=headers)
        
        if response.status_code == 200:
            data = response.json()  
            return jsonify(data)    
        else:
            print("Error:", response.text)
            return jsonify({"error": "Failed to fetch data from SPARQL endpoint"}), response.status_code
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "An error occurred while processing the request"}), 500
    
# Endpoint for retrieving coordinates of charge points
@api.route('/charging-points-coords', methods=['GET'])
def get_charging_points_coords():
    try:
        with open('static/data/madrid_charging_points_coordinates.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        return jsonify(data)  
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON"}), 500

# Endpoint for retrieving parking coordinates    
@api.route('/parking-coords', methods=['GET'])
def get_parkings_coords():
    try:
        with open('static/data/madrid_parkings_coordinates.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        return jsonify(data)  
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON"}), 500

# Endpoint for retrieving all districts
@api.route('/api/districts', methods=['GET'])
def get_districts():
    try:
        headers = {'Accept': 'application/sparql-results+json'}
        response = requests.get(SPARQL_ENDPOINT, params={'query': SPARQL_QUERY_DISTRICTS}, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            districts = [{"name": result["nameD"]["value"]} for result in data["results"]["bindings"]]
            return jsonify({"results": districts}) 
        else:
            print("Error:", response.text)
            return jsonify({"error": "Failed to fetch data from SPARQL endpoint"}), response.status_code
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "An error occurred while processing the request"}), 500

# Endpoint for retrieving charge points in a disctrict
@api.route('/api/districts-chargepoints', methods=['GET'])
def get_districts_charging_points():
    try:
        # Obtener el parámetro de distrito de la URL
        district_name = request.args.get('district')

        if district_name:
            # Incluir el nombre del distrito en la consulta SPARQL si es necesario
            # SPARQL_QUERY_DISTRICTS debe ser una consulta adaptada para filtrar por nombre de distrito
            sparql_query = SPARQL_QUERY_DISTRICTS_CHARGING_POINTS.replace("district_name", district_name)
        else:
            # Si no se proporciona un distrito, usar la consulta normal
            sparql_query = SPARQL_QUERY_DISTRICTS

        headers = {'Accept': 'application/sparql-results+json'}
        # Realizar la solicitud GET al endpoint SPARQL con la consulta en el parámetro `query`
        response = requests.get(SPARQL_ENDPOINT, params={'query': sparql_query}, headers=headers)

        # Verifica si la solicitud fue exitosa
        if response.status_code == 200:
            data = response.json()  # Obtiene la respuesta en formato JSON
            return jsonify(data)    # Devuelve el JSON al frontend
        else:
            # Si el servidor SPARQL responde con un error, registrar el error
            print("Error:", response.text)
            return jsonify({"error": "Failed to fetch data from SPARQL endpoint"}), response.status_code
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "An error occurred while processing the request"}), 500
    
# Endpoint for retrieving parkings in a disctrict
@api.route('/api/districts-parkings', methods=['GET'])
def get_districts_parkings():
    try:
        district_name = request.args.get('district')

        if district_name:
            sparql_query = SPARQL_QUERY_DISTRICTS_PARKING.replace("district_name", district_name)
        else:

            sparql_query = SPARQL_QUERY_DISTRICTS

        headers = {'Accept': 'application/sparql-results+json'}

        response = requests.get(SPARQL_ENDPOINT, params={'query': sparql_query}, headers=headers)

        if response.status_code == 200:
            data = response.json()  
            return jsonify(data)   
        else:

            print("Error:", response.text)
            return jsonify({"error": "Failed to fetch data from SPARQL endpoint"}), response.status_code
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "An error occurred while processing the request"}), 500
    
# Endpoint for retrieving all neighborhoods
@api.route('/api/neighborhoods', methods=['GET'])
def get_neighborhoods():
    try:
        
        sparql_query = SPARQL_QUERY_NEIGHBORHOODS  

        headers = {'Accept': 'application/sparql-results+json'}
        response = requests.get(SPARQL_ENDPOINT, params={'query': sparql_query}, headers=headers)

        if response.status_code == 200:
            data = response.json()  
            
            neighborhoods = [item['nameNeig']['value'] for item in data['results']['bindings']]
            return jsonify(neighborhoods)  
        else:
           
            print("Error:", response.text)
            return jsonify({"error": "Failed to fetch data from SPARQL endpoint"}), response.status_code
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "An error occurred while processing the request"}), 500

   
# Endpoint for retrieving charge points in a neighborhood
@api.route('/api/neighborhoods-chargepoints', methods=['GET'])
def get_neighborhoods_charging_points():
    try:

        neighborhood_name = request.args.get('neighborhood')

        if neighborhood_name:

            sparql_query = SPARQL_QUERY_NEIGHBORHOODS_CHARGING_POINTS.replace("neighborhood_name", neighborhood_name)

        headers = {'Accept': 'application/sparql-results+json'}
        response = requests.get(SPARQL_ENDPOINT, params={'query': sparql_query}, headers=headers)

        if response.status_code == 200:
            data = response.json()  
            return jsonify(data)    
        else:
    
            print("Error:", response.text)
            return jsonify({"error": "Failed to fetch data from SPARQL endpoint"}), response.status_code
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "An error occurred while processing the request"}), 500
    
# Endpoint for retrieving parking in a neighborhood
@api.route('/api/neighborhoods-parkings', methods=['GET'])
def get_neighborhoods_parkings():
    try:
       
        neighborhood_name = request.args.get('neighborhood')

        if neighborhood_name:
          
            sparql_query = SPARQL_QUERY_NEIGHBORHOODS_PARKING.replace("neighborhood_name", neighborhood_name)


        headers = {'Accept': 'application/sparql-results+json'}
       
        response = requests.get(SPARQL_ENDPOINT, params={'query': sparql_query}, headers=headers)


        if response.status_code == 200:
            data = response.json() 
            return jsonify(data)    
        else:
           
            print("Error:", response.text)
            return jsonify({"error": "Failed to fetch data from SPARQL endpoint"}), response.status_code
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "An error occurred while processing the request"}), 500
    
# Endpoint for retrieving the details of a charge point
@api.route('/api/chargepoint-detail', methods=['GET'])
def get_detail_charging_points():
    try:
      
        chargepoint_name = request.args.get('chargepoint')

        if chargepoint_name:
        
            sparql_query = SPARQL_QUERY_DETAIL_CHARGING_POINTS.replace("chargepoint_name", chargepoint_name)

        headers = {'Accept': 'application/sparql-results+json'}
        response = requests.get(SPARQL_ENDPOINT, params={'query': sparql_query}, headers=headers)

        
        if response.status_code == 200:
            data = response.json() 
            return jsonify(data)   
        else:
        
            print("Error:", response.text)
            return jsonify({"error": "Failed to fetch data from SPARQL endpoint"}), response.status_code
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "An error occurred while processing the request"}), 500

# Endpoint for retrieving the details of a parking
@api.route('/api/parking-detail', methods=['GET'])
def get_detail_parking():
    try:
       
        parking_name = request.args.get('parking')

        if parking_name:
            sparql_query = SPARQL_QUERY_DETAIL_PARKING.replace("parking_name", parking_name)

        headers = {'Accept': 'application/sparql-results+json'}
   
        response = requests.get(SPARQL_ENDPOINT, params={'query': sparql_query}, headers=headers)

       
        if response.status_code == 200:
            data = response.json()
            return jsonify(data)  
        else:
    
            print("Error:", response.text)
            return jsonify({"error": "Failed to fetch data from SPARQL endpoint"}), response.status_code
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "An error occurred while processing the request"}), 500

# Endpoint for retrieving the neighborhoods in a district
@api.route('/api/neighborhoods_districts', methods=['GET'])
def get_neighborhoods_with_districts():
    print("NO ENRTE")
    try:
        print("ENTRE")
       
        district_name = request.args.get('district_name')

        if district_name:
           
            sparql_query = SPARQL_QUERY_NEIGHBORHOODS_WITH_DISTRICTS.replace("district_name", district_name)

        headers = {'Accept': 'application/sparql-results+json'}
        response = requests.get(SPARQL_ENDPOINT, params={'query': sparql_query}, headers=headers)

        print(response)

       
        if response.status_code == 200:
            data = response.json() 
            
            
            neighborhoods = [item['nameNeig']['value'] for item in data['results']['bindings']]
            return jsonify(neighborhoods) 
        else:
           
            print("Error:", response.text)
            return jsonify({"error": "Failed to fetch data from SPARQL endpoint"}), response.status_code
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "An error occurred while processing the request"}), 500