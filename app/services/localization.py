import json
import os


def all_properties(cls):
    for attr_name in list(dir(cls)):
        if not attr_name.startswith("_"):
            attr_value = getattr(cls, attr_name)
            if callable(attr_value):
                setattr(cls, attr_name, property(attr_value))
    return cls


class LocalizationManager:
    def __init__(self, default_lang="ru"):
        self.strings = {}
        self.load_lang(default_lang)

    def load_lang(self, lang_code):
        """Load localization strings from a JSON file."""
        file_path = os.path.join("data", "locales", f"{lang_code}.json")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                self.strings = json.loads(f)
        else:
            print(
                f"⚠ Localization file for '{lang_code}' not found. Using empty strings."
            )
            self.strings = {}

    def _get(self, key):
        """Retrieve a localized string by its key."""
        return self.strings.get(key, key)


@all_properties
class AppStrings(LocalizationManager):
    def __init__(self, default_lang="ru"):
        super().__init__(default_lang)

    def error_initializing(self):
        return self._get("error_initializing")

    def error_loading(self):
        return self._get("error_loading")

    def route(self):
        return self._get("route")

    def error(self):
        return self._get("error")

    def hello_text(self):
        return self._get("hello_text")

    def choose_language(self):
        return self._get("choose_language")

    def add_rental(self):
        return self._get("add_rental")

    def no_rentals_history(self):
        return self._get("no_rentals_history")

    def rentals(self):
        return self._get("rentals")

    def active(self):
        return self._get("active")

    def completed(self):
        return self._get("completed")

    def cancelled(self):
        return self._get("cancelled")

    def status(self):
        return self._get("status")

    def car(self):
        return self._get("car")

    def tenant(self):
        return self._get("tenant")

    def income_in_total(self):
        return self._get("income_in_total")

    def start(self):
        return self._get("start")

    def end(self):
        return self._get("end")

    def add_operation(self):
        return self._get("add_operation")

    def no_operations_history(self):
        return self._get("no_operations_history")

    def finances(self):
        return self._get("finances")

    def income(self):
        return self._get("income")

    def expense(self):
        return self._get("expense")

    def type(self):
        return self._get("type")

    def amount(self):
        return self._get("amount")

    def description(self):
        return self._get("description")

    def add_car(self):
        return self._get("add_car")

    def no_added_cars(self):
        return self._get("no_added_cars")

    def cars(self):
        return self._get("cars")

    def brand(self):
        return self._get("brand")

    def model(self):
        return self._get("model")

    def year_of_production(self):
        return self._get("year")

    def plate_number(self):
        return self._get("plate_number")

    def new_car(self):
        return self._get("new_car")

    def upload_images(self):
        return self._get("upload_images")

    def save(self):
        return self._get("save")

    def back(self):
        return self._get("back")

    def last_added_cars(self):
        return self._get("last_added_cars")

    def main_menu(self):
        return self._get("main_menu")

    def tenants(self):
        return self._get("tenants")

    def no_images(self):
        return self._get("no_images")

    def added_successfully(self):
        return self._get("added_successfully")

    def add_tenant(self):
        return self._get("add_tenant")

    def no_added_tenants(self):
        return self._get("no_tenants")

    def details(self):
        return self._get("details")

    def full_name(self):
        return self._get("full_name")

    def phone_number(self):
        return self._get("phone_number")

    def debt_in_total(self):
        return self._get("debt_in_total")

    def new_tenant(self):
        return self._get("new_tenant")

    def upload_avatar(self):
        return self._get("upload_avatar")

    def upload_passport(self):
        return self._get("upload_passport")

    def upload_subpassport(self):
        return self._get("upload_subpassport")

    def upload_driver_license(self):
        return self._get("upload_driver_license")
