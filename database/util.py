from config import MyApp
from database.model import Group
from sqlalchemy.exc import SQLAlchemyError

database = MyApp.database


def save(obj):
    try:
        database.session.add(obj)
        database.session.commit()
    except SQLAlchemyError:
        database.session.rollback()


def get_all(obj_class):
    return database.session.query(obj_class).all()


def find_by_id(obj_class, obj_id):
    return database.session.query(obj_class).filter(obj_class.id == obj_id).first()


def get_group_by_name(name):
    group = database.session.query(Group).filter(Group.name == name).first()
    if group is None:
        group = Group(name=name)
        save(group)
        group = database.session.query(Group).filter(Group.name == name).first()
    return group
