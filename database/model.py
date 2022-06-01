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


class Company(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(255), nullable=False)
    index = database.Column(database.String(255), nullable=False)
    city = database.Column(database.String(255), nullable=False)
    address = database.Column(database.String(255), nullable=False)
    phone = database.Column(database.String(255), nullable=False)
    site = database.Column(database.String(255), nullable=False)
    okpo = database.Column(database.String(255), nullable=False)
    okdp = database.Column(database.String(255), nullable=False)
    projects = database.relationship('Project',
                                     backref=database.backref('company', lazy=True))


class Project(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(255), nullable=False)
    object_id = database.Column(database.Integer, database.ForeignKey('object.id'), nullable=False)
    company_id = database.Column(database.Integer, database.ForeignKey('company.id'), nullable=True)
    services = database.relationship("Service", secondary="ProjectServices")

    def get_services_price_sum(self):
        services_price_sum = 0
        for service in self.services:
            services_price_sum += service.price * service.margin
        return round(services_price_sum, 2)

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

    def get_margin_price(self):
        return round(self.price * self.margin, 2)

    def __str__(self):
        return self.name


class ProjectServices(database.Model):
    __tablename__ = "ProjectServices"
    id = database.Column(database.Integer, primary_key=True)
    project_id = database.Column(database.Integer, database.ForeignKey('project.id'), nullable=False)
    service_id = database.Column(database.Integer, database.ForeignKey('service.id'), nullable=False)
    project = database.relationship(Project, backref=backref("ProjectServices", cascade="all, delete-orphan"))
    service = database.relationship(Service, backref=backref("ProjectServices", cascade="all, delete-orphan"))
