from flet import Page
import flet as ft
import traceback

from app.database.models import init_db
from app.ui.router import UIRouter


def main(page: Page):
    try:
        init_db()

        page.theme = ft.Theme(font_family="Arial")
        ui = UIRouter(page)
        ui.build()

    except Exception as ex:
        print("❌ ОШИБКА ПРИ ЗАПУСКЕ ПРИЛОЖЕНИЯ:")
        print(traceback.format_exc())


if __name__ == "__main__":
    print("The app has been setup")
    ft.run(main=main)
