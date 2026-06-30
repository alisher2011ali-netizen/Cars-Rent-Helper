from typing import Tuple, List, Dict
import base64, uuid, logging

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
            logging.exception(
                "An error occurred while retrieving images for the last added cars."
            )
            images = {car.id: [] for car in last_added_cars}

        return last_added_cars, images

    async def save_image(
        self,
        *,
        image_path: str,
        object_id: int,
        object_type: str,
        category: str = "car_photo",
    ) -> str:
        try:
            unique_number = uuid.uuid4().hex[:8]
            if object_type == "car":
                new_path = f"data/images/cars/{object_id}_{unique_number}.jpg"
            elif object_type == "tenant":
                match category:
                    case "avatar":
                        new_path = f"data/images/tenants/avatars/{object_id}_{unique_number}.jpg"
                    case "passport":
                        new_path = f"data/images/tenants/passports/{object_id}_{unique_number}.jpg"
                    case "sub_passport":
                        new_path = f"data/images/tenants/sub_passports/{object_id}_{unique_number}.jpg"
                    case "driver_license":
                        new_path = f"data/images/tenants/driver_licenses/{object_id}_{unique_number}.jpg"

            self.file_manager.copy_file(image_path, new_path)
            self.db_manager.save_image_path(
                object_type=object_type,
                object_id=object_id,
                category=category,
                image_path=image_path,
            )
            return image_path
        except Exception as ex:
            logging.exception(
                f"An error occurred while saving the image for {object_type} {object_id}."
            )
            return ""
