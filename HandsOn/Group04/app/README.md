# ChargeAndParkMadridODKG
This is a software application to complement the project of the Open Data and Knowledge Graphs course (UPM - DATA SCIENCE).

This app has two main files: `back.py` and `app.py`. The application is designed to interact with RDF data and requires the Helio service to be running on port 9000 for proper functionality.

## Requirements

### Python
- Python 3.5 or higher
- Flask

### Additional Python Packages
- All necessary packages are listed in the `requirements.txt` file.

### Helio
This application depends on the Helio instance to query and manipulate RDF data. Helio should be running at `http://localhost:9000/` and configured to point to a specific RDF dataset.

- Download and run [Helio 4.0.0 - Quickstart](https://github.com/helio-ecosystem/helio-publisher/releases/tag/quickstart_4.0.0).
- Set the `Link to RDF data` field in Helio to point to the following RDF file: (https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2024-2025-ODKG/refs/heads/master/HandsOn/Group04/rdf/dataset-with-links-updated.ttl)


## Installation

1. **Clone the repository** (if using version control):

2. **Install dependencies** 
```
pip install -r requirements.txt
```

## Running the Application

1. **Start Helio**: 
    - Access http://localhost:9000/ in your browser to confirm Helio is running.
    - Ensure the Link to RDF data is set to: (https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2024-2025-ODKG/refs/heads/master/HandsOn/Group04/rdf/dataset-with-links-updated.ttl)

2. **Run the Flask application:**
```
python app.py
```
3. **Access the application** : Once Flask is running, you can access the application in your browser at (http://localhost:5000)


