from flask import request, jsonify,Blueprint
import os
from search_module.utils.elasticsearch_utils import query_index
from search_module import Base,db
from sqlalchemy.orm import sessionmaker


database_name = os.getenv("DATABASE_NAME")

main = Blueprint('main',__name__)

@main.route('/search')
def search():
    if(not request.args.get('table')):
        return jsonify(message="Error! Table name is mandatory!"), 405
    if(request.args.get('table') !="_all"):
        index = database_name+"-"+ f"{request.args.get('table')}"
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

@main.route('/test')
def test():
    table = Base.classes.vips
    Session = sessionmaker(bind=db.engine)
    session = Session()

    new_row = table(vip_id=7, name='carlos')
    session.add(new_row)

    new_row = table(vip_id=8, name='rog')
    session.add(new_row)

    existing_row = session.query(table).filter_by(vip_id=5).first()
    existing_row.name = 'rafael'

    edel = session.query(table).filter_by(vip_id=7).first()
    session.delete(edel)

    session.commit()
    session.close()
    return"" ,200