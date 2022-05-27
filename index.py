from flask import render_template

from config import MyApp
from model import Object

my_app = MyApp()
app = my_app.app
database = my_app.database


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    database.create_all()
    app.run()
