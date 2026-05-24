from flet import (
    Page,
    View,
    Container,
    Column,
    Row,
    Text,
    TextField,
    ElevatedButton,
    TextButton,
    Image,
    GestureDetector,
    Icon,
    Icons,
    NavigationBar,
    NavigationBarDestination,
    Padding,
    Colors,
    AppBar,
    Alignment,
)

from app.database.manager import DatabaseManager
from app.services.connector import Connector


class Builder:
    def __init__(self, page: Page):
        self.page = page
        self.db_manager = DatabaseManager()
        self.connector = Connector()
        self.current_image_indices = (
            {}
        )  # Отслеживаем текущее изображение для каждой машины

    def go_to_home(self, e):
        self.page.go("/")

    def go_to_cars(self, e):
        self.page.go("/cars")

    def go_to_rentals(self, e):
        self.page.go("/rentals")

    def go_to_tenants(self, e):
        self.page.go("/tenants")

    def _get_nav_bar(self, current_index: int):
        return NavigationBar(
            destinations=[
                NavigationBarDestination(icon=Icons.HOME, label="Главная"),
                NavigationBarDestination(icon=Icons.CAR_RENTAL, label="Автомобили"),
                NavigationBarDestination(icon=Icons.PERSON, label="Водители"),
                NavigationBarDestination(icon=Icons.KEY, label="Аренды"),
                NavigationBarDestination(
                    icon=Icons.ATTACH_MONEY_OUTLINED, label="Финансы"
                ),
            ],
            selected_index=current_index,
            on_change=lambda e: self._handle_nav_change(e.control.selected_index),
        )

    def _handle_nav_change(self, index):
        match index:
            case 0:
                self.page.go("/")
            case 1:
                self.page.go("/cars")
            case 2:
                self.page.go("/tenants")
            case 3:
                self.page.go("/rentals")
            case 4:
                self.page.go("/finances")

    def _create_car_card(self, car, car_images):
        """Create a card for a car with swipeable images"""
        car_id = car.id
        self.current_image_indices[car_id] = 0

        image_container = Container(
            content=Image(src_base64=car_images[0]),
            width=300,
            height=200,
        )

        def on_pan_update(e):
            """Handle swipe gesture"""
            if e.delta_x > 50:  # Swipe right
                self._prev_image(car_id, car_images, image_container)
            elif e.delta_x < -50:  # Swipe left
                self._next_image(car_id, car_images, image_container)

        image_with_swipe = GestureDetector(
            content=image_container,
            on_pan_update=on_pan_update,
        )

        # Indicator for current image
        indicator = Text(
            f"1/{len(car_images)}",
            size=12,
            weight="bold",
            color=Colors.BLUE_700,
        )

        card = Container(
            content=Column(
                [
                    Text(
                        f"{car.brand} {car.model} ({car.year})", size=14, weight="bold"
                    ),
                    image_with_swipe,
                    indicator,
                ],
                alignment=Alignment.CENTER,
                horizontal_alignment=Alignment.CENTER,
                spacing=10,
            ),
            padding=15,
            border_radius=12,
            bgcolor=Colors.GREY_100,
            shadow=True,
        )

        # Save references for updating
        card.image_container = image_container
        card.indicator = indicator
        card.car_images = car_images

        return card

    def _next_image(self, car_id, images, image_container):
        """Переключить на следующее изображение"""
        current = self.current_image_indices[car_id]
        if current < len(images) - 1:
            self.current_image_indices[car_id] += 1
            image_container.content = Image(
                src_base64=images[self.current_image_indices[car_id]]
            )
            image_container.update()

    def _prev_image(self, car_id, images, image_container):
        """Переключить на предыдущее изображение"""
        current = self.current_image_indices[car_id]
        if current > 0:
            self.current_image_indices[car_id] -= 1
            image_container.content = Image(
                src_base64=images[self.current_image_indices[car_id]]
            )
            image_container.update()

    def build_home_view(self) -> View:
        print("🏠 Построение home_view...")
        print("📊 Получение последних добавленных автомобилей...")
        last_added_cars, images_dict = self.connector.get_last_added_cars()
        print(f"✅ Получено {len(last_added_cars)} автомобилей")
        print(f"📸 Словарь изображений: {list(images_dict.keys())}")

        # Заголовок
        title = Text(
            "🚘 Cars Rent Helper",
            size=28,
            weight="bold",
            color=Colors.BLUE_700,
        )

        if not last_added_cars:
            empty_message = Container(
                content=Column(
                    [
                        Icon(
                            Icons.DIRECTIONS_CAR,
                            size=60,
                            color=Colors.GREY_400,
                            align=Alignment.CENTER,
                        ),
                        Text(
                            "Нет добавленных автомобилей",
                            size=18,
                            weight="bold",
                            color=Colors.BLACK_87,
                            align=Alignment.CENTER,
                        ),
                        TextButton(
                            "Добавить автомобиль",
                            icon=Icons.ADD,
                            on_click=lambda _: self.page.go("/add-car"),
                            align=Alignment.CENTER,
                        ),
                    ],
                    alignment=Alignment.CENTER,
                    horizontal_alignment=Alignment.CENTER,
                    spacing=20,
                ),
                padding=40,
                alignment=Alignment.CENTER,
            )

            content = Column(
                [
                    title,
                    empty_message,
                ],
                alignment=Alignment.TOP_CENTER,
                horizontal_alignment=Alignment.CENTER,
                spacing=20,
            )

            return View(
                route="/",
                navigation_bar=self._get_nav_bar(0),
                controls=[
                    Container(
                        content=content,
                        padding=20,
                        bgcolor=Colors.WHITE,
                        width=self.page.width,
                        height=self.page.height - 80,
                    )
                ],
            )

        # Если есть машины - показываем их
        cars_column = Column(
            alignment=Alignment.CENTER,
            horizontal_alignment=Alignment.CENTER,
            spacing=20,
        )

        for car in last_added_cars:
            print(f"🚗 Обработка автомобиля: {car.brand} {car.model} (ID: {car.id})")
            car_images = images_dict.get(car.id, [])
            print(f"   Количество изображений: {len(car_images)}")
            if car_images:
                print(f"   ✅ Добавляю карточку")
                card = self._create_car_card(car, car_images)
                cars_column.controls.append(card)
            else:
                print(f"   ⚠️ Нет изображений для этого автомобиля")

        subtitle = Text(
            "Последние добавленные автомобили",
            size=16,
            weight="w500",
            color=Colors.GREY_800,
        )

        content = Column(
            [
                title,
                subtitle,
                cars_column,
            ],
            alignment="start",
            horizontal_alignment=Alignment.CENTER,
            spacing=15,
        )

        print("✅ home_view построен успешно")
        return View(
            route="/",
            navigation_bar=self._get_nav_bar(0),
            controls=[
                Container(
                    content=content,
                    padding=20,
                    bgcolor=Colors.WHITE,
                    width=self.page.window_width,
                    height=self.page.window_height - 80,
                )
            ],
        )

    def build_cars_view(self) -> View:

        cars_list = self.db_manager.get_all_cars()
        if not cars_list:
            return View(
                navigation_bar=self._get_nav_bar(1),
                controls=[
                    Container(
                        content=Column(
                            [
                                AppBar(
                                    title=Text("🚗 Автомобили", size=24, weight="bold")
                                ),
                                Text(
                                    "⚠ Нет добавленных автомобилей",
                                    size=16,
                                    color=Colors.GREY_700,
                                    align=Alignment.CENTER,
                                ),
                                ElevatedButton(
                                    "Добавить новый автомобиль",
                                    icon=Icons.ADD,
                                    on_click=lambda e: self.page.go("/add_car"),
                                    align=Alignment.CENTER,
                                ),
                            ]
                        ),
                        alignment=Alignment.CENTER,
                    )
                ],
            )

        content = Container(
            padding=40,
            bgcolor=Colors.WHITE,
            expand=True,
        )

        for car in cars_list:
            car_images = [img.image_path for img in car.images]
            card = self._create_car_card(car, car_images)
            content.content.append(card)

        return View(
            route="/cars", navigation_bar=self._get_nav_bar(1), controls=[content]
        )
