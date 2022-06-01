from flask import render_template, send_file
from flask import request

import report
from database.util import save, get_all, find_by_id
from report import generate_client_report, generate_manager_report
import admin
from config import MyApp
from database.model import Object, Project, Service, Company, Manager

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
def get_client_report():
    return send_file(generate_client_report(CurrentProject.get_instance().get_current_project()))


@app.route("/report/manager")
def get_manager_report():
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


@app.route("/company/save", methods=["POST"])
def save_company():
    if CurrentProject.get_instance().get_current_project().company is None:
        company = Company(name=request.form.get("name"),
                          index=request.form.get("index"),
                          city=request.form.get("city"),
                          address=request.form.get("address"),
                          phone=request.form.get("phone"),
                          site=request.form.get("site"),
                          okpo=request.form.get("okpo"),
                          okdp=request.form.get("okdp"))
        CurrentProject.get_instance().get_current_project().company = company
        save(CurrentProject.get_instance().get_current_project())
    else:
        company = CurrentProject.get_instance().get_current_project().company
        company.name = request.form.get("name")
        company.index = request.form.get("index")
        company.city = request.form.get("city")
        company.address = request.form.get("address")
        company.phone = request.form.get("phone")
        company.site = request.form.get("site")
        company.okpo = request.form.get("okpo")
        company.okdp = request.form.get("okdp")
        save(company)
    return index()


@app.route("/manager/save", methods=["POST"])
def save_manager():
    if CurrentProject.get_instance().get_current_project().manager is None:
        manager = Manager(name=request.form.get("name"))
        CurrentProject.get_instance().get_current_project().manager = manager
        save(CurrentProject.get_instance().get_current_project())
    else:
        manager = CurrentProject.get_instance().get_current_project().manager
        manager.name = request.form.get("name")
        save(manager)
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
