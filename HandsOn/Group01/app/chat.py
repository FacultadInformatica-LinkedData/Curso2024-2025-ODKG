import streamlit as st
from rdflib import Graph, Namespace
import re





def main():
    # Cargar la ontología desde un archivo local

    g = Graph()
    ONTOLOGY_FILE = r"C:\Users\Claudia\OneDrive - Universidad Politécnica de Madrid\Universidad\Master\Open data\group proyect\Curso2024-2025-ODKG\HandsOn\Group01\rdf\aparcabicis-ttl-updated-with-links.ttl"
    with open(ONTOLOGY_FILE, "rb") as f:
        g.parse(f, format="turtle")  # Cambia "turtle" si el archivo está en otro formato

    # Definir los prefijos y namespaces utilizados en la ontología
    NS = Namespace("http://www.bikeradar.es/ontology/ont#")
    g.bind("ns", NS)

    # Crear función para ejecutar la consulta SPARQL en el grafo local
    def execute_sparql_query(query):
        try:
            results = g.query(query)
            return results
        except Exception as e:
            st.error(f"Error ejecutando la consulta SPARQL: {e}")
            return None

       # Crear función para generar consultas SPARQL según la entrada del usuario
    def generate_sparql_query(user_input):
        # 1. Consulta para parqueos de bicicletas en un barrio específico
        if "bicicletas en barrio" in user_input:
            barrio = re.search(r"bicicletas en barrio ([\w\s]+)", user_input)
            
            if barrio:
                barrio_name = barrio.group(1).strip().replace(" ", "_")
                print(barrio_name)
                query = f"""
                PREFIX ns: <http://www.bikeradar.es/ontology/ont#>
                SELECT ?bicycleParkingSpot ?id ?fechaInstalacion ?barrio
                WHERE {{
                    ?bicycleParkingSpot a ns:BicycleParkingSpot ;
                                        ns:isInBarrio ?barrio ;
                                        ns:id ?id ;
                                        ns:hasFechaInstalacion ?fechaInstalacion .
                    FILTER (?barrio = '{barrio_name}') 
                }}
                """
                return query
        
        # 2. Consulta para contar todos los puntos de parqueo
        elif "total de bicispots" in user_input:
            query = """
            PREFIX ns: <http://www.bikeradar.es/ontology/ont#>
            SELECT (COUNT(?bicycleParkingSpot) AS ?totalSpots)
            WHERE {
                ?bicycleParkingSpot a ns:BicycleParkingSpot .
            }
            """
            return query

        # 3. Consulta para coordenadas de bicicletas
        elif "coordenadas de bicicleta" in user_input:
            query = """
            PREFIX ns: <http://www.bikeradar.es/ontology/ont#>
            SELECT ?bicycleParkingSpot ?coordX ?coordY
            WHERE {
                ?bicycleParkingSpot a ns:BicycleParkingSpot ;
                                    ns:coordenadaX ?coordX ;
                                    ns:coordenadaY ?coordY .
            }
            LIMIT 10
            """
            return query

        # 4. Número de puntos de aparcamiento por barrio
        elif "bicispots por barrio" in user_input:
            query = """
            PREFIX ns: <http://www.bikeradar.es/ontology/ont#>
            SELECT ?barrio (COUNT(?bicycleParkingSpot) AS ?numSpots)
            WHERE {
                ?bicycleParkingSpot a ns:BicycleParkingSpot ;
                                    ns:isInBarrio ?barrio .
            }
            GROUP BY ?barrio
            ORDER BY DESC(?numSpots)
            """
            return query

        # 5. Promedio de capacidad de aparcamiento por barrio
        elif "promedio capacidad por barrio" in user_input:
            query = """
            PREFIX ns: <http://www.bikeradar.es/ontology/ont#>
            SELECT ?barrio (AVG(?capacidad) AS ?avgCapacity)
            WHERE {
                ?bicycleParkingSpot a ns:BicycleParkingSpot ;
                                    ns:isInBarrio ?barrio ;
                                    ns:capacidad ?capacidad .
            }
            GROUP BY ?barrio
            ORDER BY DESC(?avgCapacity)
            """
            return query

        # 6. Fechas de instalación más antigua y más reciente
        elif "fechas de instalación" in user_input:
            query = """
            PREFIX ns: <http://www.bikeradar.es/ontology/ont#>
            SELECT (MIN(?fechaInstalacion) AS ?fechaMasAntigua) (MAX(?fechaInstalacion) AS ?fechaMasReciente)
            WHERE {
                ?bicycleParkingSpot a ns:BicycleParkingSpot ;
                                    ns:hasFechaInstalacion ?fechaInstalacion .
            }
            """
            return query

        # 7. Puntos de aparcamiento por año de instalación
        elif "aparcamientos por año de instalación" in user_input:
            query = """
            PREFIX ns: <http://www.bikeradar.es/ontology/ont#>
            SELECT (YEAR(?fechaInstalacion) AS ?año) (COUNT(?bicycleParkingSpot) AS ?numSpots)
            WHERE {
                ?bicycleParkingSpot a ns:BicycleParkingSpot ;
                                    ns:hasFechaInstalacion ?fechaInstalacion .
            }
            GROUP BY ?año
            ORDER BY ?año
            """
            return query

        else:
            st.warning("No pude entender la solicitud. Intenta ser más específico.")
            return None
            


    # Configuración de la interfaz de usuario en Streamlit
    st.title("Chatbot SPARQL en Local para Ontología de Parqueos de Bicicletas")
    st.write("Este chatbot puede realizar consultas SPARQL a la ontología cargada en local.")

    user_input = st.text_input("Haz una pregunta:", "Dame todos los bicispots")

    if st.button("Consultar"):
        # Generar y ejecutar la consulta SPARQL basada en la entrada del usuario
        sparql_query = generate_sparql_query(user_input)
        if sparql_query:
            st.write(f"**Consulta SPARQL generada:**\n```sparql\n{sparql_query}\n```")
            results = execute_sparql_query(sparql_query)
            
            if results:
                st.write("### Resultados:")
                for row in results:
                    # Imprime cada variable de manera individual en lugar de usar .items()
                    st.write({str(var): str(val) for var, val in row.asdict().items()})

            else:
                st.write("No se encontraron resultados.")


if __name__ == "__main__":
    main()
