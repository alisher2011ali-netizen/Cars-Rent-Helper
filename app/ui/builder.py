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
    IconButton,
    Icons,
    NavigationBar,
    NavigationBarDestination,
    Padding,
    Colors,
    AppBar,
    Alignment,
    FloatingActionButton,
    FloatingActionButtonLocation,
    SnackBar,
    SnackBarAction,
    Duration,
    Tooltip,
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
                NavigationBarDestination(icon=Icons.CAR_RENTAL, label="Машины"),
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

    def _create_car_card(self, car, car_images=None):
        """Create a card for a car with swipeable images"""
        car_id = car.id
        car_images = car_images or []
        self.current_image_indices[car_id] = 0

        has_images = bool(car_images)

        if has_images:
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
            indicator = Text(
                f"1/{len(car_images)}",
                size=12,
                weight="bold",
                color=Colors.BLUE_700,
            )
        else:
            image_container = Container(
                content=Text(
                    "Нет изображения",
                    size=14,
                    weight="bold",
                    color=Colors.GREY_700,
                ),
                bgcolor=Colors.GREY_200,
            )
            image_with_swipe = image_container
            indicator = Text(
                "Нет изображения",
                size=12,
                weight="bold",
                color=Colors.GREY_700,
            )

        card = Container(
            content=Column(
                [
                    Text(
                        f"{car.brand} {car.model} ({car.plate_number})",
                        size=14,
                        weight="bold",
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
        )

        card.image_container = image_container
        card.indicator = indicator
        card.car_images = car_images

        return card

    def _next_image(self, car_id, images, image_container):
        """Переключить на следующее изображение"""
        if not images:
            return
        if car_id not in self.current_image_indices:
            self.current_image_indices[car_id] = 0

        current = self.current_image_indices[car_id]
        if current < len(images) - 1:
            self.current_image_indices[car_id] += 1
            image_container.content = Image(
                src_base64=images[self.current_image_indices[car_id]]
            )
            image_container.update()

    def _prev_image(self, car_id, images, image_container):
        """Переключить на предыдущее изображение"""
        if not images:
            return
        if car_id not in self.current_image_indices:
            self.current_image_indices[car_id] = 0

        current = self.current_image_indices[car_id]
        if current > 0:
            self.current_image_indices[car_id] -= 1
            image_container.content = Image(
                src_base64=images[self.current_image_indices[car_id]]
            )
            image_container.update()

    @staticmethod
    def _build_complete_snack_bar(object: str) -> SnackBar:
        return SnackBar(
            content=Text(f"Новый {object} успешно добавлен!"),
            action=SnackBarAction(label="ОК"),
            duration=Duration(seconds=5),
        )

    def _build_not_data_container(
        self, icon: Icon, text: str, button_text: str, route: str
    ) -> Container:
        return Container(
            content=Column(
                [
                    icon,
                    Text(
                        text,
                        size=18,
                        weight="bold",
                        color=Colors.BLACK_87,
                        align=Alignment.CENTER,
                    ),
                    TextButton(
                        button_text,
                        icon=Icons.ADD,
                        on_click=lambda _: self.page.go(route),
                        align=Alignment.CENTER,
                    ),
                ],
            ),
            padding=40,
            alignment=Alignment.CENTER,
        )

    def _build_fab(self, route: str, text: str) -> FloatingActionButton:
        return FloatingActionButton(
            icon=Icons.ADD,
            on_click=lambda e: self.page.go(route),
            tooltip=Tooltip(text),
        )

    def build_home_view(self) -> View:
        last_added_cars, images_dict = self.connector.get_last_added_cars()

        title = Text(
            "🚗 Cars Rent Helper",
            size=28,
            weight="bold",
            color=Colors.BLUE_700,
        )

        if not last_added_cars:
            message = Container(
                content=Column(
                    [
                        Icon(
                            Icons.HOME_FILLED,
                            size=60,
                            color=Colors.GREY_400,
                            align=Alignment.CENTER,
                        ),
                        Text(
                            """Здесь пока пусто.
Начните пользоваться приложением и эта страница заполнится.""",
                            size=18,
                            width=400,
                            align=Alignment.CENTER,
                        ),
                    ],
                    align=Alignment.CENTER,
                    spacing=5,
                )
            )

            content = Column(
                [
                    title,
                    message,
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

        cars_column = Column(
            alignment=Alignment.CENTER,
            horizontal_alignment=Alignment.CENTER,
            spacing=20,
        )

        for car in last_added_cars:
            car_images = images_dict.get(car.id, [])
            if car_images:
                card = self._create_car_card(car, car_images)
                cars_column.controls.append(card)

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

    def build_cars_view(self) -> View:
        cars_list = self.db_manager.get_all_cars()
        fab = self._build_fab("/add_car", "Добавить автомобиль")

        if not cars_list:
            empty_message = self._build_not_data_container(
                Icon(
                    Icons.DIRECTIONS_CAR,
                    size=60,
                    color=Colors.GREY_400,
                    align=Alignment.CENTER,
                ),
                "⚠ Нет добавленных автомобилей",
                "Добавить автомобиль",
                "/add_car",
            )
            return View(
                route="/cars",
                navigation_bar=self._get_nav_bar(1),
                controls=[
                    Container(
                        content=Column(
                            [
                                AppBar(
                                    title=Text("🚗 Автомобили", size=24, weight="bold")
                                ),
                                empty_message,
                            ]
                        ),
                        alignment=Alignment.CENTER,
                    )
                ],
                floating_action_button=fab,
                floating_action_button_location=FloatingActionButtonLocation.END_FLOAT,
            )

        cars_column = Column(
            spacing=20,
            horizontal_alignment=Alignment.CENTER,
            alignment=Alignment.CENTER,
        )

        for car in cars_list:
            car_images = [img.image_path for img in car.images]
            card = self._create_car_card(car, car_images)
            cars_column.controls.append(card)

        content = Column(
            [
                Text("🚗 Автомобили", size=24, weight="bold"),
                cars_column,
            ],
            spacing=20,
            padding=40,
            horizontal_alignment=Alignment.CENTER,
        )

        cars_content = Container(
            content=content,
            width=self.page.width,
            height=self.page.height,
            expand=True,
        )

        return View(
            route="/cars",
            navigation_bar=self._get_nav_bar(1),
            controls=[cars_content],
            floating_action_button=fab,
            floating_action_button_location=FloatingActionButtonLocation.END_FLOAT,
        )

    def build_tenants_view(self) -> View:
        tenants_list = self.db_manager.get_all_tenants()
        fab = self._build_fab("/add_tenant", "Добавить водителя")

        if not tenants_list:
            empty_message = self._build_not_data_container(
                Icon(
                    Icons.PERSON, size=60, color=Colors.GREY_400, align=Alignment.CENTER
                ),
                "⚠ Нет добавленных водителей",
                "Добавить водителя",
                "/add_tenant",
            )
            return View(
                route="/tenants",
                navigation_bar=self._get_nav_bar(2),
                controls=[
                    Container(
                        content=Column(
                            [
                                AppBar(
                                    title=Text("👤 Водители", size=24, weight="bold")
                                ),
                                empty_message,
                            ]
                        ),
                        alignment=Alignment.CENTER,
                    )
                ],
                floating_action_button=fab,
                floating_action_button_location=FloatingActionButtonLocation.END_FLOAT,
            )

        tenants_content = Container(
            content=Column([], spacing=20),
            padding=40,
            bgcolor=Colors.WHITE,
            expand=True,
        )

        for tenant in tenants_list:
            tenant_card = Container(
                content=Column(
                    [
                        Text(f"{tenant.fullname}", size=14, weight="bold"),
                        Text(f"Телефон: {tenant.phone_number}", size=12),
                        TextButton(
                            "Подробнее",
                            on_click=lambda e: self.page.go(f"/details_{tenant.id}"),
                        ),
                    ],
                    spacing=5,
                ),
                padding=15,
                border_radius=12,
                bgcolor=Colors.GREY_100,
                shadow=True,
            )
            tenants_content.content.controls.append(tenant_card)

        return View(
            route="/tenants",
            navigation_bar=self._get_nav_bar(2),
            controls=[tenants_content],
            floating_action_button=fab,
            floating_action_button_location=FloatingActionButtonLocation.END_FLOAT,
        )

    def build_rentals_view(self):
        rentals_list = self.db_manager.get_all_rentals()
        fab = self._build_fab("/add_rental", "Добавить аренду")

        if not rentals_list:
            empty_message = self._build_not_data_container(
                Icon(
                    Icons.KEY,
                    size=60,
                    color=Colors.GREY_400,
                    align=Alignment.CENTER,
                ),
                "⚠ Нет истории аренды машин",
                "Добавить аренду",
                "/add_rental",
            )
            return View(
                route="/tenants",
                navigation_bar=self._get_nav_bar(3),
                controls=[
                    Container(
                        content=Column(
                            [
                                AppBar(title=Text("📋 Аренды", size=24, weight="bold")),
                                empty_message,
                            ]
                        ),
                        alignment=Alignment.CENTER,
                    )
                ],
                floating_action_button=fab,
                floating_action_button_location=FloatingActionButtonLocation.END_FLOAT,
            )

        rentals_content = Container(
            content=Column([], spacing=20),
            padding=40,
            bgcolor=Colors.WHITE,
            expand=True,
        )

        for rental in rentals_list:
            match rental.status:
                case "active":
                    status_text = "Активно"
                    status_color = Colors.GREEN_500
                case "completed":
                    status_text = "Завершено"
                    status_color = Colors.BLACK_87
                case "cancelled":
                    status_text = "Отменено"
                    status_color = Colors.RED_500

            rental_card = Container(
                content=Column(
                    [
                        Text(
                            f"Статус: {status_text}",
                            size=16,
                            color=status_color,
                            weight="bold",
                        ),
                        Text(
                            f"Машина: {rental.car.brand} {rental.car.model} ({rental.car.plate_number})",
                            size=14,
                        ),
                        Text(
                            f"Водитель: {rental.tenant.fullname} ({rental.tenant.phone_number})",
                            size=14,
                        ),
                        Text(f"Доход в сумме: {rental.total_cost} руб."),
                        Text(f"Начало: {rental.start_date}", size=14),
                        Text(f"Конец: {rental.end_date}", size=14),
                    ],
                    spacing=5,
                ),
                padding=15,
                border_radius=12,
                bgcolor=Colors.GREY_100,
                shadow=True,
            )
            rentals_content.content.controls.append(rental_card)

        return View(
            route="/rentals",
            navigation_bar=self._get_nav_bar(3),
            controls=[rentals_content],
            floating_action_button=fab,
            floating_action_button_location=FloatingActionButtonLocation.END_FLOAT,
        )

    def build_finances_view(self):
        payments_list = self.db_manager.get_all_payments()
        fab = self._build_fab("/add_payment", "Добавить операцию")

        if not payments_list:
            empty_message = self._build_not_data_container(
                Icon(
                    Icons.ATTACH_MONEY,
                    size=60,
                    color=Colors.GREY_400,
                    align=Alignment.CENTER,
                ),
                "⚠ Нет истории доходов/расходов",
                "Добавить операцию",
                "/add_payment",
            )
            return View(
                route="/finances",
                navigation_bar=self._get_nav_bar(4),
                controls=[
                    Container(
                        content=Column(
                            [
                                AppBar(
                                    title=Text("💰 Финансы", size=24, weight="bold")
                                ),
                                empty_message,
                            ]
                        ),
                        alignment=Alignment.CENTER,
                    )
                ],
                floating_action_button=fab,
                floating_action_button_location=FloatingActionButtonLocation.END_FLOAT,
            )

        payments_content = Container(
            content=Column([], spacing=20),
            padding=40,
            bgcolor=Colors.WHITE,
            expand=True,
        )

        for payment in payments_list:
            payment_type = "Доход" if payment.type else "Расход"
            text_color = Colors.GREEN_500 if payment.type else Colors.RED_500
            payment_card = Container(
                content=Column(
                    [
                        Row(
                            Text(f"Тип:", size=14),
                            Text(f"{payment_type}", size=14, color=text_color),
                        ),
                        Text(f"Сумма: {payment.amount} руб.", size=14),
                        Text(
                            f"Комментарий: {payment.comment}",
                            size=12,
                            color=Colors.GREY_700,
                        ),
                    ]
                )
            )
            payments_content.content.controls.append(payment_card)

        return View(
            route="/finances",
            navigation_bar=self._get_nav_bar(4),
            controls=[payments_content],
            floating_action_button=fab,
            floating_action_button_location=FloatingActionButtonLocation.END_FLOAT,
        )

    def build_add_car_view(self):
        def upload_images(e):
            # Логика загрузки изображений для автомобиля
            pass

        def save_car(e):
            self.db_manager.save_new_car(
                brand=brand_input.value,
                model=model_input.value,
                year=year_input.value,
                plate_number=plate_num_input.value,
            )

            self.page.go("/cars")

        brand_input = TextField(label="Марка", width=300)
        model_input = TextField(label="Модель", width=300)
        year_input = TextField(label="Год выпуска", width=300)
        plate_num_input = TextField(label="Гос. номер", width=300)
        input = Container(
            content=Column(
                [
                    Text("Новый автомобиль", size=24, weight="bold"),
                    brand_input,
                    model_input,
                    year_input,
                    plate_num_input,
                    TextButton(
                        "Загрузить изображения",
                        icon=Icons.UPLOAD_FILE,
                        on_click=upload_images,
                    ),
                    ElevatedButton("Сохранить", icon=Icons.SAVE, on_click=save_car),
                    ElevatedButton(
                        "Назад",
                        icon=Icons.ARROW_BACK,
                        on_click=lambda e: self.page.go("/cars"),
                    ),
                ],
                spacing=15,
            ),
            padding=40,
            alignment=Alignment.CENTER,
        )

        return View(
            route="/add_car",
            navigation_bar=self._get_nav_bar(1),
            controls=[input],
        )
