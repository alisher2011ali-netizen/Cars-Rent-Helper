from flet import View, Column, Text, Dropdown, DropdownOption, Alignment, Colors

from app.ui.builders.base import Builder


class FirstLaunchBuilder(Builder):
    def build_first_launch_view(self) -> View:
        def on_language_change(e):
            selected_language = e.control.value
            self.db_manager.set_setting("language", selected_language)
            self.localization.load_lang(selected_language)

            self.page.views.clear()
            self.page.views.append(self.build_first_launch_view())

        def on_currency_change(e):
            selected_currency = e.control.value
            self.db_manager.set_setting("currency", selected_currency)
            self.localization.currency = selected_currency

            self.page.views.clear()
            self.page.views.append(self.build_first_launch_view())

        content = Column(
            [
                Text(
                    self.localization.hello_text,
                    size=24,
                    weight="bold",
                    text_align="center",
                ),
                Text(
                    self.localization.choose_language,
                    size=20,
                    text_align="center",
                ),
                Dropdown(
                    options=[
                        DropdownOption(key="ru", text="Русский"),
                        DropdownOption(key="en", text="English"),
                    ],
                    value=self.db_manager.get_setting("language") or "en",
                    align=Alignment.CENTER,
                    width=200,
                    on_select=on_language_change,
                ),
                Text(self.localization.choose_currency, size=20, text_align="center"),
                Dropdown(
                    options=[
                        DropdownOption(key="RUB", text="RUB"),
                        DropdownOption(key="USD", text="USD"),
                        DropdownOption(key="KGS", text="KGS"),
                        DropdownOption(key="CNY", text="CNY"),
                    ],
                    value=self.db_manager.get_setting("currency") or "RUB",
                    align=Alignment.CENTER,
                    width=200,
                    on_select=on_currency_change,
                ),
            ],
            alignment=Alignment.CENTER,
            horizontal_alignment=Alignment.CENTER,
            spacing=20,
        )
        return View(route="/first_launch", controls=[content])
