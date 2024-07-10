from elasticsearch import Elasticsearch, NotFoundError

import os

database_name = os.environ.get("DATABASE_NAME")

def create_client():
    username=os.environ.get('ELASTIC_USERNAME')
    password = os.environ.get('ELASTIC_PASSWORD')
    es_client = Elasticsearch(
    ['http://localhost:9200'],
    basic_auth=(username, password),
    request_timeout = 60
    )
    return es_client
    

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
    es_client = create_client()
    if not es_client.ping():
        return {"error":"Could not connect to Elasticsearch!"}
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
        return extract_search_results(result), 200
    
    except NotFoundError:
        return {"error":"Index not found!"}

    except Exception as e:
        return {"error":"An unexpected error occurred: " + str(e)}


def index_doc(index_name, data):
    es_client = create_client()
    if not es_client.ping():
        return {"error":"Could not connect to Elasticsearch!"}
    try:
        p_key = query_index(database_name+"-"+index_name,"",["primary_key"],1,5)[0]['hits'][0]["primary_key"]
        resp = es_client.index(index=database_name+"-"+index_name, document=data, id=data[p_key])
        return resp
    except Exception as e:
        return {"error":"An unexpected error occurred: " + str(e)}

def delete_doc(index_name, data):
    es_client = create_client()
    if not es_client.ping():
        return {"error":"Could not connect to Elasticsearch!"}
    try:
        p_key = query_index(database_name+"-"+index_name,"",["primary_key"],1,5)[0]['hits'][0]["primary_key"]
        resp = es_client.delete(index=database_name+"-"+index_name, id=data[p_key])
        return resp
    except Exception as e:
        return {"error":"An unexpected error occurred: " + str(e)}

def update_doc(index_name, data):
    es_client = create_client()
    if not es_client.ping():
        return {"error":"Could not connect to Elasticsearch!"}
    try:
        p_key = query_index(database_name+"-"+index_name,"",["primary_key"],1,5)[0]['hits'][0]["primary_key"]
        resp = es_client.update(index=database_name+"-"+index_name, doc = data, id=data[p_key])
        return resp
    except Exception as e:
        return {"error":"An unexpected error occurred: " + str(e)}