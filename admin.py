from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from model import *

from config import MyApp


def init():
    admin = Admin(MyApp.app, name='EstimateApp', template_mode='bootstrap3')
    admin.add_view(ModelView(Object, MyApp.database.session))
    admin.add_view(ModelView(Project, MyApp.database.session))
    admin.add_view(ModelView(Service, MyApp.database.session))
