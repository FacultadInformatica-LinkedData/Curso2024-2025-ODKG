1
    Analysis
        - The analysis.html file does not contain the license of the dataset to be generated.
        - The resource naming strategy does not ensure uniqueness of individuals.
    Ontology
        - The domain and/or range of some property is not defined.
        - You are connecting the Spot to both Barrio and Distrito, but should not it be connected to Barrio and then the Barrio to the District?
    RDF data
        - Add labels to individuals; don't require people to interpret your URIs.
        - The RDF file does not use the class and property URIs as they are defined in the ontology.
        - The Spots are not related to Barrios or Distritos; they only have datatype properties with string values.
    Take into account that the review has been performed over a previous version of the hands-on. Some of the defects found may have been already fixed.
