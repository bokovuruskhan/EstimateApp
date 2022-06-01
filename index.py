from flask import render_template, send_file
from flask import request

import report
from database.util import save, get_all, find_by_id
from report import generate_client_report, generate_manager_report
import admin
from config import MyApp
from database.model import Object, Project, Service

app = MyApp.app
database = MyApp.database


class CurrentProject:
    __instance = None

    def __init__(self):
        self._current_project = database.session.query(Project).first()

    def set_current_project(self, project):
        self._current_project = project

    def get_current_project(self):
        return self._current_project

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.__instance = super(CurrentProject, cls).__new__(cls)
        return cls.__instance

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = CurrentProject()
        return cls.__instance


@app.route("/report/client")
def report_client():
    return send_file(generate_client_report(CurrentProject.get_instance().get_current_project()))


@app.route("/report/manager")
def report_manager():
    return send_file(generate_manager_report(CurrentProject.get_instance().get_current_project()))


@app.route("/object", methods=["POST"])
def add_object():
    name = request.form.get("name")
    save(Object(name=name))
    return index()


@app.route("/project", methods=["POST"])
def add_project():
    name = request.form.get("name")
    object_id = request.form.get("object_id")
    save(Project(name=name, object_id=object_id))
    return index()


@app.route("/project/<project_id>")
def set_current_project(project_id):
    CurrentProject.get_instance().set_current_project(find_by_id(Project, project_id))
    return index()


@app.route("/project/service/add", methods=["POST"])
def add_service_in_current_project():
    service_id = int(request.form.get("service_id"))
    CurrentProject.get_instance().get_current_project().services.append(find_by_id(Service, service_id))
    save(CurrentProject.get_instance().get_current_project())
    return index()


@app.route("/")
def index():
    return render_template("index.html", current_project=CurrentProject.get_instance().get_current_project(),
                           objects=get_all(Object),
                           services=get_all(Service))


if __name__ == '__main__':
    database.create_all()
    admin.config()
    report.config()
    app.run()
