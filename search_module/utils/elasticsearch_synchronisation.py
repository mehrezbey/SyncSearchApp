from flask import current_app
from sqlalchemy.ext.automap import automap_base
from elasticsearch.helpers import bulk, BulkIndexError 
from sqlalchemy import event
import os
from search_module.utils.elasticsearch_utils import index_doc, delete_doc, update_doc,create_client,database_name
from search_module.utils.colors import colors
from search_module.utils.logs import print_log

def after_insert_listener(mapper, connection, target):
    data = {k: v for k, v in target.__dict__.items() if k != '_sa_instance_state'}
    resp = index_doc(target.__table__.name, data)
    if("error" in resp):
        print(resp["error"])
    else:
        print_log('insert', target.__table__.name, data, resp)

def after_delete_listener(mapper, connection, target):
    data = {k: v for k, v in target.__dict__.items() if k != '_sa_instance_state'}
    resp = delete_doc(target.__table__.name, data)
    if("error" in resp):
        print(resp["error"])
    else:
        print_log('delete', target.__table__.name, data, resp)

def after_update_listener(mapper, connection, target):
    data = {k: v for k, v in target.__dict__.items() if k != '_sa_instance_state'}
    resp = update_doc(target.__table__.name, data)
    if("error" in resp):
        print(resp["error"])
    else:
        print_log('update', target.__table__.name, data, resp)

# Main function : Every operation performed on the database will also be applied to the Elasticsearch cluster.
def synchronise(Base):
    for table_name, mapped_class in Base.classes.items():
        event.listen(mapped_class, 'after_insert', after_insert_listener)
        event.listen(mapped_class, 'after_delete', after_delete_listener)
        event.listen(mapped_class, 'after_update', after_update_listener)

def ingest_data_to_elasticsearch(db,batch_size=500):
    database_schema=[]
    es_client = create_client()
    if not es_client.ping():
        return {"error":"Could not connect to Elasticsearch!"}
    index_name = database_name +"-"+os.getenv("TABLE_NAME")
    index_exists = es_client.indices.exists(index=index_name)
    if(index_exists):return
    Base = automap_base()
    with current_app.app_context():
        Base.prepare(db.engine,reflect=True)
        tables = Base.classes.keys()
        for table_name in tables:
            table={}
            model = Base.classes[table_name]
            table["table_name"] = table_name
            rows = db.session.query(model).all()
            columns = model.__table__.columns.keys()
            table["columns"]= columns
            database_schema.append(table)
            total_rows = db.session.query(model).count()
            pk = columns[0] # Assuming that the primary key of the table is the first column
            doc = {"primary_key": pk } # We will save the name of  the primary key because we will need it for synchronisation
            es_client.index(index=database_name+"-"+table_name.lower(), document=doc)
            for start in range(0, total_rows, batch_size):
                rows = db.session.query(model).offset(start).limit(batch_size).all()
                data = [
                    {
                        '_index': database_name +"-"+table_name.lower(),
                        '_id': getattr(row,pk ),
                        '_source': {col: getattr(row, col) for col in columns}
                    }
                    for row in rows
                ]
                try:
                    bulk(es_client, data)
                except BulkIndexError as e:
                    for error in e.errors:
                        print("Error indexing document:", error)
                    raise
        print("Data was successfully indexed into ElasticSearch")
        print(database_schema)