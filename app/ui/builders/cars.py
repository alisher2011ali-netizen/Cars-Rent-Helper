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
    FilePicker,
    FilePickerFileType,
    FilePickerUploadEvent,
    TextField,
    TextButton,
    ElevatedButton,
    FloatingActionButtonLocation,
)

from app.ui.builders.base import Builder


class CarBuilder(Builder):
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
            car_images = [img.path for img in car.images]
            card = self._create_car_card(car, car_images)
            cars_column.controls.append(card)

        content = Column(
            [
                Text("🚗 Автомобили", size=24, weight="bold"),
                cars_column,
            ],
            spacing=20,
            horizontal_alignment=Alignment.CENTER,
        )

        cars_content = Container(
            content=content,
            padding=20,
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

    def build_add_car_view(self) -> View:
        selected_images_paths = []

        async def _on_file_picker_result(self, e: FilePickerUploadEvent):
            if e.files:
                for file in e.files:
                    if file.path not in selected_images_paths:
                        selected_images_paths.append(file.path)

        file_picker = FilePicker(on_upload=_on_file_picker_result)

        async def pick_image_click(e):
            await file_picker.pick_files(
                allow_multiple=True, file_type=FilePickerFileType.IMAGE
            )

        async def save_car(e=None):
            car_id = self.db_manager.add_car(
                brand=brand_input.value,
                model=model_input.value,
                year=year_input.value,
                plate_number=plate_num_input.value,
            ).id

            for image_path in selected_images_paths:
                await self.connector.save_image(
                    image_path=image_path, object_id=car_id, object_type="car"
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
                        on_click=pick_image_click,
                    ),
                    ElevatedButton(
                        "Сохранить",
                        icon=Icons.SAVE,
                        on_click=save_car,
                    ),
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
