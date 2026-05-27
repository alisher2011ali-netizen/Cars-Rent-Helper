from flet import View, Container, Column, Text, Icon, Icons, Alignment, Colors

from app.ui.builders.base import Builder


class HomeBuilder(Builder):
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
