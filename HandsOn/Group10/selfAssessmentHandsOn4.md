# Hands-on assignment 4 – Self assessment

## Checklist

**Every RDF file:**

- [x] Uses the .nt extension
- [x] Is serialized in the NTriples format
- [x] Follows the resource naming strategy
- [x] Uses class and property URIs that are the same as those used in the ontology

**Every URI in the RDF files:**

- [x] Is "readable" and has some meaning (e.g., it is not an auto-increased integer) 
- [x] Is not encoded as a string
- [x] Does not contain a double slash (i.e., “//”)

**Every individual in the RDF files:**

- [x] Has a label with the name of the individual
- [x] Has a type

**Every value in the RDF files:**

- [x] Is trimmed
- [x] Is properly encoded (e.g., dates, booleans)
- [x] Includes its datatype
- [x] Uses the correct datatype (e.g., values of 0-1 may be booleans and not integers, not every string made of numbers is a number)

## Comments on the self-assessment
1. For this hands-on, we revisited the dataset pre-processing to alter a couple of columns minimally. Due to previously having needed to use Python to separate and stack columns, functionality missing in OpenRefine, we continued using Python for this minimal alterations.
2. As we are utilizing schema:Place as it appears in https://schema.org/Place, to the letter, including blanknode schema:PostalAddress's. We believed that following the template was more important than the comments on how we should try to avoid them.
3. We decided on using in the URI's the class of the instance and the ID of the place, which effectively behaves as an autoincreasing integer. This was carefully considered, but the alternatives we tried were worse.
   1. Trips only had starting and ending date as unique identifiers, which would have left us with a horribly unreadable link. Creating an ID and using it was clearer.
   2. Stations are literally identified with IDs, which lead us to considering that Station1 is quite representative and readable. Using their names would have been undesirable, as they are very long names that include their addresses.
   3. Free Places, which are locations where bikes where dropped outside a station, only give us coordinates and an approximation of the street they are in. None of those could be converted to a very clear URI, and thus, FreePlace with an identifier numeral was chosen.
   
   This is a bizarre situation where there is no clear label for each instance, and we hope it is not a problem, as the class each belongs to makes the IRI readable.
