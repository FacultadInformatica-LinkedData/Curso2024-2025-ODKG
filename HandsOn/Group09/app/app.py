import streamlit as st
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import folium
import datetime
from streamlit_folium import folium_static
from PIL import Image

# App favicon
favi = Image.open('images/mAIRdrid.ico')

# URL del endpoint de GraphDB
sparql = SPARQLWrapper("http://localhost:7200/repositories/Prueba")

# Título de la app
st.set_page_config(
    page_icon = favi,
)
st.title("mAIRdrid: Madrid Air Quality")

# CSS para el fondo de la aplicación y las tablas
st.markdown(
    """
    <style>
    /* Fondo de la aplicación */
    .stApp {
        background-image: url('https://media.traveler.es/photos/613763cc70e3cff8b85f81af/master/w_1600,c_limit/180966.jpg');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    /* Fondo blanco semi-transparente para las tablas */
    .dataframe {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 8px;
        padding: 10px;
    }
    
    /* Opcional: Mejorar la apariencia de las tablas */
    table {
        border-collapse: collapse;
        width: 100%;
    }
    
    th, td {
        text-align: left;
        padding: 8px;
    }
    
    th {
        background-color: #f2f2f2;
    }
    </style>
    """,
    unsafe_allow_html=True
)

isMapNotShown=True

# Lista de consultas
queries = {
    "Query 1: Give all the stations and their IDs": """
        SELECT ?StationLocation ?StationID (STRAFTER(STR(?Sensor), "#") AS ?SensorName) WHERE {
            ?Subject <http://www.w3.org/2000/01/rdf-schema#label> ?StationLocation.
            FILTER(LANG(?StationLocation) = "es")
            ?Subject <http://mAIRdrid.org/ontology/nationalStationID> ?StationID.
    
            # Obtener los sensores asociados a cada estación mediante ssn:hasSubSystem
            ?Subject <http://www.w3.org/ns/ssn/hasSubSystem> ?Sensor.
        }
    """,
    "Query 2: Give numeric values of the meditions": """
        SELECT ?Medition ?Value WHERE {
            ?Medition <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://qudt.org/schema/qudt#QuantityValue> .
            FILTER(STRSTARTS(STR(?Medition), "http://mAIRdrid.org/resources/Station/28079004/2023-01-01#")).
            ?Medition <http://qudt.org/schema/qudt#numericValue> ?Value.
        }
        LIMIT 10
    """,
    "Query 3: Give all sensors' location labels": """
        SELECT ?Station ?Location WHERE {
            ?Station <http://www.w3.org/2000/01/rdf-schema#label> ?Location.
            FILTER(LANG(?Location) = "es" && STRENDS(STR(?Station), "Location"))
        }
    """,
    "Query 4: Give all the stations with their altitude, latitude and longitude": """
        SELECT (STRBEFORE(STRAFTER(str(?Subject), "resources/"), "#") as ?StationID) ?StationLocation ?Altitude ?Latitude ?Longitude WHERE {
            ?Subject <http://www.w3.org/2000/01/rdf-schema#label> ?StationLocation.
		    FILTER(STRBEFORE(STRAFTER(str(?Subject), "resources/"), "#") != "")
            FILTER(LANG(?StationLocation) = "es")
            ?Subject <http://www.w3.org/2003/01/geo/wgs84_pos#alt> ?Altitude.
            ?Subject <http://www.w3.org/2003/01/geo/wgs84_pos#lat> ?Latitude.
            ?Subject <http://www.w3.org/2003/01/geo/wgs84_pos#long> ?Longitude.
        }
    """,
    "Query 5: Give stations and their Wikidata links": """
        SELECT ?StationLocation ?WikidataLink WHERE {
            ?Subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://mAIRdrid.org/ontology/Location>.
            ?Subject <http://www.w3.org/2000/01/rdf-schema#label> ?StationLocation.
            FILTER(LANG(?StationLocation) = "es")
            ?Subject <http://www.w3.org/2002/07/owl#sameAs> ?WikidataLink.
        }
    """,
    "Query 6: Sensors with units reconciled with WikiData": """
        SELECT ?Sensor ?WikidataLink WHERE {
            ?Subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://mAIRdrid.org/ontology/AirQualityMetric>.
            ?Subject <http://www.w3.org/2000/01/rdf-schema#label> ?Sensor.
            FILTER(LANG(?Sensor) = "es")
            ?Subject <http://www.w3.org/2002/07/owl#sameAs> ?WikidataLink.
        }
    """
}

def customQuery():
    if(st.session_state.metric != "All"):
        metricPrefixes = "PREFIX ssn: <http://www.w3.org/ns/ssn/>"
        metricOutput = "?ObservableProperty"
        metricConstraint = "?Subject ssn:hasProperty ?ObservableProperty."
        metricFilter = 'FILTER(regex(str(?ObservableProperty), CONCAT(STRAFTER(STRBEFORE(str(?Subject), "#"), "resources/Station/"), "#", "' + st.session_state.metric + '") ) )'
    else:
        metricPrefixes = ""
        metricOutput = ""
        metricConstraint = ""
        metricFilter = ""

    executeQueryAndRepresent("""
        """ + metricPrefixes + """

        SELECT (STRBEFORE(STRAFTER(str(?Subject), "resources/"), "#") as ?StationID) ?StationLocation ?Altitude ?Latitude ?Longitude """ + metricOutput + """ WHERE {
            ?Subject <http://www.w3.org/2000/01/rdf-schema#label> ?StationLocation.
		    FILTER(STRBEFORE(STRAFTER(str(?Subject), "resources/"), "#") != "")
            FILTER(LANG(?StationLocation) = "es")
            """ + metricConstraint + """
            """ + metricFilter + """
            ?Subject <http://www.w3.org/2003/01/geo/wgs84_pos#alt> ?Altitude.
            ?Subject <http://www.w3.org/2003/01/geo/wgs84_pos#lat> ?Latitude.
            ?Subject <http://www.w3.org/2003/01/geo/wgs84_pos#long> ?Longitude.
        }
    """, st.session_state.mapIniDate.strftime('%Y-%m-%d'), st.session_state.metric)

def updateMetric():
    customQuery()

def updateDateRange():
    customQuery()

def updateDateSelectors():
    customQuery()

def relevantStationsColumnToString(stationIDiterator):
    resultString = "('" + next(stationIDiterator)[1]['StationID'] + "'"
    for index, row in stationIDiterator:
        resultString = resultString + ",'" + row['StationID'] + "'"
    return resultString + ")"

def showMap(data, dateString, metricString):
    df = pd.DataFrame(data)
    df["Latitude"] = df["Latitude"].astype(float)
    df["Longitude"] = df["Longitude"].astype(float)
    df["Altitude"] = df["Altitude"].astype(float)
    stationIDs = relevantStationsColumnToString(df.iterrows())
    
    if(metricString != "All"):
        metricFilter = """FILTER(regex(str(?Observation), '""" + metricString + """') )"""
    else:
        metricFilter = ""

    valuesQuery = """
        PREFIX ssn: <http://www.w3.org/ns/ssn/>
        PREFIX sosa: <http://www.w3.org/ns/sosa/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ns1: <http://qudt.org/schema/qudt#>

        SELECT distinct (STRBEFORE(STRAFTER(str(?Observation), "resources/Station/"), "/") as ?StationID) (STRAFTER(str(?Observation), "#") as ?Metric) ?Value WHERE {
            ?Observation a sosa:Observation.
   		    FILTER(STRBEFORE(STRAFTER(str(?Observation), "resources/Station/"), "/") IN """ + stationIDs + """ )
    		FILTER(regex(str(?Observation), '""" + dateString + """') )
            """ + metricFilter + """
            ?Observation sosa:hasResult ?Result.
            ?Result ns1:numericValue ?Value.
      	} order by asc(?Observation)
    """

    sparql.setQuery(valuesQuery)
    sparql.setReturnFormat(JSON)

    valuesData = []

    try:
        # Ejecuta la consulta y obtiene resultados
        valuesResults = sparql.query().convert()
        
        # Procesa los resultados
        variables = valuesResults["head"]["vars"]
        for result in valuesResults["results"]["bindings"]:
            row = {var: result[var]['value'] for var in variables if var in result}
            valuesData.append(row)

    except Exception as e:
        st.error(f"Error al ejecutar la consulta: {e}")

    vdf = pd.DataFrame(valuesData)
    vdf = vdf.set_index('StationID')

    # Crear el mapa centrado en la media de las ubicaciones
    map_center = [df["Latitude"].mean(), df["Longitude"].mean()]
    m = folium.Map(location=map_center, zoom_start=12)

    # Añadir marcadores para cada estación con información adicional en el tooltip
    for _, row in df.iterrows():
        tooltip_text = f"<div style = 'display:flex;flex-direction:column;'><span>{row['StationLocation']}</span>" + f"<span><ul><li>Latitud: {row['Latitude']}</li>"
        tooltip_text = tooltip_text + f"<li>Longitud: {row['Longitude']}</li>" + f"<li>Altitud: {row['Altitude']} m</li></ul></span>"
        tooltip_text = tooltip_text + f"<span>Medidas para el {dateString}:</span><span><ul>"
        for index, vRow in vdf.iterrows():
            if index == row['StationID']:
                tooltip_text = tooltip_text + f"<li><b>{vRow['Metric']}</b>: <i style = 'font-weight:bold;color:#666666;'>{float(vRow['Value'])} μg/m3</i></li>"
        tooltip_text = tooltip_text + "</ul></span></div>"

        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=row["StationLocation"],
            tooltip=tooltip_text
        ).add_to(m)
    
    folium_static(m)
    
    today = datetime.datetime.now()
    this_year = today.year
    last_year = today.year - 1
    resetIniDate = datetime.date(last_year, 1, 1)
    resetEndDate = datetime.date(this_year, 8, 31)

    st.sidebar.selectbox('Metrics', ['All', 'BTX', 'CO', 'NO', 'NO2', 'NOx', 'O3', 'PM10', 'PM2.5', 'SO2'], 0, on_change=updateMetric, key='metric')
    # st.sidebar.radio('Dates', ['Specific', 'Range'], on_change=updateDateSelectors, key='dateInputType')
    # if(st.session_state.dateInputType == "Range"):
    #     disableEndDate = False
    # else:
    #     disableEndDate = True

    st.sidebar.date_input('Date',
        value=resetIniDate,
        min_value=resetIniDate,
        max_value=resetEndDate,
        format="YYYY-MM-DD",
        on_change=updateDateRange,
        key='mapIniDate')
    # st.sidebar.date_input('To Date',
    #     value=resetEndDate,
    #     min_value=resetIniDate,
    #     max_value=resetEndDate,
    #     format="YYYY-MM-DD",
    #     on_change=updateDateRange,
    #     disabled=disableEndDate,
    #     key='mapEndDate')

# Selector de consulta
query_selection = st.selectbox("Selecciona una consulta para ejecutar:", list(queries.keys()))

def executeQueryAndRepresent(query, dateString, metricString):
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    
    try:
        # Ejecuta la consulta y obtiene resultados
        results = sparql.query().convert()
        
        # Procesa los resultados
        data = []
        variables = results["head"]["vars"]
        for result in results["results"]["bindings"]:
            row = {var: result[var]['value'] for var in variables if var in result}
            
            # Hacer el WikidataLink clickeable para Query 6 y Query 7
            if query_selection in ["Query 5: Give stations and their Wikidata links", "Query 6: Sensors with units reconciled with WikiData"]:
                if "WikidataLink" in row:
                    # Convierte el link en HTML
                    row["WikidataLink"] = f'<a href="{row["WikidataLink"]}" target="_blank">Wikidata</a>'

            data.append(row)

        # Muestra los resultados en un DataFrame si no es el Query 5
        if query_selection != "Query 4: Give all the stations with their altitude, latitude and longitude":
            st.sidebar.write()
            isMapNotShown=True
            st.write("Resultados de la consulta:")
            if data:
                # Crea un DataFrame y permite el HTML en el markdown
                df = pd.DataFrame(data)
                st.markdown(df.to_html(escape=False), unsafe_allow_html=True)

            else:
                st.write("No se encontraron resultados.")
        
        # Mostrar el mapa solo si se selecciona Query 5
        elif data:
            showMap(data, dateString, metricString)

    except Exception as e:
        st.error(f"Error al ejecutar la consulta: {e}")

# Botón para ejecutar la consulta
if st.button("Ejecutar Consulta"):
    # Define la consulta SPARQL seleccionada
    executeQueryAndRepresent(queries[query_selection], "2023-01-01", "All")
