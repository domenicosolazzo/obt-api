from . import entities
from flask import request, Response, jsonify
from jroc.pipelines.linkeddata.LinkedDataEntityPipeline import LinkedDataEntityPipeline
from werkzeug.exceptions import HTTPException
import urllib2
import json

@entities.route('/search')
def search():
    return "ciao"

@entities.route("/")
def main():
    uris = {
        "uri" : "%s" % (request.base_url,)
    }

    json_response = json.dumps(uris)
    return Response(json_response, mimetype="application/json")

@entities.route("/<entity_name>")
def entityMain(entity_name):
    basic_url = "%s" % (request.base_url)
    entity = {}
    pipeline = LinkedDataEntityPipeline(entity_name, name="LinkedData Pipeline")
    pipeline.execute()
    output = pipeline.getOutput()

    uniqueUri = output.get('entity-uri', {}).get('uri', None)
    entityName = entity_name

    if uniqueUri:
        uniqueName = uniqueUri.replace("http://dbpedia.org/resource/", "")
        basic_url = "%sentities/%s" % (request.url_root, uniqueName)
        entityName = uniqueName
        entity["redirected_from"] = request.base_url

    entity["name"] = entityName
    entity["types_uri"] = "%s/%s" % (basic_url, "types")
    entity["properties_uri"] = "%s/%s" %  (basic_url, "properties")
    result = {
        "data": entity,
        "uri": basic_url
    }
    json_response = json.dumps(result)
    return Response(json_response, mimetype="application/json")

@entities.route("/<entity_name>/types")
def entityTypes(entity_name):
    pipeline = LinkedDataEntityPipeline(entity_name, name="LinkedData Pipeline", withTypesAnnotation=True)
    pipeline.execute()
    output = pipeline.getOutput()

    result = output.get('entity-types', None)

    entity = {}
    entity["name"] = entity_name
    entity["uri"] = "%s" % (request.base_url)
    entity["entity_uri"] = "%sentities/%s" % (request.url_root, entity_name,)
    entity["data"] = result
    json_response = json.dumps(entity)
    return Response(json_response, mimetype="application/json")

@entities.route("/<entity_name>/properties")
def entityProperties(entity_name):
    entity = {}
    entity["name"] = entity_name
    entity["uri"] = "%s" % (request.url)
    entity["entity_uri"] = "%sentities/%s" % (request.url_root, entity_name,)

    if request.args.get('name'):
        propertyName = request.args.get('name')
        lang = request.args.get('lang') if request.args.get('lang') else None
        pipeline = LinkedDataEntityPipeline(entity_name, name="LinkedData Pipeline", withPropertyAnnotation=(True, [(urllib2.unquote(propertyName).decode('utf8'), lang)]))
        pipeline.execute()
        output = pipeline.getOutput()
        result = output.get('entity-property', {})
        if len(result) > 0:
            result = result.get('properties')
        entity["data"] = result
    else:
        fetchValues = True if request.args.get('fetch', None) else False
        pipeline = LinkedDataEntityPipeline(entity_name, name="LinkedData Pipeline", withPropertiesAnnotation=True, withPropertyValuesAnnotation=fetchValues)
        pipeline.execute()
        output = pipeline.getOutput()


        entityProperties = output.get('entity-properties', None)
        properties = entityProperties.get("properties", [])
        result = {}
        for propertyName in properties.keys():
            prop = {'uri': "", "name": propertyName}
            if fetchValues == True:
                prop["values"] = properties[propertyName]
            if not propertyName in result:
                result[propertyName] = prop
            prop["uri"] = "%s?name=%s" % (request.base_url, urllib2.quote(propertyName))
            result[propertyName] = prop
        entity["data"] = result

    json_response = json.dumps(entity)
    return Response(json_response, mimetype="application/json")
