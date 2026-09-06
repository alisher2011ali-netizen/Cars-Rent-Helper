import json
import os


class Localization:
    def __init__(
        self, default_lang: str | None = None, default_currency: str | None = None
    ):
        self.strings = {}
        self.language = default_lang or "ru"
        self.currency = default_currency or "RUB"
        self.load_lang(self.language)

    def load_lang(self, lang_code: str):
        """Load localization strings from a JSON file."""
        current_dir = os.path.dirname(os.path.abspath(__file__))

        file_path = os.path.join(
            current_dir, "..", "assets", "locales", f"{lang_code}.json"
        )

        print(f"DEBUG: Ищу файл перевода по пути: {file_path}")

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


localization = Localization()
