#!/usr/bin/env python3
"""
Простой тест UI - показывает яркий контент на экране
"""
import flet as ft
from flet import Page, View, Text, Container, Column, Colors, ElevatedButton, Row, Icons


def main(page: Page):
    print("=" * 60)
    print("🧪 ТЕСТИРОВАНИЕ UI")
    print("=" * 60)

    page.title = "Cars Rent Helper - TEST"
    page.window_width = 800
    page.window_height = 600

    print("✅ Страница создана")
    print(f"   Размер: {page.window_width}x{page.window_height}")

    # Создаём очень яркий контент
    test_content = Container(
        content=Column(
            [
                Text(
                    "🧪 ТЕСТ UI - ЕСЛИ ВЫ ЭТО ВИДИТЕ, ТО ВСЕ РАБОТАЕТ! 🎉",
                    size=24,
                    weight="bold",
                    color=Colors.WHITE,
                ),
                Text(
                    "Это очень большой и видимый текст",
                    size=20,
                    color=Colors.YELLOW,
                    weight="bold",
                ),
                Text(
                    "Экран должен быть красным",
                    size=16,
                    color=Colors.WHITE,
                ),
                ElevatedButton(
                    "✅ КОНТЕНТ ВИДНА",
                    width=300,
                    height=60,
                ),
            ],
            alignment="center",
            horizontal_alignment="center",
            spacing=30,
        ),
        padding=50,
        bgcolor=Colors.RED_700,  # Яркий красный фон
        expand=True,
    )

    view = View(
        route="/test",
        controls=[test_content],
    )

    print("✅ View создана")
    print("📍 Очистка старых views...")
    page.views.clear()

    print("📍 Добавление нового view...")
    page.views.append(view)

    print("📍 Обновление страницы...")
    page.update()

    print("=" * 60)
    print("✅ ТЕСТОВАЯ СТРАНИЦА ЗАГРУЖЕНА")
    print("=" * 60)
    print("Если вы видите окно с красным фоном и текстом,")
    print("то интерфейс работает правильно!")
    print()


if __name__ == "__main__":
    print("The test app has been setup")
    ft.run(main=main)
