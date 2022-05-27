from config import MyApp

database = MyApp.database


class Object(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(255), nullable=False)