import streamlit as st
import rdflib
import folium
from streamlit_folium import st_folium
import requests
from io import BytesIO

# URL del archivo RDF en GitHub
RDF_URL = "https://raw.githubusercontent.com/julianlopez-code/Curso2024-2025-ODKG/refs/heads/HO5-Group11-updated/HandsOn/Group11/rdf/dataset-with-links.ttl"

response = requests.get(RDF_URL)
rdf_data = BytesIO(response.content)

g = rdflib.Graph()
g.parse(rdf_data, format="turtle")

OPENCAGE_API_KEY = ''  # replace with opencage api key 

def geocode_address(address):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={address}&key={OPENCAGE_API_KEY}&language=es"
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200 and data['results']:
        location = data['results'][0]['geometry']
        return (location['lat'], location['lng'])
    else:
        return None

districts_query = """
PREFIX ns: <https://datos.madrid/estaciones_carga_vehiculos_electricos/ontology#>

SELECT DISTINCT ?district
WHERE {
    ?s a ns:District ;
        ns:districtName ?district .
}
"""

districts_results = g.query(districts_query)
districts = sorted([str(row.district) for row in districts_results]) 

st.title("Map of Charging Stations for Electric Vehicles in Madrid")

selected_district = st.selectbox("Select a district:", ["All Districts"] + districts)

if selected_district:
    st.info("Searching for charging stations...")

query = f"""
PREFIX ns: <https://datos.madrid/estaciones_carga_vehiculos_electricos/ontology#>

SELECT ?idPoint ?additionalInfo ?operator ?numberOfDevices ?placement ?address ?neighname ?district
       ?characteristicsDevices ?management ?schedule ?state
WHERE {{
    ?station a ns:ChargingStation ;
             ns:idPoint ?idPoint ;
             ns:additionalInfo ?additionalInfo ;
             ns:operator ?operator ;
             ns:numberOfDevices ?numberOfDevices ;
             ns:placement ?placement ;
             ns:characteristicsDevices ?characteristicsDevices ;
             ns:management ?management ;
             ns:schedule ?schedule ;
             ns:state ?state ;
             ns:isLocated ?location .
    ?location a ns:Location ;
              ns:address ?address ;
              ns:containedInNeighborhood ?neigh .
    ?neigh a ns:Neighborhood ; 
            ns:containedInDistrict ?district_code ;
            ns:neighborhoodName ?neighname .
    ?district_code ns:districtName ?district .

    FILTER (str(?district) = "{selected_district}" || "{selected_district}" = "All Districts")
}}
"""

results = g.query(query)

if not results:
    st.warning("Couldn't find charging stations for the selected district.")
else:
    madrid_coords = (40.4168, -3.7038)
    m = folium.Map(location=madrid_coords, zoom_start=12)
    station_count = 0

    for row in results:
        id_point = row.idPoint
        additional_info = row.additionalInfo
        operator = row.operator
        number_of_devices = row.numberOfDevices
        placement = row.placement
        address = row.address
        neighborhood = row.neighname
        district = row.district
        characteristics = row.characteristicsDevices
        management = row.management
        schedule = row.schedule
        state = row.state

        addressGeo = address + ", Madrid, Spain"
        coords = geocode_address(addressGeo)
        if coords:
            folium.Marker(
                coords,
                popup=(
                    f"<b>ID:</b> {id_point}<br>"
                    f"<b>Address:</b> {address}<br>"
                    f"<b>Additional info:</b> {additional_info}<br>"
                    f"<b>Operator:</b> {operator}<br>"
                    f"<b>Devices:</b> {number_of_devices}<br>"
                    f"<b>Location:</b> {placement}<br>"
                    f"<b>Characteristics:</b> {characteristics}<br>"
                    f"<b>Management:</b> {management}<br>"
                    f"<b>Schedule:</b> {schedule}<br>"
                    f"<b>State:</b> {state}<br>"
                    f"<b>Neighborhood:</b> {neighborhood if neighborhood else 'Not available'}<br>"
                    f"<b>District:</b> {district if district else 'Not available'}"
                ),
            ).add_to(m)
            station_count += 1

    st.success(f"Found {station_count} charging stations.")
    st_folium(m, width=700, height=500)
