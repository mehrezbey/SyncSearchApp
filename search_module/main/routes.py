from flask import request, jsonify,Blueprint
from flask_restx import fields , Resource

import os
from search_module.utils.elasticsearch_utils import query_index
from search_module import Base,db
from sqlalchemy.orm import sessionmaker
from . import main_namespace

database_name = os.getenv("DATABASE_NAME")

# main = Blueprint('main',__name__)


#---------------------------- Swagger Models
query_model  =main_namespace.model( 
    'query_doc',{
        'table':fields.String(required=True, description="The name of the table. Write '_all' if you want the search to include all tables."),
        'query':fields.String(required=False,description="The text to search. If you want to return all documents, do not write anything."),
        'fields':fields.String(required=False,description="The fields of the query seperated by ','. If you want to include all the fields do not write anything."),
        'page':fields.Integer(required=False,description="The number of the page starting from 1. The default value = 1"),
        'per_page':fields.Integer(required=False,description="The number of documents in each page. The default value = 5")
    }
)

@main_namespace.route('/search', methods=["POST"])
class Search(Resource):
    @main_namespace.expect(query_model)
    def post(self):
        req = request.get_json()
        if(not ("table" in req)):
            return jsonify(message="Error! Table name is mandatory!"), 405
        if(req["table"] !="_all"):
            index = database_name+"-"+ req["table"]
        else: 
            index = req["table"]
        if("query" in req):
            query = req["query"]
        else:
            query=""
        if("fields" in req):
            fields = req["fields"]
        else:
            fields=''
        if(fields==''):
            fields = ['*']
        else:
            fields = fields.split(",")
        if("page" in req):
            page = int(req["page"])
        else:
            page=1
        if("per_page" in req):
            per_page = int(req["per_page"])
        else:
            per_page=5
        return query_index(index,query,fields,page,per_page)

