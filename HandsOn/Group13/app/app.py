from flask import Flask, jsonify, g, request
import rdflib
from flask_cors import CORS  # Importar CORS
#python app.py
app = Flask(__name__)
CORS(app)  # Habilitar CORS para toda la aplicación

# Cargar el grafo RDF en memoria
@app.before_request
def load_graph():
    g.graph = rdflib.Graph()
    g.graph.parse("CCTV-via-publica-updated-with-links.ttl", format="ttl")

@app.route('/api/locations', methods=['GET'])
def get_locations():
    locations = set()
    for camera in g.graph.subjects(rdflib.RDF.type, rdflib.URIRef("http://CamaraMadrid.org/Camera")):
        location = g.graph.value(camera, rdflib.URIRef("http://CamaraMadrid.org/location"))
        if location:
            locations.add(location)

    return jsonify(list(locations))

@app.route('/api/cameras', methods=['GET'])
def get_cameras():
    location = request.args.get('location')
    cameras = []
    type_count = {}
    resolution_count = {}
    zoom_count = {}

    for camera in g.graph.subjects(rdflib.RDF.type, rdflib.URIRef("http://CamaraMadrid.org/Camera")):
        cam_location = g.graph.value(camera, rdflib.URIRef("http://CamaraMadrid.org/location"))
        if cam_location and str(cam_location) == location:  # Convertir a string para la comparación
            camera_data = {
                'id': camera.split('/')[-1],
                'type': str(g.graph.value(camera, rdflib.URIRef("http://CamaraMadrid.org/type"))),
                'resolution': str(g.graph.value(camera, rdflib.URIRef("http://CamaraMadrid.org/resolution"))),
                'zoom': str(g.graph.value(camera, rdflib.URIRef("http://CamaraMadrid.org/opticalZoom"))),
                'year': str(g.graph.value(camera, rdflib.URIRef("http://CamaraMadrid.org/acquisitionYear"))),
            }
            cameras.append(camera_data)

            # Contar por tipo
            if camera_data['type'] in type_count:
                type_count[camera_data['type']] += 1
            else:
                type_count[camera_data['type']] = 1

            # Contar por resolución
            if camera_data['resolution'] in resolution_count:
                resolution_count[camera_data['resolution']] += 1
            else:
                resolution_count[camera_data['resolution']] = 1

            # Contar por zoom
            if camera_data['zoom'] in zoom_count:
                zoom_count[camera_data['zoom']] += 1
            else:
                zoom_count[camera_data['zoom']] = 1

    # Regresar tanto las cámaras como los recuentos
    return jsonify({
        'cameras': cameras,
        'type_count': type_count,
        'resolution_count': resolution_count,
        'zoom_count': zoom_count
    })


if __name__ == '__main__':
    app.run(debug=True)
