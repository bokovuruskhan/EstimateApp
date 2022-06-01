import datetime

from flask import render_template, send_file
from flask import request
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

import admin
from config import MyApp
from model import Object, Project, Service

my_app = MyApp()
app = my_app.app
database = my_app.database

current_project = None

pdfmetrics.registerFont(TTFont("Piazzolla", "reportlab/piazzolla.ttf"))


def generate_estimate_manager_report(project_id):
    project = database.session.query(Project).filter(Project.id == project_id).first()

    filepath = app.config["UPLOAD_FOLDER"] + "/" + f"{datetime.datetime.now().date()}_report.pdf"
    my_canvas = canvas.Canvas(filepath, pagesize=letter)
    my_canvas.setLineWidth(.3)
    my_canvas.setFont('Piazzolla', 14)
    my_canvas.drawString(30, 750, 'OFFICIAL COMMUNIQUE')
    my_canvas.drawString(30, 735, 'OF ACME INDUSTRIES')
    my_canvas.drawString(500, 750, f"{datetime.datetime.now().date()}")
    my_canvas.line(480, 747, 580, 747)
    my_canvas.drawString(275, 725, 'Итоговая стоимость:')
    my_canvas.drawString(500, 725, f"{current_project.get_services_sum()}руб")
    my_canvas.line(408, 723, 580, 723)
    my_canvas.drawString(30, 703, 'Менеджер:')
    my_canvas.line(120, 700, 580, 700)
    my_canvas.drawString(120, 703, "JOHN DOE")

    y = 663
    for service in project.services:
        print("sss")
        my_canvas.drawString(120, y, f"{service.name}")
        my_canvas.drawString(480, y, f"{service.price}руб")
        my_canvas.drawString(360, y, f"{(service.margin * 100) - 100}%")
        my_canvas.line(120, y - 5, 580, y - 5)
        y -= 30

    my_canvas.save()
    return filepath


def generate_estimate_client_report(project_id):
    project = database.session.query(Project).filter(Project.id == project_id).first()

    filepath = app.config["UPLOAD_FOLDER"] + "/" + f"{datetime.datetime.now().date()}_report_client.pdf"
    my_canvas = canvas.Canvas(filepath, pagesize=letter)
    my_canvas.setLineWidth(.3)
    my_canvas.setFont('Piazzolla', 14)
    my_canvas.drawString(30, 750, 'OFFICIAL COMMUNIQUE')
    my_canvas.drawString(30, 735, 'OF ACME INDUSTRIES')
    my_canvas.drawString(500, 750, f"{datetime.datetime.now().date()}")
    my_canvas.line(480, 747, 580, 747)
    my_canvas.drawString(275, 725, 'Итоговая стоимость:')
    my_canvas.drawString(500, 725, f"{current_project.get_services_sum()}руб")
    my_canvas.line(408, 723, 580, 723)
    my_canvas.drawString(30, 703, 'Менеджер:')
    my_canvas.line(120, 700, 580, 700)
    my_canvas.drawString(120, 703, "JOHN DOE")

    y = 663
    for service in project.services:
        print("sss")
        my_canvas.drawString(120, y, f"{service.name}")
        my_canvas.drawString(480, y, f"{service.price}руб")
        my_canvas.line(120, y - 5, 580, y - 5)
        y -= 30

    my_canvas.save()
    return filepath


@app.route("/report/client")
def report_client():
    return send_file(generate_estimate_client_report(current_project.id), attachment_filename='report.pdf')


@app.route("/report/manager")
def report_manager():
    return send_file(generate_estimate_manager_report(current_project.id), attachment_filename='report.pdf')


@app.route("/object", methods=["POST"])
def create_object():
    name = request.form.get("name")
    database.session.add(Object(name=name))
    database.session.commit()
    return index()


@app.route("/project", methods=["POST"])
def create_project():
    name = request.form.get("name")
    object_id = request.form.get("object_id")
    database.session.add(Project(name=name, object_id=object_id))
    database.session.commit()
    return index()


@app.route("/project/<project_id>")
def set_current_project(project_id):
    global current_project
    current_project = database.session.query(Project).filter(Project.id == project_id).first()
    return index()


@app.route("/project/service/add", methods=["POST"])
def add_service_in_current_project():
    global current_project
    service_id = int(request.form.get("service_id"))
    current_project.services.append(database.session.query(Service).filter(Service.id == service_id).first())
    database.session.add(current_project)
    database.session.commit()
    return index()


@app.route("/")
def index():
    return render_template("index.html", current_project=current_project,
                           objects=database.session.query(Object).all(),
                           services=database.session.query(Service).all())


if __name__ == '__main__':
    database.create_all()
    admin.init()
    app.run()
