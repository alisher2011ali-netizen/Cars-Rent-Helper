import flet as ft

from app.ui.builders.base import Builder


class FirstLaunchBuilder(Builder):
    def build_first_launch_view(self) -> ft.View:
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

        def on_continue(e):
            self.db_manager.set_setting("is_first_launch", "false")
            self.page.go("/cars")

        content = ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(
                            icon=ft.Icons.CAR_RENTAL,
                            size=100,
                            color=ft.Colors.PRIMARY,
                            align=ft.Alignment.CENTER,
                        ),
                        ft.Text(
                            self.localization.app_name,
                            size=28,
                            weight="bold",
                        ),
                    ],
                ),
                ft.Text(
                    self.localization.hello_text,
                    size=24,
                    weight="bold",
                    text_align="center",
                ),
                ft.Column(
                    [
                        ft.Text(
                            self.localization.choose_language,
                            size=20,
                            text_align="center",
                        ),
                        ft.Dropdown(
                            options=[
                                ft.DropdownOption(key="ru", text="Русский"),
                                ft.DropdownOption(key="en", text="English"),
                                ft.DropdownOption(key="zh", text="中文"),
                            ],
                            value=self.db_manager.get_setting("language") or "ru",
                            width=200,
                            on_select=on_language_change,
                        ),
                    ],
                    spacing=5,
                ),
                ft.Column(
                    [
                        ft.Text(
                            self.localization.choose_currency,
                            size=20,
                            text_align="center",
                        ),
                        ft.Dropdown(
                            options=[
                                ft.DropdownOption(key="RUB", text="RUB  ₽"),
                                ft.DropdownOption(key="USD", text="USD  $"),
                                ft.DropdownOption(key="CNY", text="CNY  ¥"),
                                ft.DropdownOption(key="KGS", text="KGS"),
                            ],
                            value=self.db_manager.get_setting("currency") or "RUB",
                            width=200,
                            on_select=on_currency_change,
                        ),
                    ],
                    spacing=5,
                ),
                ft.ElevatedButton(
                    ft.Text(self.localization.continue_text, size=20),
                    icon=ft.Icon(ft.Icons.ARROW_FORWARD, size=20),
                    align=ft.Alignment.CENTER,
                    on_click=on_continue,
                ),
            ],
            alignment=ft.Alignment.CENTER,
            horizontal_alignment=ft.Alignment.CENTER,
            spacing=20,
        )
        return ft.View(route="/first_launch", controls=[content])
