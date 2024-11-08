from rdflib import Graph
from flask import Flask, render_template, request, flash, redirect, url_for
import folium
import os
from pyproj import Proj, Transformer

# Load RDF data
g = Graph()
g.parse("C:/Users/34629/Documents/MASTER/Open Data/APPLICATION/APP2/Group08/rdf/Grupo8-updated.ttl", format="ttl")

# Define a function to query data by date and district
def query_accidents(date, district):
    query = f"""
    PREFIX ns1: <http://madridcityheatmap.org/group08/accidentalidad#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT ?coordenada_x_utm ?coordenada_y_utm
    WHERE {{
    ?accidente a ns1:Accidente ;
                ns1:pertenceADistrito ?distrito ;
                ns1:fecha ?fecha ;
                ns1:coordenada_x_utm ?coordenada_x_utm ;
                ns1:coordenada_y_utm ?coordenada_y_utm .
                
    ?distrito ns1:codigo_distrito ?codigo_distrito .
    
    FILTER(?codigo_distrito = {district}) 
    FILTER(?fecha = "{date}"^^xsd:dateTime)
    }}
    """

    prefixes = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX ex: <http://example.org#>
    """

    default_query = f"""
    SELECT ?coordenada_x_utm ?coordenada_y_utm
    WHERE {{
        ?accidente ns1:pertenceADistrito ?distrito .
        ?accidente ns1:fecha "{date}"^^xsd:dateTime .
        ?distrito ns1:codigo_distrito {district} .
        ?accidente ns1:coordenada_x_utm ?coordenada_x_utm .
        ?accidente ns1:coordenada_y_utm ?coordenada_y_utm .
    }}
    """

    print("DEFAULT QUERY***",default_query)

    results = g.query( default_query)

    # Print each coordinate pair for debugging
    for row in results:
        print((float(row.coordenada_x_utm), float(row.coordenada_y_utm)))
    return [(float(row.coordenada_x_utm), float(row.coordenada_y_utm)) for row in results]

def utm_to_latlon(coordinates, zone, hemisphere='N'):
    """
    Convierte coordenadas UTM a latitud y longitud.
    
    Parámetros:
    - coordinates (tuple): Tupla con las coordenadas UTM (x, y).
    - zone (int): Número de la zona UTM.
    - hemisphere (str): 'N' para hemisferio norte o 'S' para hemisferio sur.
    
    Retorno:
    - tuple: (latitud, longitud) en grados decimales.
    """
    # Determinar si está en el hemisferio sur
    is_south = hemisphere == 'S'
    
    # Crear el proyector para el sistema UTM en la zona dada
    utm_proj = Proj(proj="utm", zone=zone, ellps="WGS84", south=is_south)
    wgs84_proj = Proj(proj="latlong", datum="WGS84")

    # Crear un transformador para convertir de UTM a lat/long
    transformer = Transformer.from_proj(utm_proj, wgs84_proj)

    # Desempaquetar las coordenadas UTM
    x_utm, y_utm = coordinates

    # Convertir UTM a latitud y longitud
    lon, lat = transformer.transform(x_utm, y_utm)
    return lat, lon

def is_valid_District(cadena):
    # Comprobamos si la cadena es un número
    if str(cadena).isdigit():
        code = int(cadena)
        # Comprobamos si el número está entre 1 y 21
        if 1 <= code <= 21:
            return True
    return False





# MAIN APP

# Create the Flask app
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necesario para usar `flash`

@app.route("/", methods=["GET", "POST"])
def index():
    # Get date and district from the form, with default values
    date = request.form.get("date", "2024-04-01")
    district = request.form.get("district", 1)

    if(not is_valid_District(district)):
        flash('El código no es válido. Debe ser un número entre 1 y 21.', 'error')
        return redirect(url_for('index'))
    else:
        # Query accident data and generate map
        accident_data = query_accidents(date+"T00:00:00+00:00", district)
        map_center = [40.4168, -3.7038]  # Coordinates for Madrid
        accident_map = folium.Map(location=map_center, zoom_start=12)

        # Add accident markers
        print("\nCOORDENATES")

        for x_utm, y_utm in accident_data:
            lat, lon = utm_to_latlon((x_utm,y_utm), zone=30)   # Zona UTM para Madrid
            print(f"Latitud: {lat}, Longitud: {lon}")
            # folium.CircleMarker([lat, lon], radius=5, color="red").add_to(accident_map)
            folium.Marker(
                location=[lat, lon],
                popup="Accident",
                icon=folium.Icon(color="red")
            ).add_to(accident_map)

        # Optional: Add a default test marker if no data is returned+
        if not accident_data:
            print("There are no accidents...")
            folium.Marker([40.4168, -3.7038], popup="Madrid Center").add_to(accident_map)

        # Save the map to the static folder
        try:
            accident_map.save("C:/Users/34629/Documents/MASTER/Open Data/APPLICATION/APP2/Group08/app/static/map.html")
            print("Map saved successfully to static/map.html")
        except Exception as e:
            print("Failed to save map:", e)

    # Render the index.html template
    return render_template("index.html", date=date, district=district)

# Run the app
if __name__ == "__main__":
    # Check if the static directory exists, and create it if it doesn’t
    if not os.path.exists("static"):
        os.makedirs("static")
    app.run(debug=True)
