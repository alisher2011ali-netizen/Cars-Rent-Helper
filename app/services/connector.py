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
        images = {}
        for car in last_added_cars:
            images[car.id] = []
            try:
                if car.images and len(car.images) > 0:
                    for car_image in car.images:
                        try:
                            with open(car_image.image_path, "rb") as f:
                                image_bytes = f.read()
                                images[car.id].append(
                                    base64.b64encode(image_bytes).decode("utf-8")
                                )
                        except FileNotFoundError:
                            print(
                                f"Ошибка: Файл изображения {car_image.image_path} не найден"
                            )
                        except Exception as ex:
                            print(f"Ошибка при чтении {car_image.image_path}: {ex}")
                else:
                    print(f"Предупреждение: У автомобиля {car.id} нет изображений")
            except Exception as ex:
                print(f"Ошибка при обработке изображений для автомобиля {car.id}: {ex}")
        return last_added_cars, images
