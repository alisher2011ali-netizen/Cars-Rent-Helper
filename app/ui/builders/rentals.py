from flet import (
    View,
    Container,
    Column,
    Text,
    Icon,
    Icons,
    Alignment,
    Colors,
    AppBar,
    FloatingActionButtonLocation,
)

from app.ui.builders.base import Builder


class RentalBuilder(Builder):
    def build_rentals_view(self) -> View:
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
