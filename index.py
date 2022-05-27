from flask import render_template

from config import MyApp

my_app = MyApp()
app = my_app.app


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
