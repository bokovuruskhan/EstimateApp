from flask import render_template
from flask import request
from config import MyApp
from model import Object, Project
import admin

my_app = MyApp()
app = my_app.app
database = my_app.database

current_project = None


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


@app.route("/")
def index():
    return render_template("index.html", current_project=current_project,
                           objects=database.session.query(Object).all())


if __name__ == '__main__':
    database.create_all()
    admin.init()
    app.run()
