import json
import os


class Localization:
    def __init__(self, default_lang: str = "ru", default_currency: str = "RUB"):
        self.strings = {}
        self.language = default_lang
        self.currency = default_currency
        self.load_lang(default_lang)

    def load_lang(self, lang_code: str):
        """Load localization strings from a JSON file."""
        file_path = os.path.join("assets", "locales", f"{lang_code}.json")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                self.strings = json.load(f)
        else:
            print(
                f"⚠ Localization file for '{lang_code}' not found. Using empty strings."
            )
            self.strings = {}

    def __getattr__(self, key: str):
        """Retrieve a localized string by its key."""
        return self.strings.get(key, key)
