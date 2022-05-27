from sqlalchemy.orm import backref

from config import MyApp

database = MyApp.database


class Object(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(255), nullable=False)
    projects = database.relationship('Project',
                                     backref=database.backref('projects', lazy=True))


class Project(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(255), nullable=False)
    object_id = database.Column(database.Integer, database.ForeignKey('object.id'), nullable=False)
    services = database.relationship("Service", secondary="ProjectServices")


class Service(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(255), nullable=False)
    price = database.Column(database.REAL, nullable=False)
    margin = database.Column(database.REAL, nullable=False, default=0.0)
    projects = database.relationship("Project", secondary="ProjectServices")


class ProjectServices(database.Model):
    __tablename__ = "ProjectServices"
    id = database.Column(database.Integer, primary_key=True)
    project_id = database.Column(database.Integer, database.ForeignKey('project.id'), nullable=False)
    service_id = database.Column(database.Integer, database.ForeignKey('service.id'), nullable=False)
    project = database.relationship(Project, backref=backref("ProjectServices", cascade="all, delete-orphan"))
    service = database.relationship(Service, backref=backref("ProjectServices", cascade="all, delete-orphan"))
