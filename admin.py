import os
from io import TextIOWrapper

from flask import request, flash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.utils import redirect, secure_filename

from model import *

app = MyApp.app
database = MyApp.database


def get_file_path(filename):
    return os.path.join(app.config['UPLOAD_FOLDER'], filename)


def read_services_from_csv(filename):
    import csv
    with open(get_file_path(filename), encoding="UTF-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in reader:
            if database.session.query(Service).filter(Service.name == row[0]).first() is None:
                database.session.add(Service(name=row[0], price=int(row[1]), margin=float(row[2])))
        database.session.commit()


@app.route("/data/import", methods=['GET', 'POST'])
def import_data():
    if request.method == 'POST':
        if "file" not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files.get("file")
        if file:
            filename = secure_filename(file.filename)
            file.save(get_file_path(filename))
            read_services_from_csv(filename)
    return redirect("/admin")


def init():
    admin = Admin(app, name='EstimateApp', template_mode='bootstrap3')
    admin.add_view(ModelView(Object, database.session))
    admin.add_view(ModelView(Project, database.session))
    admin.add_view(ModelView(Service, database.session))
