from search_module.utils.elasticsearch_utils import index_doc, delete_doc, update_doc
from search_module.utils.colors import colors
from search_module.utils.logs import print_log
from sqlalchemy import event

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
