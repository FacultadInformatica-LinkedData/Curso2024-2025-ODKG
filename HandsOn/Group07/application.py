import streamlit as st
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import folium
from streamlit_folium import st_folium





# Initialize the SPARQL wrapper
endpoint_url = "http://localhost:7201/repositories/madrid_events"
sparql = SPARQLWrapper(endpoint_url)
sparql.setReturnFormat(JSON)

def execute_sparql_query(query):
    """Execute a SPARQL query and return results."""
    sparql.setQuery(query)
    try:
        results = sparql.query().convert()
        return results
    except Exception as e:
        st.error(f"An error occurred while querying: {e}")
        return None

def extract_distinct_values(results, value_key):
    """Extract distinct values from query results."""
    values = set()
    for result in results["results"]["bindings"]:
        value = result[value_key]["value"].strip()
        if ',' in value:
            values.update(ac.strip() for ac in value.split(","))
        else:
            values.add(value)
    return sorted(values)

# Query to get accessibility options
access_query = """
PREFIX schema: <http://schema.org/>
PREFIX ns: <http://madrid.events.com/>

SELECT DISTINCT ?access
WHERE { 
  GRAPH <http://madrid.events.com/graph/events> {
    ?place a schema:Place ;
           schema:placeName ?placeName ;
           ns:accessibilityLevel ?access;
  }
}
"""
access_results = execute_sparql_query(access_query)
available_access = extract_distinct_values(access_results, 'access') if access_results else []

# Query to get audience options
audience_query = """
PREFIX schema: <http://schema.org/>
PREFIX ns: <http://madrid.events.com/>

SELECT DISTINCT ?audience
WHERE { 
  GRAPH <http://madrid.events.com/graph/events> {
    ?event a schema:Event ;
           schema:audience ?audience .
  }
}
"""
audience_results = execute_sparql_query(audience_query)
available_audiences = extract_distinct_values(audience_results, 'audience') if audience_results else []

# Query to get district options
district_query = """
PREFIX schema: <http://schema.org/>
PREFIX ns: <http://madrid.events.com/>

SELECT DISTINCT ?district
WHERE { 
  GRAPH <http://madrid.events.com/graph/events> {
    ?geo a schema:GeoCoordinates ;
           ns:district ?district .
  }
}
"""
district_results = execute_sparql_query(district_query)
available_districts = extract_distinct_values(district_results, 'district') if district_results else []

# Query to get neighborhood options
neighborhood_query = """
PREFIX schema: <http://schema.org/>
PREFIX ns: <http://madrid.events.com/>

SELECT DISTINCT ?neighborhood
WHERE { 
  GRAPH <http://madrid.events.com/graph/events> {
    ?geo a schema:GeoCoordinates ;
           ns:neighborhood ?neighborhood .
  }
}
"""
neighborhood_results = execute_sparql_query(neighborhood_query)
available_neighborhoods = extract_distinct_values(neighborhood_results, 'neighborhood') if neighborhood_results else []


with st.sidebar:
# Date range selection
  start_date = st.date_input("Start date", value=pd.to_datetime("2023-01-01"))
  end_date = st.date_input("End date", value=pd.to_datetime("2025-12-31"))
  is_free_check = st.checkbox("Free", value=False)
  selected_audiences = st.multiselect("Select Audiences", options=available_audiences)
  selected_access = st.multiselect("Select Accessibility", options=available_access)
  selected_districts = st.multiselect("Select Districts", options=available_districts)
  selected_neighborhoods = st.multiselect("Select Neighborhoods", options=available_neighborhoods)


# Define the SPARQL query with date filters
base_query = f"""
PREFIX schema: <http://schema.org/>
PREFIX ns: <http://madrid.events.com/>

SELECT ?eventName ?startDate ?placeName ?latitude ?longitude ?audience ?access ?district ?neighborhood ?url ?placeUrl ?neighborhoodWiki ?districtWiki 
WHERE {{ 
  GRAPH <http://madrid.events.com/graph/events> {{
    ?event a schema:Event ;
           ns:eventName ?eventName ;
           schema:startDate ?startDate ;
           schema:isAccessibleForFree ?isFree ;
           schema:audience ?audience ;
           ns:hasPlace ?place ;
           schema:url ?url .

    ?place a schema:Place ;
           schema:placeName ?placeName ;
           ns:accessibilityLevel ?access ;
           schema:url ?placeUrl ;
           schema:geo ?geo .

    ?geo a schema:GeoCoordinates ;
         ns:district ?district ;
         ns:neighborhood ?neighborhood ;
         owl:sameAs ?neighborhoodWiki ;
         owl:sameAs ?districtWiki ;
         schema:latitude ?latitude ;
         schema:longitude ?longitude .

    FILTER (?startDate >= "{start_date.isoformat()}"^^xsd:dateTime && ?startDate <= "{end_date.isoformat()}"^^xsd:dateTime).
    {"FILTER( ?isFree = 'true'^^xsd:boolean) ." if is_free_check else ""}
    {"FILTER(" + " || ".join(f'contains(?audience, "{audience}")' for audience in selected_audiences) + ") ." if selected_audiences else ""}
    {"FILTER(" + " && ".join(f'contains(?access, "{ac}")' for ac in selected_access) + ") ." if selected_access else ""}
    # Combine district and neighborhood filters with OR
    {"FILTER(" + " || ".join(f'contains(?district, "{district}")' for district in selected_districts + selected_neighborhoods) + ") ." if selected_districts or selected_neighborhoods else ""}
  }}
}}
ORDER BY ?startDate
"""

# Execute the event query and process results
# Execute the event query and process results
event_results = execute_sparql_query(base_query)
if event_results:
    data = []
    for result in event_results["results"]["bindings"]:
        data.append({
            "Event Name": result["eventName"]["value"],
            "Start Date": result["startDate"]["value"],
            "Place": result["placeName"]["value"],
            "Place Url": result["placeUrl"]["value"],
            "Latitude": float(result["latitude"]["value"]),
            "Longitude": float(result["longitude"]["value"]),
            "Audience": result["audience"]["value"],
            "Access": result["access"]["value"],
            "District": result["district"]["value"],
            "Neighborhood": result["neighborhood"]["value"],
            "District Wiki": result["districtWiki"]["value"],   # Include district Wikipedia link
            "Neighborhood Wiki": result["neighborhoodWiki"]["value"],
            "URL": result["url"]["value"]
        })
    if len(data) != 0:
        # Create and display the DataFrame
        df = pd.DataFrame(data)
        

        # Display a map with event locations, ensuring unique events per location
        grouped_df = df.groupby(['Latitude', 'Longitude']).agg({
            'Event Name': lambda x: list(set(x)),  # Keep unique event names
            'Start Date': lambda x: list(set(x)),  # Unique start dates per event
            'Audience': lambda x: list(set(x)),    # Unique audiences per event
            'URL': lambda x: list(set(x)),         # Unique URLs per event
            'Place': 'first',                      # Assuming one place per location
            'Place Url': 'first',                  # Assuming one place URL per location
            'Access': 'first',                     # Assuming access level is consistent for the location
            'District': 'first',                   # Assuming one district per location
            'Neighborhood': 'first',               # Assuming one neighborhood per location
            'District Wiki': 'first',              # Assuming one district wiki link per location
            'Neighborhood Wiki': 'first'           # Assuming one neighborhood wiki link per location
        }).reset_index()

        m = folium.Map(location=[40.4168, -3.7038], zoom_start=12)

        # Add markers for each unique event location
        # Add markers for each event in the DataFrame with error handling for missing data

try:
    for _, row in grouped_df.iterrows():
        # Create popup text that includes all events at this location
        popup_html = "<b>Events:</b>"

        # Get the number of events at this location
        num_events = len(row['Event Name'])

        for idx in range(num_events):
            # Safely retrieve data for each attribute, providing a default if it's missing
            event_name = row['Event Name'][idx] if idx < len(row['Event Name']) else "N/A"
            start_date = row['Start Date'][idx] if idx < len(row['Start Date']) else "N/A"
            audience = row['Audience'][idx] if idx < len(row['Audience']) else "N/A"
            url = row['URL'][idx] if idx < len(row['URL']) else "#"

            # Append each event to the popup
            popup_html += f"""
            <div class="box" style="border: 1px black solid; border-radius: 2px; padding: 5px 3px; margin: 5px auto;">
            <a href="{url}" target="_blank">{event_name}</a><br>
            <b>Start Date:</b> {start_date}<br>
            <b>Type:</b> {audience}<br>
            </div>
            """

        # Additional information about the place, access, district, and neighborhood
        popup_html += f"""
            <b>Place: <a href="{row['Place Url']}">{row['Place']}</a></b>
            <div class="site">
            <b>Access:</b> {row['Access']}<br>
            <b>District:</b> <a href="{row['District Wiki']}">{row['District']}</a><br>
            <b>Neighborhood:</b> <a href="{row['Neighborhood Wiki']}"> {row['Neighborhood']}</a><br>
            </div>
        """

        # Add a marker for the grouped location
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color='blue')  # Customize the marker color as needed
        ).add_to(m)

    # Display the map in Streamlit
    st.write("### Map of Events")
    st_folium(m, width=1300, height=800)

    # st.write("DF",)
except Exception as e:
    st.write("### No events found for these filters, try again!")