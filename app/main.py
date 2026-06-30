from flet import (
    Page,
    Theme,
    PageTransitionsTheme,
    PageTransitionTheme,
    run,
)
import logging

from app.database.models import init_db
from app.ui.router import UIRouter
from app.services.logging import setup_logging


def main(page: Page):
    try:
        init_db()

        page.theme = Theme(
            font_family="Arial",
            page_transitions=PageTransitionsTheme(
                android=PageTransitionTheme.NONE, linux=PageTransitionTheme.NONE
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
    run(main=main)
