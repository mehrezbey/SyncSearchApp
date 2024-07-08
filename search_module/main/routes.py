from elasticsearch import Elasticsearch, NotFoundError  # type: ignore
from flask import Flask, request, jsonify,Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from elasticsearch.helpers import bulk, BulkIndexError # type: ignore
import os
import json
from sqlalchemy import event
from sqlalchemy import text
data_base_name = "nation"
from search_module.utils.elasticsearch_utils import query_index
main = Blueprint('main',__name__)



@main.route('/search')
def search():
    if(not request.args.get('table')):
        return jsonify(message="Error! Table name is mandatory!"), 405
    if(request.args.get('table') !="_all"):
        index = data_base_name+"-"+ f"{request.args.get('table')}"
    else: 
        index = f"{request.args.get('table')}"
    query = request.args.get('query', default='')
    fields = request.args.get('fields',default='')
    if(fields==''):
        fields = ['*']
    else:
        fields = fields.split(",")
    page = request.args.get('page',default = 1,type = int)
    per_page = request.args.get('per_page',default = 5,type = int)
    return query_index(index,query,fields,page,per_page)