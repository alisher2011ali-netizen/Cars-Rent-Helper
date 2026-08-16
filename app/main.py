import flet as ft
import logging

from database.models import init_db
from ui.router import UIRouter
from services.logging import setup_logging


def main(page: ft.Page):
    try:
        init_db()

        page.fonts = {"NotoSansSC": "assets/fonts/NotoSansSC-Regular.ttf"}
        page.theme = ft.Theme(
            font_family="NotoSansSC",
            page_transitions=ft.PageTransitionsTheme(
                android=ft.PageTransitionTheme.NONE, linux=ft.PageTransitionTheme.NONE
            ),
        )
        page.window.width = 360
        page.window.height = 780
        ui = UIRouter(page)
        ui.build()

    except Exception as ex:
        logging.exception("An unexpected error occurred while running the app.")


if __name__ == "__main__":
    setup_logging()
    print("The app has been setup")
    ft.run(main=main)
