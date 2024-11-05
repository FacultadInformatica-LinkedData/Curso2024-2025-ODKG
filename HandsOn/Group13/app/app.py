from flask import Flask, jsonify, g, request, render_template
import rdflib
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilitar CORS para toda la aplicación

# Cargar el grafo RDF en memoria
@app.before_request
def load_graph():
    g.graph = rdflib.Graph()
    g.graph.parse("CCTV-via-publica-updated-with-links.ttl", format="ttl")

@app.route('/')
def index():
    return render_template('index.html')  # Renderiza index.html



@app.route('/api/locations', methods=['GET'])
def get_locations():
    locations = set()
    headers = {'Accept': 'application/json'}
    url_locations='http://localhost:7200/repositories/Group13?query=PREFIX%20schema%3A%20%3Chttp%3A%2F%2Fschema.org%2F%3E%20%20SELECT%20DISTINCT%20%3Flocation%20WHERE%20%7B%20%20%20%20%20%3Fcamera%20a%20%3Chttp%3A%2F%2Fcamaras.madrid.org%2Fresources%2FCamera%3E%20%3B%20%20%20%20%20%20%20%20%20%20%20%20%20schema%3Alocation%20%3Flocation%20.%20%7D'
    response = requests.get(url_locations,headers=headers)
    rjson = response.json()
    locations_list = [item['location']['value'] for item in rjson['results']['bindings']]

    for location in locations_list:
        location_cleaned = location.replace('http://camaras.madrid.org/resources/Location/','')
        locations.add(location_cleaned)

    print(locations)
    return jsonify(list(locations))

@app.route('/api/cameras', methods=['GET'])
def get_cameras():
    location = request.args.get('location')
    cameras = []
    type_count = {}
    resolution_count = {}
    zoom_count = {}
    base_url_camera_info = 'http://localhost:7200/repositories/Group13?query=PREFIX%20schema%3A%20%3Chttp%3A%2F%2Fschema.org%2F%3E%20PREFIX%20rdf%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F1999%2F02%2F22-rdf-syntax-ns%23%3E%20%20SELECT%20%3Fid%20%3Ftype%20%3Fresolution%20%3Fzoom%20%3Fyear%20WHERE%20%7B%20%20%20%20%20%3Fid%20a%20%3Chttp%3A%2F%2Fcamaras.madrid.org%2Fresources%2FCamera%3E%20%3B%20%20%20%20%20%20%20%20%20%20rdf%3Atype%20%3Ftype%20%3B%20%20%20%20%20%20%20%20%20%20schema%3Alocation%20%3Chttp%3A%2F%2Fcamaras.madrid.org%2Fresources%2FLocation%2FCUSTOM_LOCATION%3E%20%3B%20%20%20%20%20%20%20%20%20%20schema%3Aresolution%20%3Fresolution%20%3B%20%20%20%20%20%20%20%20%20%20schema%3AopticalZoom%20%3Fzoom%20%3B%20%20%20%20%20%20%20%20%20%20schema%3AacquisitionYear%20%3Fyear%20.%20%20%20%20%20FILTER%28isLiteral%28%3Ftype%29%29%20%7D'
    final_url = base_url_camera_info.replace("CUSTOM_LOCATION", location)
    headers = {'Accept': 'application/json'}
    response = requests.get(final_url,headers=headers)
    rjson = response.json()
    camera_info = [item for item in rjson['results']['bindings']]

    for camera in camera_info:
        camera_data = {
            'id': camera['id']['value'].split('/')[-1],
            'type': camera['type']['value'],
            'resolution': camera['resolution']['value'],
            'zoom': camera['zoom']['value'],
            'year': camera['year']['value'].split('/')[-1],
        }
        cameras.append(camera_data)
        if camera_data['type'] in type_count:
            type_count[camera_data['type']] += 1
        else:
            type_count[camera_data['type']] = 1

        if camera_data['resolution'] in resolution_count:
            resolution_count[camera_data['resolution']] += 1
        else:
            resolution_count[camera_data['resolution']] = 1

        if camera_data['zoom'] in zoom_count:
            zoom_count[camera_data['zoom']] += 1
        else:
            zoom_count[camera_data['zoom']] = 1



    return jsonify({
        'cameras': cameras,
        'type_count': type_count,
        'resolution_count': resolution_count,
        'zoom_count': zoom_count
    })


if __name__ == '__main__':
    app.run(debug=True)
