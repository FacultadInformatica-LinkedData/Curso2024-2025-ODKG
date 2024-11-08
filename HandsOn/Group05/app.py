import streamlit as st
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
from datetime import date, datetime, time
import plotly.express as px

endpoint_url = "http://localhost:7200/repositories/riverside_pollution" 
sparql = SPARQLWrapper(endpoint_url)
sparql.setReturnFormat(JSON)

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
        /* Ajusta el ancho del contenido */
        .main {
            max-width: 90%;
            margin: auto;
        }

        /* Ajustes adicionales opcionales para alinear mejor el contenido */
        .css-18e3th9 {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌆 Riverside Pollution Study Dashboard")
st.write("An interactive tool to visualize and analyze pollution data along various streets. Use the filters on the left to customize your view.")


main_col, info_col = st.columns([4, 1])  

def execute_sparql_query(query):
    sparql.setQuery(query)
    try:
        results = sparql.query().convert()
        return results
    except Exception as e:
        st.error(f"An error occurred while querying: {e}")
        return None
    

def convert_results_to_dataframe(results, date_key="date", value_key="value"):
    data = []
    for result in results["results"]["bindings"]:
        date = result[date_key]["value"]
        value = result[value_key]["value"]
        data.append((date, value))
    
    df = pd.DataFrame(data, columns=["Date", "Value"])
    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
    df["Value"] = pd.to_numeric(df["Value"], errors='coerce')
    df = df.groupby("Date", as_index=False).mean()
    return df

def get_riverside_info():
    query = """
    PREFIX schema: <http://schema.org/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rps: <http://riversidepollutionstudy.org/>
    SELECT ?population ?mayor ?cityUrl
    WHERE {
        <https://wikidata.org/entity/Q49243> rdfs:label "Riverside" ;
        <https://www.wikidata.org/wiki/PropertyP1082> ?population ;
        <https://www.wikidata.org/wiki/PropertyP6> ?mayor ;
        <https://www.wikidata.org/wiki/PropertyP856> ?cityUrl .
    }
    """
    return execute_sparql_query(query)


with st.sidebar:
    st.header("📊 Filter Data")
    st.subheader("Select Location and Observation Type")
    

    street_options = ["Iowa", "Chicago", "Cranford", "Magnolia"]
    selected_street = st.selectbox("Street", street_options)

    observation_types = ["NO2", "humidity", "windDirection", "pressure", "temperature", "nearBoundHighwayVehicles", "nearBoundLocalRoadwayVehicles", "farBoundHighwayVehicles", "farBoundLocalRoadway", "backgroundNO2","backgroundPM2.5", "PM2.5", "windSpeed"]  # Ajusta según los tipos disponibles en tu ontología
    selected_observation_type = st.selectbox("Observation", observation_types)

    st.subheader("Select Date Range")

    min_date = date(2021, 5, 21)
    min_time = time(12, 30)
    max_date = date(2021, 6, 27)
    max_time = time(23, 30)

    start_date = st.date_input("Starting date", min_value=min_date, max_value=max_date, value=min_date)
    start_time = st.time_input("Starting time", value=min_time if start_date == min_date else time(0, 0))

    end_date = st.date_input("Ending date", min_value=min_date, max_value=max_date, value=max_date)
    end_time = st.time_input("Ending time", value=max_time if end_date == max_date else time(23, 59))

    start_datetime = datetime.combine(start_date, start_time)
    end_datetime = datetime.combine(end_date, end_time)
    min_datetime = datetime.combine(min_date, min_time)
    max_datetime = datetime.combine(max_date, max_time)

    if start_datetime < min_datetime or end_datetime > max_datetime:
        st.error("Select date and time between the valid range please (2021-05-21 12:30:00 to 2021-06-27 23:30:00)")
    elif end_datetime < start_datetime:
        st.error("Starting date and time must be sooner than ending date and time.")
    else:
        start_datetime_str = start_datetime.strftime("%Y-%m-%d %H:%M:%S-07:00")
        end_datetime_str = end_datetime.strftime("%Y-%m-%d %H:%M:%S-07:00")

    query_button = st.button("Show")

with main_col:
    if query_button:
        with st.spinner("Loading..."):
            query = f"""
                    PREFIX schema: <https://schema.org/>
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    SELECT ?date ?value
                    WHERE {{
                        ?observation schema:variableMeasured "{selected_observation_type}" ;
                                    schema:value ?value ;
                                    schema:observationDate ?date  .


                        ?place rdf:type schema:Place ;
                            rdfs:label "{selected_street}" ;
                            rdfs:label ?label .
                    }}
                    ORDER BY ?date
                """
            result = execute_sparql_query(query)
            if result:
                df = convert_results_to_dataframe(result, date_key="date", value_key="value")
                filtered_df = df[(df["Date"] >= start_datetime_str) & (df["Date"] <= end_datetime_str)]
                if not filtered_df.empty:
                    col1, col2, col3 = st.columns(3)
                    col1.metric(label="🌡️ Average Value", value=f"{filtered_df['Value'].mean():.2f}")
                    col2.metric(label="📈 Max Value", value=f"{filtered_df['Value'].max():.2f}")
                    col3.metric(label="📉 Min Value", value=f"{filtered_df['Value'].min():.2f}")
                    fig = px.line(filtered_df, x="Date", y="Value", title=f"Observations of {selected_observation_type} on {selected_street}", markers=True)
                    fig.update_layout(xaxis_title="Date", yaxis_title="Value", hovermode="x unified")
                    fig.update_layout(template="plotly_white", title_font=dict(size=20, family='Arial', color='royalblue'), xaxis=dict(showgrid=True, gridcolor='lightgrey'), yaxis=dict(showgrid=True, gridcolor='lightgrey'))
                    fig.update_traces(line=dict(color="royalblue"))
                    st.plotly_chart(fig, use_container_width=True)
                    st.subheader("Value Distribution")
                    fig_hist = px.histogram(filtered_df, x="Value", nbins=20, title="Distribution of Observed Values")
                    st.plotly_chart(fig_hist, use_container_width=True)
                else:
                    st.error("No data found for the selected filters. Try adjusting the date range or observation type.")
            else:
                st.write("Failed to retrieve data from the endpoint.")

    st.markdown("""
    <hr>
    <footer style='text-align: center;'>
        Open Data Aplication - Group 05
    </footer>
    """, unsafe_allow_html=True)

with info_col:
    riverside_info = get_riverside_info()

    if riverside_info and riverside_info["results"]["bindings"]:
        data = riverside_info["results"]["bindings"][0]

        population = data.get("population", {}).get("value", "N/A")
        mayor = data.get("mayor", {}).get("value", "N/A")
        city_url = data.get("cityUrl", {}).get("value", "N/A")
    
        st.subheader("🌆 Riverside Information")
        st.write(f"**👨‍👩‍👧‍👦Population:** {population}")
        st.write(f"**🧑‍💼Mayor:** {mayor}")
        st.write(f"**🧑‍💻City URL:** [Visit Riverside]({city_url})")
