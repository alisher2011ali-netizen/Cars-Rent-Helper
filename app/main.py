from flet import Page, Theme, PageTransitionsTheme, PageTransitionTheme, run
import traceback

from app.database.models import init_db
from app.ui.router import UIRouter


def main(page: Page):
    try:
        init_db()

        page.theme = Theme(
            font_family="Arial",
            page_transitions=PageTransitionsTheme(
                android=PageTransitionTheme.NONE, linux=PageTransitionTheme.NONE
            ),
        )
        ui = UIRouter(page)
        ui.build()

    except Exception as ex:
        print("❌ ОШИБКА ПРИ ЗАПУСКЕ ПРИЛОЖЕНИЯ:")
        print(traceback.format_exc())


if __name__ == "__main__":
    print("The app has been setup")
    run(main=main)
