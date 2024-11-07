12
    Analysis
        - The resource naming strategy is not defined for individuals.
        - The analysis.html file does not contain the license of the dataset to be generated.
    Ontology
        - In OWL, having multiple domains (or ranges) means that the domain (or range) is the intersection of all the classes.  The current definitions of properties with multiple domains are wrong.
        - The domain and/or range of some property is not defined.
    RDF data
        - It could happen that two individuals from different classes have the same URI because the naming strategy does not ensure uniqueness.
        - Individuals have no type.
        - Some types in the data should reflect types in the class hierarchy in the ontology and should not be encoded as property values.
        - Coordinates should be represented independently as two numbers, not both in a string.
        - Accidents have multiple genders. The persons involved are not correctly represented. The same happens with the injuries.
        - Date values are not encoded properly.
        - Boolean data values are not encoded properly.
            Some fields with range 0-1 are not integers, they are booleans.
        - Some entities could be encoded as instances and not strings.
            You will need them for linking.
    Take into account that the review has been performed over a previous version of the hands-on. Some of the defects found may have been already fixed.
