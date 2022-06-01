import os

from config import MyApp

app = MyApp.app


def get_upload_file_path(filename):
    return os.path.join(app.config['UPLOAD_FOLDER'], filename)
