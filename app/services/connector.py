from typing import Tuple, List, Dict
import base64

from app.database.models import Car
from app.database.manager import DatabaseManager
from app.services.file_manager import FileManager


class Connector:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.file_manager = FileManager()

    def get_last_added_cars(self) -> Tuple[List[Car], Dict[int, List[str]]]:
        last_added_cars = self.db_manager.get_last_added_cars()
        if not last_added_cars:
            return [], {}
        try:
            images = {}
            for car in last_added_cars:
                images[car.id] = []

                if not car.images:
                    continue

                for car_image in car.images:
                    with open(car_image.image_path, "rb") as f:
                        image_bytes = f.read()
                        images[car.id].append(
                            base64.b64encode(image_bytes).decode("utf-8")
                        )
        except Exception as ex:
            print(f"❌ Ошибка при загрузке изображений автомобилей:")
            print(ex)
            images = {car.id: [] for car in last_added_cars}

        return last_added_cars, images
