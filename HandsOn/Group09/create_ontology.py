from rdflib import Graph
import morph_kgc, subprocess, os, requests, json, csv, time

## --------------------OPENREFINE API--------------------
csrf_token = ""

def get_csrf_token():
    global csrf_token

    url = 'http://127.0.0.1:3333/command/core/get-csrf-token'
    response = requests.get(url)
    csrf_token = response.json()["token"]

# Cargar el CSV como un nuevo proyecto en OpenRefine
def create_project(csv_file_path, project_name):
    url = 'http://127.0.0.1:3333/command/core/create-project-from-upload'
    with open(csv_file_path, 'rb') as f:
        files = {'file': f}
        data = {
            'project-name': project_name,
            'format': 'text/line-based/csv',  # Indicar que es un csv_file_path
        }
        response = requests.post(f'{url}?csrf_token={csrf_token}', files=files, data=data)
    return response.url[38:len(response.url)]

def create_project_2_files(csv_file_path1, csv_file_path2, project_name):
    url = 'http://127.0.0.1:3333/command/core/create-project-from-upload'
    with open(csv_file_path1, 'rb') as f1, open(csv_file_path2, 'rb') as f2:
        files = {
            'file1': f1,
            'file2': f2
        }
        data = {
            'project-name': project_name,
            'format': 'text/line-based/csv',  # Indicar que es un csv_file_path
        }
        response = requests.post(f'{url}?csrf_token={csrf_token}', files=files, data=data)
    return response.url[38:len(response.url)]


# Aplicar el archivo JSON de operaciones
def apply_operations(project_id, operations_json_file):
    url = 'http://127.0.0.1:3333/command/core/apply-operations'
    with open(operations_json_file, 'r') as f:
        operations = json.load(f)
        data = {
            'operations': json.dumps(operations),
        }

        response = requests.post(f'{url}?project={project_id}&csrf_token={csrf_token}', data=data)

        if response.json()["code"] == "error":
            raise Exception(f"Error al aplicar los cambios: {response.text}")
    return 0

def export_project_to_csv(project_id, export_file_path):
    url = 'http://127.0.0.1:3333/command/core/export-rows'
    response = requests.post(f'{url}?project={project_id}&format=csv')
    with open(export_file_path, 'wb') as f:
        f.write(response.content)

def delete_project(project_id):
    url = 'http://127.0.0.1:3333/command/core/delete-project'
    response = requests.post(f'{url}?project={project_id}&csrf_token={csrf_token}')
    if response.json()["code"] != "ok":
        raise Exception("Deleting project error")


# -----------------------------------------------

def wait_for_reconciliation(project_id):
    reconciliation_done = False
    url = 'http://127.0.0.1:3333/command/core/get-processes'
    while(not reconciliation_done):
        response = requests.get(f'{url}?project={project_id}&csrf_token={csrf_token}')
        if(response.json()['processes'] == []):
            reconciliation_done = True
            print("Reconcillied")
        else:
            print("Waiting for reconciliation")
            time.sleep(1)

def apply_changes_csv(path_csv, project_name, changes_json_path, export_file_path):
    string = f'------------Applying changes to {path_csv} with {changes_json_path}------------'
    print(string)
    # Crear un proyecto1
    project_id = create_project(path_csv, project_name)

    apply_operations(project_id,changes_json_path)

    wait_for_reconciliation(project_id)

    export_project_to_csv(project_id, export_file_path)

    delete_project(project_id)

def apply_changes_2_csv(path_csv1, path_csv2, project_name, changes_json_path, export_file_path):
    string = f'------------Applying changes to {path_csv1} and {path_csv2} with {changes_json_path}------------'
    print(string)
    # Crear un proyecto1
    project_id = create_project_2_files(path_csv1, path_csv2, project_name)

    apply_operations(project_id,changes_json_path)

    wait_for_reconciliation(project_id)

    export_project_to_csv(project_id, export_file_path)

    delete_project(project_id)

'''
def join_files(path_csv1, path_csv2, output_path):
    string = f"------------Merging {path_csv1} and {path_csv2}------------"
    print(string)

    command = f"(cat {path_csv1}; tail -n +2 {path_csv2}) > {output_path}"
    resultado = subprocess.run(command, shell=True)

    if resultado.returncode == 0:
        print("------------Deleting intermediate files------------")
        os.remove(path_csv1)
        os.remove(path_csv2)
    else:
        raise Exception("Error al juntar los archivos")
'''

def generate_rdf(with_links):
    print("------------Generating RDF data with Morph-KGC------------")

    # Generates the RDF knowledge graph
    config_no_links = """
    [CONFIGURATION]
    [DEFAULT]
    main_dir: ./

    # INPUT
    na_values=,#N/A,N/A,#N/A N/A,n/a,NA,<NA>,#NA,NULL,null,NaN,nan,None

    # MULTIPROCESSING
    number_of_processes=2

    [SOURCE]
    mappings=mappings/mapping_rules.yml
    """

    config_with_links = """
    [CONFIGURATION]
    [DEFAULT]
    main_dir: ./

    # INPUT
    na_values=,#N/A,N/A,#N/A N/A,n/a,NA,<NA>,#NA,NULL,null,NaN,nan,None

    # MULTIPROCESSING
    number_of_processes=2

    [SOURCE]
    mappings=mappings/mapping_rules-with-links.yml
    """
    config = config_with_links if with_links else config_no_links

    print(config)
    return morph_kgc.materialize(config)

def turtle_serialization(graph,with_links):
    print("------------Serializing RDF data into a file------------")
    # Turtle format printing
    destination = "rdf/knowledge-graph-with-links.ttl" if (with_links) else "rdf/knowledge-graph.ttl"
    graph.serialize(destination=destination)

# -------------------------------------------------

def stations_csv2json(csv_file, json_file, with_links):
    print(f"------------Converting {csv_file} to json------------")
    # Leer el archivo CSV
    with open(csv_file, 'r', encoding='utf-8') as file:
        lector_csv = csv.DictReader(file)

        # Crear una lista para almacenar los datos
        lista_datos = []

        # Recorrer cada fila del archivo CSV y agregarlo a la lista
        for fila in lector_csv:
            # Convertir las columnas numéricas a enteros

            no = {
                "label": "NO",
                "sameAsWikidata": "http://wikidata.org/entity/Q207843"
            }
            no2 = {
                "label": "NO2",
                "sameAsWikidata": "http://wikidata.org/entity/Q207895"
            }
            nox = {
                "label": "NOx",
                "sameAsWikidata": "http://wikidata.org/entity/Q20962970"
            }
            so2 = {
                "label": "SO2",
                "sameAsWikidata": "http://wikidata.org/entity/Q5282"
            }
            co = {
                "label": "CO",
                "sameAsWikidata": "http://wikidata.org/entity/Q2025"
            }
            pm10 = {
                "label": "PM10",
                "sameAsWikidata": "http://wikidata.org/entity/Q48035511"
            }
            pm2_5 = {
                "label": "PM2.5",
                "sameAsWikidata": "http://wikidata.org/entity/Q48035814"
            }
            o3 = {
                "label": "O3",
                "sameAsWikidata": "http://wikidata.org/entity/Q36933"
            }
            btx = {
                "label": "BTX",
                "sameAsWikidata": "http://wikidata.org/entity/Q411087"
            }
            measures = []
            if fila['NO2'] == "true":
                measures.append(no)
                measures.append(nox)
                measures.append(no2)
            if fila['SO2'] == "true":
                measures.append(so2)
            if fila['CO'] == "true":
                measures.append(co)
            if fila['PM10'] == "true":
                measures.append(pm10)
            if fila['PM2_5'] == "true":
                measures.append(pm2_5)
            if fila['O3'] == "true":
                measures.append(o3)
            if fila['BTX'] == "true":
                measures.append(btx)


            station_no_links = {
              'CODIGO': fila['CODIGO'],
              'ESTACION': fila["ESTACION"],
              'ALTITUD': fila["ALTITUD"],
              'MEDIDAS': measures,
              'COD_VIA': fila['COD_VIA'],
              'LONGITUD': fila['LONGITUD'],
              'LATITUD': fila['LATITUD']
            }

            station_with_links = {
              'CODIGO': fila['CODIGO'],
              'same_as_wikidata_streets': fila['same_as_wikidata_streets'],
              'ESTACION': fila["ESTACION"],
              'ALTITUD': fila["ALTITUD"],
              'MEDIDAS': measures,
              'COD_VIA': fila['COD_VIA'],
              'LONGITUD': fila['LONGITUD'],
              'LATITUD': fila['LATITUD']
            }
            station = station_with_links if with_links else station_no_links
            lista_datos.append(station)

    # Escribir el archivo JSON con la lista de datos
    with open(json_file, 'w', encoding='utf-8') as file:
        json.dump(lista_datos, file, ensure_ascii=False, indent=2)

def treatment_measures(with_links):
    source_file1 = "csv/datos_diarios_2023.csv"
    source_file2 = "csv/datos_diarios_2024.csv"
    if(with_links):
        output_path = "csv/datos_diarios-updated-with-links.csv"
        cambios_json_path = "openrefine/cambios_datos_diarios.json"
    else:
        output_path = "csv/datos_diarios-updated.csv"
        cambios_json_path = "openrefine/cambios_datos_diarios.json"

    # Air quality measures
    apply_changes_2_csv(source_file1, source_file2, "measures", cambios_json_path, output_path)

def treatment_stations(with_links):
    source_file = "csv/info_estaciones.csv"
    if(with_links):
        output_path = "csv/info_estaciones-updated-with-links.csv"
        cambios_json_path = "openrefine/cambios_estaciones-with-links.json"
        json_ouput_path = "csv/info_estaciones-updated-with-links.json"
    else:
        output_path = "csv/info_estaciones-updated.csv"
        cambios_json_path = "openrefine/cambios_estaciones.json"
        json_ouput_path = "csv/info_estaciones-updated.json"

    apply_changes_csv(source_file, "stations", cambios_json_path, output_path)
    # Generate json version
    stations_csv2json(output_path,json_ouput_path,with_links)


def main():
    # --- NO LINKS ---
    #get_csrf_token()
    #treatment_measures(False)
    #treatment_stations(False)

    #g = generate_rdf(False)
    #turtle_serialization(g,False)

    # --- WITH LINKS ---
    get_csrf_token()
    treatment_measures(True)
    treatment_stations(True)

    g = generate_rdf(True)
    turtle_serialization(g,True)

if __name__ == "__main__":
    main()
