from flet import Page, View, Text, Container, Column, Colors, ElevatedButton, Row, Icons
import traceback
import time

from app.ui.builder import Builder


class UIRouter:
    def __init__(self, page: Page):
        self.page = page
        self.builder = Builder(self.page)

    def _set_navigation_bar(self, route_index: int):
        self.page.navigation_bar = self.builder._get_nav_bar(route_index)
        self.page.update()

    def build(self):
        self.page.title = "Cars Rent Helper"

        # Сначала регистрируем обработчик
        self.page.on_route_change = self.route_change

        # Явно фиксируем текущий маршрут и рендерим первую view
        self.page.route = self._set_navigation_bar(0)

        try:
            view = self.home_view()
            self.page.views.clear()
            self.page.views.append(view)
            self.page.update()
        except Exception as ex:
            print(f"❌ Ошибка при загрузке начального экрана:")
            print(traceback.format_exc())
            error_content = Container(
                content=Column(
                    [
                        Text(
                            "❌ ОШИБКА ПРИ ИНИЦИАЛИЗАЦИИ",
                            size=20,
                            weight="bold",
                            color=Colors.RED,
                        ),
                        Text(str(ex), size=14, color=Colors.RED_800),
                    ],
                    alignment="center",
                    horizontal_alignment="center",
                    spacing=20,
                ),
                padding=40,
                bgcolor=Colors.WHITE,
                expand=True,
            )
            error_view = View(route="/", controls=[error_content])
            self.page.views.clear()
            self.page.views.append(error_view)
            self.page.update()

    def route_change(self, e):
        """Обработчик смены экранов.
        :params
        e: RouteChangeEvent"""

        try:
            match e.route:
                case "/":
                    view = self.home_view()
                case "/cars":
                    view = self.cars_view()
                case "/tenants":
                    view = self.tenants_view()
                case "/rentals":
                    view = self.rentals_view()
                case "/finances":
                    view = self.finances_view()
                case "/add_car":
                    view = self.add_car_view()
                case _:
                    view = self.home_view()
        except Exception as ex:
            print(f"❌ Ошибка при сборке экрана {e.route}:")
            print(traceback.format_exc())
            error_content = Container(
                content=Column(
                    [
                        Text(
                            "❌ ОШИБКА ПРИ ЗАГРУЗКЕ",
                            size=20,
                            weight="bold",
                            color=Colors.RED,
                        ),
                        Text(f"Маршрут: {e.route}", size=12, color=Colors.BLACK_87),
                        Text(f"Ошибка: {str(ex)}", size=12, color=Colors.RED_800),
                    ],
                    alignment="center",
                    horizontal_alignment="center",
                    spacing=15,
                ),
                padding=40,
                bgcolor=Colors.WHITE,
                expand=True,
            )
            view = View(
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
            print(f"❌ Ошибка при обновлении страницы: {ex}")
            print(traceback.format_exc())

    def home_view(self):
        return self.builder.build_home_view()

    def cars_view(self):
        return self.builder.build_cars_view()

    def tenants_view(self):
        return self.builder.build_tenants_view()

    def rentals_view(self):
        return self.builder.build_rentals_view()

    def finances_view(self):
        return self.builder.build_finances_view()

    def add_car_view(self):
        return self.builder.build_add_car_view()

    def add_tenant_view(self):
        return self.builder.build_add_tenant_view()

    def add_rental_view(self):
        return self.builder.build_add_rental_view()

    def add_payment_view(self):
        return self.builder.build_add_payment_view()
