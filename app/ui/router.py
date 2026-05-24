from flet import Page, View, Text, Container, Column, Colors, ElevatedButton, Row, Icons
import traceback
from app.ui.builder import Builder


class UIRouter:
    def __init__(self, page: Page):
        self.page = page
        self.builder = Builder(self.page)

    def _set_navigation_bar(self, route_index: int):
        self.page.navigation_bar = self.builder._get_nav_bar(route_index)
        self.page.update()

    def build(self):
        print("🚀 Инициализация UIRouter...")
        self.page.title = "Cars Rent Helper"

        # Сначала регистрируем обработчик
        self.page.on_route_change = self.route_change
        print("📍 Регистрация обработчика маршрутизации...")

        # Явно фиксируем текущий маршрут и рендерим первую view
        self.page.route = "/"
        print(f"📍 Текущий маршрут: {self.page.route}")
        self._set_navigation_bar(0)

        print("🔨 Построение начального экрана (home)...")
        try:
            view = self.home_view()
            self.page.views.clear()
            self.page.views.append(view)
            self.page.update()
            print("✅ Начальный экран загружен успешно")
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
        """Обработчик смены экранов. e — это RouteChangeEvent"""
        print(f"📂 route_change вызван: {e.route}")

        # 1. Сначала Пытаемся создать вьюшку.
        try:
            print(f"🔄 Обработка маршрута: {e.route}")
            match e.route:
                case "/":
                    print("✨ Построение home_view...")
                    self._set_navigation_bar(0)
                    view = self.home_view()
                case "/cars":
                    self._set_navigation_bar(1)
                    view = self.cars_view()
                case "/tenants":
                    self._set_navigation_bar(2)
                    view = self.tenants_view()
                case "/rentals":
                    self._set_navigation_bar(3)
                    view = self.rentals_view()
                case "/finances":
                    self._set_navigation_bar(4)
                    view = self.finances_view()
                case _:
                    print(f"⚠️ Неизвестный маршрут: {e.route}, используем home_view")
                    self._set_navigation_bar(0)
                    view = self.home_view()
            print(f"✅ Вьюшка построена успешно для {e.route}")
        except Exception as ex:
            print(f"❌ Ошибка при сборке экрана {e.route}:")
            print(traceback.format_exc())
            # Показываем ошибку в UI
            error_content = Container(
                content=Column(
                    [
                        Text(
                            "❌ ОШИБКА ПРИ ЗАГРУЗКЕ",
                            size=20,
                            weight="bold",
                            color=Colors.RED,
                        ),
                        Text(f"Маршрут: {e.route}", size=12, color=Colors.BLACK87),
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

        # 2. Только если вьюшка успешно собрана — обновляем экран
        try:
            print("🔄 Обновление страницы...")
            self.page.views.clear()
            self.page.views.append(view)
            self.page.update()
            print("✅ Страница обновлена")
        except Exception as ex:
            print(f"❌ Ошибка при обновлении страницы: {ex}")
            print(traceback.format_exc())

    def home_view(self):
        return self.builder.build_home_view()

    # Добавляем недостающие методы-заглушки, чтобы роутер не падал
    def _create_placeholder_view(self, route: str, title: str, nav_index: int):
        """Создаёт красивую view-заглушку"""
        content = Container(
            content=Column(
                [
                    Text(
                        title,
                        size=24,
                        weight="bold",
                        color=Colors.BLUE_700,
                    ),
                    Text(
                        "В разработке",
                        size=16,
                        color=Colors.ORANGE_700,
                        weight="w500",
                    ),
                ],
                alignment="center",
                horizontal_alignment="center",
                spacing=20,
            ),
            padding=40,
            bgcolor=Colors.WHITE,
            expand=True,
        )

        return View(
            route=route,
            controls=[content],
        )

    def cars_view(self):
        """Экран автомобилей с большим видимым контентом для теста"""
        print("🚗 Загрузка экрана /cars")
        return self.builder.build_cars_view()

    def tenants_view(self):
        return self._create_placeholder_view("/tenants", "👥 Водители", 2)

    def rentals_view(self):
        return self._create_placeholder_view("/rentals", "📋 Аренды", 3)

    def finances_view(self):
        return self._create_placeholder_view("/finances", "💰 Финансы", 4)
