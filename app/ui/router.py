import flet as ft
import logging
import time

from app.ui.builders import (
    Builder,
    HomeBuilder,
    CarBuilder,
    TenantBuilder,
    RentalBuilder,
    FinanceBuilder,
    FirstLaunchBuilder,
)


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
                fisrt_launch_builder = FirstLaunchBuilder(self.page)
                self.builder.db_manager.set_setting("is_first_launch", "true")
                view = fisrt_launch_builder.build_first_launch_view()
                self.page.views.clear()
                self.page.views.append(view)
                self.page.update()
            else:
                home_builder = HomeBuilder(self.page)
                view = home_builder.build_home_view()
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
                    home_builder = HomeBuilder(self.page)
                    view = home_builder.build_home_view()
                case "/first_launch":
                    first_launch_builder = FirstLaunchBuilder(self.page)
                    view = first_launch_builder.build_first_launch_view()
                case "/cars":
                    car_builder = CarBuilder(self.page)
                    view = car_builder.build_cars_view()
                case "/tenants":
                    tenant_builder = TenantBuilder(self.page)
                    view = tenant_builder.build_tenants_view()
                case "/rentals":
                    rental_builder = RentalBuilder(self.page)
                    view = rental_builder.build_rentals_view()
                case "/finances":
                    finance_builder = FinanceBuilder(self.page)
                    view = finance_builder.build_finances_view()
                case "/add_car":
                    car_builder = CarBuilder(self.page)
                    view = car_builder.build_add_car_view()
                case "/add_tenant":
                    tenant_builder = TenantBuilder(self.page)
                    view = tenant_builder.build_add_tenant_view()
                case "/add_rental":
                    rental_builder = RentalBuilder(self.page)
                    view = rental_builder.build_add_rental_view()
                case "/add_payment":
                    finance_builder = FinanceBuilder(self.page)
                    view = finance_builder.build_add_payment_view()
                case _:
                    home_builder = HomeBuilder(self.page)
                    view = home_builder.build_home_view()
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
