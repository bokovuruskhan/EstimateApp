from sqlalchemy.orm import backref

from config import MyApp

database = MyApp.database


class Object(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(255), nullable=False)
    projects = database.relationship('Project',
                                     backref=database.backref('object', lazy=True))

    def __str__(self):
        return self.name


class Project(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(255), nullable=False)
    object_id = database.Column(database.Integer, database.ForeignKey('object.id'), nullable=False)
    services = database.relationship("Service", secondary="ProjectServices")

    def get_services_price_sum(self):
        services_price_sum = 0
        for service in self.services:
            services_price_sum += service.price * service.margin
        return services_price_sum

    def __str__(self):
        return self.name


class Group(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(255), nullable=False, unique=True)
    services = database.relationship('Service',
                                     backref=database.backref('group', lazy=True))

    def __str__(self):
        return self.name


class Service(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(255), nullable=False, unique=True)
    price = database.Column(database.REAL, nullable=False)
    margin = database.Column(database.REAL, nullable=False, default=1.0)
    projects = database.relationship("Project", secondary="ProjectServices")
    group_id = database.Column(database.Integer, database.ForeignKey('group.id'), nullable=False)

    def get_margin_percent_str(self):
        return f"{round((self.margin - 1) * 100, 2)}%"

    def __str__(self):
        return self.name


class ProjectServices(database.Model):
    __tablename__ = "ProjectServices"
    id = database.Column(database.Integer, primary_key=True)
    project_id = database.Column(database.Integer, database.ForeignKey('project.id'), nullable=False)
    service_id = database.Column(database.Integer, database.ForeignKey('service.id'), nullable=False)
    project = database.relationship(Project, backref=backref("ProjectServices", cascade="all, delete-orphan"))
    service = database.relationship(Service, backref=backref("ProjectServices", cascade="all, delete-orphan"))
