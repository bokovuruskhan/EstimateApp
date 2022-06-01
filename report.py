from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

from config import MyApp
from util import get_upload_file_path
from datetime import datetime

app = MyApp.app


def config():
    pdfmetrics.registerFont(TTFont(MyApp.FONT_NAME, MyApp.FONT_FILE_PATH))


def generate_manager_report(project):
    file_path = get_upload_file_path(f"{datetime.now().date()}_report.pdf")
    my_canvas = Canvas(file_path, pagesize=letter)
    my_canvas.setLineWidth(.3)
    my_canvas.setFont('Piazzolla', 14)
    my_canvas.drawString(30, 750, 'OFFICIAL COMMUNIQUE')
    my_canvas.drawString(30, 735, 'OF ACME INDUSTRIES')
    my_canvas.drawString(500, 750, f"{datetime.now().date()}")
    my_canvas.line(480, 747, 580, 747)
    my_canvas.drawString(275, 725, 'Итоговая стоимость:')
    my_canvas.drawString(500, 725, f"{project.get_services_price_sum()}руб")
    my_canvas.line(408, 723, 580, 723)
    my_canvas.drawString(30, 703, 'Менеджер:')
    my_canvas.line(120, 700, 580, 700)
    my_canvas.drawString(120, 703, "JOHN DOE")

    y = 663
    for service in project.services:
        my_canvas.drawString(120, y, f"{service.name}")
        my_canvas.drawString(480, y, f"{service.price}руб")
        my_canvas.drawString(360, y, f"{service.get_margin_percent_str()}")
        my_canvas.line(120, y - 5, 580, y - 5)
        y -= 30

    my_canvas.save()
    return file_path


def generate_client_report(project):
    file_path = get_upload_file_path(f"{datetime.now().date()}_report.pdf")
    my_canvas = Canvas(file_path, pagesize=letter)
    my_canvas.setLineWidth(.3)
    my_canvas.setFont('Piazzolla', 14)
    my_canvas.drawString(30, 750, 'OFFICIAL COMMUNIQUE')
    my_canvas.drawString(30, 735, 'OF ACME INDUSTRIES')
    my_canvas.drawString(500, 750, f"{datetime.now().date()}")
    my_canvas.line(480, 747, 580, 747)
    my_canvas.drawString(275, 725, 'Итоговая стоимость:')
    my_canvas.drawString(500, 725, f"{project.get_services_price_sum()}руб")
    my_canvas.line(408, 723, 580, 723)
    my_canvas.drawString(30, 703, 'Менеджер:')
    my_canvas.line(120, 700, 580, 700)
    my_canvas.drawString(120, 703, "JOHN DOE")

    y = 663
    for service in project.services:
        my_canvas.drawString(120, y, f"{service.name}")
        my_canvas.drawString(480, y, f"{service.price}руб")
        my_canvas.line(120, y - 5, 580, y - 5)
        y -= 30

    my_canvas.save()
    return file_path
