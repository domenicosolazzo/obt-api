class Queries(object):

    def __init__(self):
        pass

    # Fetch all the properties and values of a given resource
    QUERY_PROPERTIES_VALUES = """
            SELECT ?property ?propValue WHERE {
                <http://dbpedia.org/resource/%s> ?property ?propValue .
            }
    """

    # Fetch all the properties of a given resource
    QUERY_PROPERTIES = """
            SELECT DISTINCT ?property  WHERE {
                <http://dbpedia.org/resource/%s> ?property ?propValue .
            }
    """

    # Fetch value for a given property
    QUERY_PROPERTIES_VALUES_EXACT_MATCH = """
        SELECT ?property ?propValue WHERE {
            <http://dbpedia.org/resource/%s> ?property ?propValue .
            FILTER regex(str(?property), "^%s$")
        }
    """

    QUERY_PROPERTIES_VALUES_EXACT_MATCH_WITH_LANG = """
        SELECT ?property ?propValue WHERE {
            <http://dbpedia.org/resource/%s> ?property ?propValue .
            FILTER regex(str(?property), "^%s$")
            FILTER(langMatches(lang(?propValue), "%s"))
        }
    """

    # Fetch all the page disambiguates
    QUERY_WIKI_PAGE_DISAMBIGUATES = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX dbo: <http://dbpedia.org/ontology/>
            PREFIX dc: <http://purl.org/dc/elements/1.1/>
            PREFIX : <http://dbpedia.org/resource/>
            PREFIX dbpedia2: <http://dbpedia.org/property/>
            PREFIX dbpedia: <http://dbpedia.org/>
            SELECT DISTINCT ?syn WHERE {
                {   ?disPage dbpedia:wikiPageDisambiguates <http://dbpedia.org/resource/%s> .
                    ?disPage dbpedia:wikiPageDisambiguates ?syn .
                }
                UNION
                {
                    <http://dbpedia.org/resource/%s> dbpedia:wikiPageDisambiguates ?syn .
                }
            }
    """
    # Fetch the thumbnail of a given resource
    QUERY_THUMBNAIL = """
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
            SELECT ?thumbnail
            WHERE {
              <http://dbpedia.org/resource/%s> dbpedia-owl:thumbnail ?thumbnail .
            }
            LIMIT 1
    """

    # Fetch the unique URI of a given resource
    QUERY_SPARQL_URI = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX dbo: <http://dbpedia.org/ontology/>

            SELECT ?s WHERE {
              {
                ?s rdfs:label "%s"@en ;
                   a owl:Thing .
              }
              UNION
              {
                ?altName rdfs:label "%s"@en ;
                         dbo:wikiPageRedirects ?s .
              }
            }
    """

    # Fetch URI of entities which have the label starting with a given string
    QUERY_SPARQL_URI_STARTWITH = """
        SELECT ?uri ?label WHERE
        {
            ?uri <http://www.w3.org/2000/01/rdf-schema#label> ?label .
            FILTER regex(str(?uri), "^http://dbpedia.org/resource/%s")
        }LIMIT 10
    """


    # Fetch the basic info of a given resource
    QUERY_BASIC_INFO = """
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?comment, ?label, ?abstract, ?name
            WHERE {
              <http://dbpedia.org/resource/%s>  rdfs:label ?label; rdfs:comment ?comment; foaf:name ?name .
              FILTER(langMatches(lang(?name), "EN"))
              FILTER(langMatches(lang(?comment), "EN"))
              FILTER(langMatches(lang(?label), "EN"))
            }
            LIMIT 5
    """

    # Fetch entity types
    QUERY_ENTITY_TYPES = """
        PREFIX yago: <http://dbpedia.org/class/yago/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT ?type  WHERE {
            <http://dbpedia.org/resource/%s> rdf:type ?type.
        }LIMIT 100
    """
