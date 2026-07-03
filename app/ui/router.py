import flet as ft
import logging
import time

from app.ui.builders import Builder


class UIRouter:
    def __init__(self, page: ft.Page):
        self.page = page
        self.builder = Builder(self.page)

    def _set_navigation_bar(self, route_index: int):
        self.page.navigation_bar = self.builder._get_nav_bar(route_index)
        self.page.update()

    def build(self):
        self.page.title = "Cars Rental App"
        self.page.on_route_change = self.route_change
        self.page.route = self._set_navigation_bar(0)
        try:
            if self.builder.db_manager.get_setting("is_first_launch") != "false":
                self.builder.db_manager.set_setting("is_first_launch", "true")
                view = self.builder.build_first_launch_view()
                self.page.views.clear()
                self.page.views.append(view)
                self.page.update()
            else:
                view = self.builder.build_home_view()
                self.page.views.clear()
                self.page.views.append(view)
                self.page.update()
        except Exception as ex:
            logging.exception("An error occurred while initializing.")
            error_content = ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            self.builder.localization.error_initializing,
                            size=20,
                            weight="bold",
                            color=ft.Colors.RED,
                        ),
                        ft.Text(str(ex), size=14, color=ft.Colors.RED_800),
                    ],
                    alignment="center",
                    horizontal_alignment="center",
                    spacing=20,
                ),
                padding=40,
                bgcolor=ft.Colors.WHITE,
                expand=True,
            )
            error_view = ft.View(route="/", controls=[error_content])
            self.page.views.clear()
            self.page.views.append(error_view)
            self.page.update()

    def route_change(self, e):
        """Handler for route change events. Updates the page view based on the new route.
        :params
        e: RouteChangeEvent"""

        try:
            match e.route:
                case "/":
                    view = self.builder.build_home_view()
                case "/first_launch":
                    view = self.builder.build_first_launch_view()
                case "/cars":
                    view = self.builder.build_cars_view()
                case "/tenants":
                    view = self.builder.build_tenants_view()
                case "/rentals":
                    view = self.builder.build_rentals_view()
                case "/finances":
                    view = self.builder.build_finances_view()
                case "/add_car":
                    view = self.builder.build_add_car_view()
                case "/add_tenant":
                    view = self.builder.build_add_tenant_view()
                case "/add_rental":
                    view = self.builder.build_add_rental_view()
                case "/add_payment":
                    view = self.builder.build_add_payment_view()
                case _:
                    view = self.builder.build_home_view()
        except Exception as ex:
            logging.exception(f"An error occurred while changing route to {e.route}.")
            error_content = ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            self.builder.localization.error_loading,
                            size=20,
                            weight="bold",
                            color=ft.Colors.RED,
                        ),
                        ft.Text(
                            f"{self.builder.localization.route}: {e.route}",
                            size=12,
                            color=ft.Colors.BLACK_87,
                        ),
                        ft.Text(
                            f"{self.builder.localization.error}: {str(ex)}",
                            size=12,
                            color=ft.Colors.RED_800,
                        ),
                    ],
                    alignment="center",
                    horizontal_alignment="center",
                    spacing=15,
                ),
                padding=40,
                bgcolor=ft.Colors.WHITE,
                expand=True,
            )
            view = ft.View(
                route="/error",
                controls=[error_content],
            )

        # Only after we have the view, we try to update the page. This way we avoid clearing the page if view creation fails.
        try:
            self.page.views.clear()
            time.sleep(0.1)
            self.page.views.append(view)
            self.page.update()
        except Exception as ex:
            logging.exception(f"An error occurred while updating the page: {ex}")
