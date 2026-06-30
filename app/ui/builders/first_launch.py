from flet import View, Column, Text, Dropdown

from app.ui.builders.base import Builder
from app.services.localization import AppStrings


class FirstLaunchBuilder(Builder):
    def build_first_launch_view(self) -> View:
        content = Column(
            [
                Text(
                    AppStrings.hello_text,
                    size=24,
                    weight="bold",
                ),
                Text(AppStrings.choose_language, size=16),
                Dropdown(
                    options=[
                        {"label": "Русский", "value": "ru"},
                        {"label": "English", "value": "en"},
                    ],
                    value="ru",
                    on_change=self._on_language_change,
                ),
            ],
            alignment="center",
            horizontal_alignment="center",
            spacing=20,
        )
        return View(route="/first_launch", controls=[content])

    def _on_language_change(self, e):
        selected_language = e.control.value
        self.db_manager.set_setting("app_language", selected_language)
        # Here you might want to trigger a UI update or reload the app with the new language settings.
