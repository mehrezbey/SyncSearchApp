from search_module.utils.elasticsearch_utils import index_doc, delete_doc, update_doc

from sqlalchemy import event

def after_insert_listener(mapper, connection, target):
    data = {k: v for k, v in target.__dict__.items() if k != '_sa_instance_state'}
    resp = index_doc(target.__table__.name, data)

def after_delete_listener(mapper, connection, target):
    data = {k: v for k, v in target.__dict__.items() if k != '_sa_instance_state'}
    resp = delete_doc(target.__table__.name, data)

def after_update_listener(mapper, connection, target):
    data = {k: v for k, v in target.__dict__.items() if k != '_sa_instance_state'}
    resp = update_doc(target.__table__.name, data)

# Main function : Every operation performed on the database will also be applied to the Elasticsearch cluster.
def synchronise(Base):
    for table_name, mapped_class in Base.classes.items():
        event.listen(mapped_class, 'after_insert', after_insert_listener)
        event.listen(mapped_class, 'after_delete', after_delete_listener)
        event.listen(mapped_class, 'after_update', after_update_listener)
