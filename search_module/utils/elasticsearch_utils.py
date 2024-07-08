from elasticsearch import Elasticsearch, NotFoundError  # type: ignore
from flask import  jsonify

def extract_search_results(response):
    to_return = {}
    to_return["total"] =0
    to_return["hits"] = []
    if 'hits' in response and 'hits' in response['hits'] and 'total' in response['hits']:
        documents = response['hits']['hits']
        to_return["total"] = int(response["hits"]["total"]["value"])
        hits = []
        for hit in documents:
            source = hit.get('_source', {})
            hits.append(source)
        to_return["hits"] = hits

    return to_return

def query_index(index, query, fields , page, per_page ):
    es_client = Elasticsearch(
    ['http://localhost:9200'],
    basic_auth=("elastic", 'mehrez'),
    request_timeout = 60
    )
    if es_client.ping():
        print("Connected to Elasticsearch!")
    else:
        return jsonify(error="Could not connect to Elasticsearch!"), 500
    
    try:
        result = es_client.search(
            index = index,
            body={'query':{
                        "query_string": {
                            "query": "*"+query+"*",
                            'fields': fields
                            }
                        },
                        'from': (page - 1) * per_page,
                        'size': per_page
                    }
        )

    except NotFoundError:
        return jsonify(error="Index not found!"), 404

    except Exception as e:
        return jsonify(error="An unexpected error occurred: " + str(e)), 500

    return extract_search_results(result),200