from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.utils import redirect

from model import *

from config import MyApp

app = MyApp.app
database = MyApp.database


@app.route("/data/import")
def import_data():
    return redirect("/admin")


def init():
    admin = Admin(app, name='EstimateApp', template_mode='bootstrap3')
    admin.add_view(ModelView(Object, database.session))
    admin.add_view(ModelView(Project, database.session))
    admin.add_view(ModelView(Service, database.session))
