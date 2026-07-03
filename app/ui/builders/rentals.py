import flet as ft
from datetime import datetime, timedelta

from app.ui.builders.base import Builder


class RentalBuilder(Builder):
    def build_rentals_view(self) -> ft.View:
        rentals_list = self.db_manager.get_all_rentals()
        fab = self._build_fab("/add_rental", "Добавить аренду")

        if not rentals_list:
            empty_message = self._build_not_data_container(
                ft.Icon(
                    ft.Icons.KEY,
                    size=60,
                    color=ft.Colors.GREY_400,
                    align=ft.Alignment.CENTER,
                ),
                self.localization.no_rentals_history,
                self.localization.add_rental,
                "/add_rental",
            )
            return ft.View(
                route="/tenants",
                navigation_bar=self._get_nav_bar(3),
                controls=[
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.AppBar(
                                    title=ft.Text(
                                        f"📋 {self.localization.rentals}",
                                        size=24,
                                        weight="bold",
                                    )
                                ),
                                empty_message,
                            ]
                        ),
                        alignment=ft.Alignment.CENTER,
                    )
                ],
                floating_action_button=fab,
                floating_action_button_location=ft.FloatingActionButtonLocation.END_FLOAT,
            )

        rentals_content = ft.Container(
            content=ft.Column([], spacing=20),
            padding=40,
            bgcolor=ft.Colors.WHITE,
            expand=True,
        )

        for rental in rentals_list:
            match rental.status:
                case "active":
                    status_text = self.localization.active
                    status_color = ft.Colors.GREEN_500
                case "completed":
                    status_text = self.localization.completed
                    status_color = ft.Colors.BLACK_87
                case "cancelled":
                    status_text = self.localization.cancelled
                    status_color = ft.Colors.RED_500

            rental_card = ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            f"{self.localization.status}: {status_text}",
                            size=16,
                            color=status_color,
                            weight="bold",
                        ),
                        ft.Text(
                            f"{self.localization.car}: {rental.car.brand} {rental.car.model} ({rental.car.plate_number})",
                            size=14,
                        ),
                        ft.Text(
                            f"{self.localization.tenant}: {rental.tenant.last_name} {rental.tenant.first_name} ({rental.tenant.phone_number})",
                            size=14,
                        ),
                        ft.Text(
                            f"{self.localization.income_in_total}: {rental.total_cost} руб."
                        ),
                        ft.Text(
                            f"{self.localization.start}: {rental.start_date}",
                            size=14,
                        ),
                        ft.Text(f"{self.localization.end}: {rental.end_date}", size=14),
                    ],
                    spacing=5,
                ),
                padding=15,
                border_radius=12,
                bgcolor=ft.Colors.GREY_100,
                shadow=True,
            )
            rentals_content.content.controls.append(rental_card)

        return ft.View(
            route="/rentals",
            navigation_bar=self._get_nav_bar(3),
            controls=[rentals_content],
            floating_action_button=fab,
            floating_action_button_location=ft.FloatingActionButtonLocation.END_FLOAT,
        )

    def build_add_rental_view(self) -> ft.View:
        cars = self.db_manager.get_all_cars()
        tenants = self.db_manager.get_all_tenants()

        if not cars or not tenants:
            snack = ft.SnackBar(
                ft.Text(self.localization.no_cars_or_tenants),
                bgcolor=ft.Colors.RED_500,
                open=True,
            )
            self.page.overlay.append(snack)
            return self.build_rentals_view()

        car_options = [
            ft.DropdownOption(
                key=car.id, text=f"{car.brand} {car.model} ({car.plate_number})"
            )
            for car in cars
        ]
        car_dropdown = ft.Dropdown(
            options=car_options,
            value=car_options[0].key if car_options else None,
            width=300,
        )

        tenant_options = [
            ft.DropdownOption(
                key=tenant.id,
                text=f"{tenant.last_name} {tenant.first_name} ({tenant.phone_number})",
            )
            for tenant in tenants
        ]
        tenant_dropdown = ft.Dropdown(
            options=tenant_options,
            width=300,
        )

        selected_car = None
        selected_tenant = None

        dates_info_text = ft.Text("Срок: 7 дней", size=16, weight="bold")
        total_price_text = ft.Text(
            f"{self.localization.total_to_be_paid}: 0 руб.",
            size=20,
            weight="bold",
            color=ft.Colors.GREEN_700,
        )

        price_field = ft.TextField(
            label="Стоимость за неделю",
            value="0",
            keyboard_type=ft.KeyboardType.NUMBER,
            width=400,
            on_change=lambda e: recalculate_total(),
        )

        def handle_date_change(e):
            recalculate_total()

        start_picker = ft.DatePicker(on_change=handle_date_change)
        end_picker = ft.DatePicker(on_change=handle_date_change)

        manual_date_row = ft.Row(
            [
                ft.ElevatedButton(
                    self.localization.start,
                    icon=ft.Icons.CALENDAR_MONTH,
                    on_click=lambda e: start_picker.pick_date(),
                ),
                ft.ElevatedButton(
                    self.localization.end,
                    icon=ft.Icons.CALENDAR_MONTH,
                    on_click=lambda e: end_picker.pick_date(),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            visible=False,
        )

        def recalculate_total():
            tariff = tariff_radio.value
            try:
                entered_price = float(price_field.value or 0)
            except ValueError:
                entered_price = 0

            if tariff == "weekly":
                start_date = datetime.now()
                end_date = start_date + timedelta(days=7)
                days = 7
                total_amount = entered_price
                dates_info_text.value = f"Срок: {days} дней ({start_date.strftime('%d.%m')} - {end_date.strftime('%d.%m')})"

            elif tariff == "monthly":
                start_date = datetime.now()
                end_date = start_date + timedelta(days=30)
                days = 30
                total_amount = entered_price
                dates_info_text.value = f"Срок: 30 дней ({start_date.strftime('%d.%m')} - {end_date.strftime('%d.%m')})"

            elif tariff == "custom":
                manual_date_row.visible = True
                if start_picker.value:
                    start_date = start_picker.value
                if end_picker.value:
                    end_date = end_picker.value

                days = (end_date - start_date).days
                total_amount = entered_price
                dates_info_text.value = f"Срок: {days} дн. ({start_date.strftime('%d.%m')} - {end_date.strftime('%d.%m')})"

            total_price_text.value = (
                f"{self.localization.total_to_be_paid}: {total_amount:.2f} руб."
            )

            dates_info_text.update()
            total_price_text.update()
            manual_date_row.update()

        def on_tariff_change(e):
            tariff = e.control.value
            if tariff == "weekly":
                price_field.label = "Стоимость за неделю"
            elif tariff == "monthly":
                price_field.label = "Стоимость за месяц"
            elif tariff == "custom":
                price_field.label = "Стоимость за выбранный период"

            price_field.update()
            recalculate_total()

        tariff_radio = ft.RadioGroup(
            content=ft.Row(
                [
                    ft.Radio(value="weekly", label=self.localization.weekly),
                    ft.Radio(value="monthly", label=self.localization.monthly),
                    ft.Radio(value="custom", label=self.localization.another_term),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            value="weekly",
            on_change=on_tariff_change,
        )

        def on_click_save(e):
            pass

        save_button = ft.ElevatedButton(
            self.localization.save, icon=ft.Icons.SAVE, on_click=on_click_save
        )

        content = ft.Column(
            [
                ft.Text(
                    f"📋 {self.localization.add_rental}",
                    size=24,
                    weight="bold",
                ),
                car_dropdown,
                tenant_dropdown,
                tariff_radio,
                price_field,
                dates_info_text,
                total_price_text,
                manual_date_row,
                save_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )
        return ft.View(
            route="/add_rental",
            navigation_bar=self._get_nav_bar(3),
            controls=[
                ft.Container(content=content, padding=20, alignment=ft.Alignment.CENTER)
            ],
        )
