import streamlit as st
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

# URL of your GraphDB SPARQL endpoint
GRAPHDB_URL = "http://localhost:7200/repositories/output-ttl"  # Replace 'your_repo' with your actual repository name

# Initialize SPARQL wrapper
sparql = SPARQLWrapper(GRAPHDB_URL)

# Load the provinces list from the CSV file
try:
    provinces_df = pd.read_csv("provinces.csv")
    # Assuming the province names are in a column named 'Province'
    provinces_list = ["Any"] + provinces_df['Province'].tolist()
except FileNotFoundError:
    st.error("The file 'provinces.csv' was not found.")
    provinces_list = ["Any"]

# Function to get municipalities based on selected province
def get_municipalities(province):
    query = f"""
    PREFIX ex: <https://fuelpricespain.org/gasstations#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

    SELECT DISTINCT ?municipality
    WHERE {{
        ?station rdf:type ex:GasStation ;
                 ex:locatedInProvince "{province}" ;
                 ex:locatedInMunicipality ?municipality .
    }}
    """
    
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    municipalities = ["Any"]  # Default option
    for result in results["results"]["bindings"]:
        municipalities.append(result["municipality"]["value"])
    
    return municipalities

# Streamlit app layout
st.title("GraphDB Fuel Station Query Interface")

# Province selection dropdown
st.write("### Filters")
province = st.selectbox("Select Province", provinces_list)

# Get municipalities dynamically based on selected province
if province != "Any":
    municipalities_list = get_municipalities(province)
else:
    municipalities_list = ["Any"]  # Default when no province is selected

# Municipality dropdown
municipality = st.selectbox("Select Municipality", municipalities_list)
# Sorting options
st.write("### Sorting Options")
price_column = st.selectbox("Order by Price", ["Diesel", "Gasoline"])
order = st.radio("Order", ["Ascending", "Descending"])

# Construct SPARQL query for main query
base_query = """
            PREFIX ex: <https://fuelpricespain.org/gasstations#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>

            SELECT ?station ?municipality ?province ?diesel_price ?gasoline_price ?lat ?long
            WHERE {
                ?station rdf:type ex:GasStation ;
                        ex:locatedInProvince ?province ;
                        ex:priceOfDieselA ?diesel_price ;
                        ex:priceOf95E5 ?gasoline_price ;
                        ex:locatedInMunicipality ?municipality ;
                        geo:lat ?lat ;
                        geo:long ?long .
"""


# Add filters to the query if specific options are selected
filters = []
if province != "Any":
    filters.append(f'FILTER (?province = "{province}")')
if municipality != "Any":
    filters.append(f'FILTER (?municipality = "{municipality}")')
# Append filters to the query
if filters:
    base_query += "\n".join(filters)

# Add ordering
price_var = "?diesel_price" if price_column == "Diesel" else "?gasoline_price"
order_by_clause = f"ORDER BY {'ASC' if order == 'Ascending' else 'DESC'}({price_var})"
base_query += f"\n}} {order_by_clause}"

# Display the query for verification
st.write("### Generated SPARQL Query")
st.code(base_query)

if st.button("Run Query"):
    try:
        # Set the SPARQL query
        sparql.setQuery(base_query)
        sparql.setReturnFormat(JSON)
        
        # Execute the query
        results = sparql.query().convert()
        
        # Extract results into a pandas DataFrame
        data = []
        for result in results["results"]["bindings"]:
            row = {
                "Station": result["station"]["value"],
                "Municipality": result.get("municipality", {}).get("value", "N/A"),
                "Province": result["province"]["value"],
                "Diesel Price": result["diesel_price"]["value"],
                "Gasoline Price": result["gasoline_price"]["value"],
                "LATITUDE": float(result["lat"]["value"][::-1].replace(',','',1)[::-1].replace(',','.')),
                "LONGITUDE": float(result["long"]["value"][::-1].replace(',','',1)[::-1].replace(',','.')),
            }
            data.append(row)
        df = pd.DataFrame(data)
        
        # Display the results in Streamlit
        st.write("### Query Results")
        st.dataframe(df)
        
        # Display the locations on a map
        st.write("### Map of Fuel Stations")
        st.map(df[['LATITUDE', 'LONGITUDE']])
    
    except Exception as e:
        st.error(f"An error occurred: {e}")
