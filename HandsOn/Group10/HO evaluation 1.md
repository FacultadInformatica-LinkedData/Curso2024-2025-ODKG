10
    Analysis
        - The analysis.html file does not contain the resource naming strategy.
    Ontology
        - The namespaces of the ontology are not correct; it is not a valid OWL file. Do not create ontologies by hand; use some tool.
        - The ontology presents text encoding issues.
        - The domain and/or range of some property is not defined.
        - Why are you creating all the terms in the ontology as instances of dctypes:Dataset? This is not correct.
    RDF data
        - Not every string composed by numbers is a number.
        - It could happen that two individuals from different classes have the same URI because the naming strategy does not ensure uniqueness.
    Take into account that the review has been performed over a previous version of the hands-on. Some of the defects found may have been already fixed.
