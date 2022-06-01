from flask import request, flash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.utils import redirect, secure_filename
import csv
from database.model import *
from database.util import save, get_group_by_name
from util import get_upload_file_path

app = MyApp.app
database = MyApp.database


def config():
    admin = Admin(app, name='EstimateApp', template_mode='bootstrap3')
    admin.add_view(ModelView(Object, database.session, "Объекты"))
    admin.add_view(ModelView(Project, database.session, "Проекты"))
    admin.add_view(ModelView(Service, database.session, "Услуги"))
    admin.add_view(ModelView(Group, database.session, "Группа услуг"))
    admin.add_view(ModelView(Company, database.session, "Компании"))


def read_services_from_csv(file_name):
    with open(get_upload_file_path(file_name), encoding=MyApp.ENCODING) as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        for row in reader:
            save(Service(name=row[0], group=get_group_by_name(row[1]), price=int(row[2]), margin=float(row[3])))


@app.route("/services/csv", methods=['GET', 'POST'])
def import_services_from_csv():
    if request.method == 'POST':
        if "file" not in request.files:
            flash("Файл не прикреплен.")
        else:
            file = request.files.get("file")
            if file:
                filename = secure_filename(file.filename)
                file.save(get_upload_file_path(filename))
                read_services_from_csv(filename)
    return redirect("/admin")
