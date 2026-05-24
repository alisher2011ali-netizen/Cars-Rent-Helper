#!/usr/bin/env python3
"""
Диагностический скрипт для проверки компонентов приложения
"""

import sys
import traceback

print("=" * 60)
print("🔍 ДИАГНОСТИКА ПРИЛОЖЕНИЯ CARS-RENT-HELPER")
print("=" * 60)

# 1. Проверка импортов
print("\n[1/5] Проверка импортов...")
try:
    from flet import Page, View, Text

    print("✅ flet импортирован")
except ImportError as e:
    print(f"❌ Ошибка импорта flet: {e}")
    sys.exit(1)

try:
    from app.database.models import init_db, Car

    print("✅ database.models импортирован")
except ImportError as e:
    print(f"❌ Ошибка импорта database.models: {e}")
    traceback.print_exc()
    sys.exit(1)

# 2. Проверка БД
print("\n[2/5] Проверка базы данных...")
try:
    init_db()
    print("✅ База данных инициализирована")
except Exception as e:
    print(f"❌ Ошибка инициализации БД: {e}")
    traceback.print_exc()
    sys.exit(1)

# 3. Проверка DatabaseManager
print("\n[3/5] Проверка DatabaseManager...")
try:
    from app.database.manager import DatabaseManager

    db_manager = DatabaseManager()
    print("✅ DatabaseManager создан")

    cars = db_manager.get_last_added_cars()
    print(f"✅ Получено {len(cars)} автомобилей из БД")
    if cars:
        car = cars[0]
        print(f"   Первый автомобиль: {car.brand} {car.model}")
        print(f"   Количество изображений: {len(car.images) if car.images else 0}")
except Exception as e:
    print(f"❌ Ошибка с DatabaseManager: {e}")
    traceback.print_exc()
    sys.exit(1)

# 4. Проверка Connector
print("\n[4/5] Проверка Connector...")
try:
    from app.services.connector import Connector

    connector = Connector()
    print("✅ Connector создан")

    last_cars, images = connector.get_last_added_cars()
    print(f"✅ Получено {len(last_cars)} автомобилей")
    print(f"✅ Словарь изображений: {list(images.keys())}")

    for car_id, img_list in images.items():
        print(f"   Car {car_id}: {len(img_list)} изображений")
        if img_list and len(img_list) > 0:
            print(f"      Первое изображение: {len(img_list[0])} символов base64")
except Exception as e:
    print(f"❌ Ошибка с Connector: {e}")
    traceback.print_exc()
    sys.exit(1)

# 5. Проверка Builder (без Flet page)
print("\n[5/5] Проверка Builder...")
try:
    from app.ui.builder import Builder

    print("✅ Builder импортирован")
    print("⚠️  Полная проверка Builder требует Flet Page объекта")
except Exception as e:
    print(f"❌ Ошибка с Builder: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ!")
print("=" * 60)
print("\nЕсли приложение всё ещё не работает, попробуйте:")
print("1. Запустить с флагом: python -m app.main --web")
print("2. Проверить, открывается ли приложение на http://localhost:8550")
