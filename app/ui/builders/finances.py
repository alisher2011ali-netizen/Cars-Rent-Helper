import flet as ft

from app.ui.builders.base import Builder


class FinanceBuilder(Builder):
    def build_finances_view(self) -> ft.View:
        payments_list = self.db_manager.get_all_payments()
        fab = self._build_fab("/add_payment", self.localization.add_operation)

        if not payments_list:
            empty_message = self._build_not_data_container(
                ft.Icon(
                    ft.Icons.ATTACH_MONEY,
                    size=60,
                    color=ft.Colors.GREY_400,
                    align=ft.Alignment.CENTER,
                ),
                self.localization.no_operations_history,
                self.localization.add_operation,
                "/add_payment",
            )
            return ft.View(
                route="/finances",
                navigation_bar=self._get_nav_bar(4),
                controls=[
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.AppBar(
                                    title=ft.Text(
                                        f"💰 {self.localization.finances}",
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

        payments_content = ft.Container(
            content=ft.Column([], spacing=20),
            padding=40,
            bgcolor=ft.Colors.WHITE,
            expand=True,
        )

        for payment in payments_list:
            payment_type = (
                self.localization.income if payment.type else self.localization.expense
            )
            text_color = ft.Colors.GREEN_500 if payment.type else ft.Colors.RED_500
            payment_card = ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            ft.Text(f"{self.localization.type}:", size=14),
                            ft.Text(payment_type, size=14, color=text_color),
                        ),
                        ft.Text(
                            f"{self.localization.amount}: {payment.amount} руб.",
                            size=14,
                        ),
                        ft.Text(
                            f"{self.localization.comment}: {payment.comment}",
                            size=12,
                            color=ft.Colors.GREY_700,
                        ),
                    ]
                )
            )
            payments_content.content.controls.append(payment_card)

        return ft.View(
            route="/finances",
            navigation_bar=self._get_nav_bar(4),
            controls=[payments_content],
            floating_action_button=fab,
            floating_action_button_location=ft.FloatingActionButtonLocation.END_FLOAT,
        )

    def build_add_payment_view(self) -> ft.View:
        def save_payment(e):
            payment_type = (
                True if type_dropdown.value == self.localization.income else False
            )
            self.db_manager.add_payment(
                amount=amount_input.value,
                comment=comment_input.value,
                type=payment_type,
            )

            self._build_complete_snack_bar()
            self.page.go("/finances")

        amount_input = ft.TextField(label=self.localization.amount, width=300)
        comment_input = ft.TextField(label=self.localization.comment, width=300)
        type_dropdown = ft.Dropdown(
            options=[
                ft.DropdownOption(key="income", text=self.localization.income),
                ft.DropdownOption(key="expense", text=self.localization.expense),
            ],
            value="income",
            width=200,
        )
        save_button = ft.ElevatedButton(
            self.localization.save,
            icon=ft.Icons.SAVE,
            on_click=save_payment,
        )

        content = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        f"💰 {self.localization.new_operation}",
                        size=24,
                        weight="bold",
                    ),
                    amount_input,
                    comment_input,
                    type_dropdown,
                    save_button,
                ],
            ),
            padding=40,
        )
        return ft.View(
            route="/add_payment",
            navigation_bar=self._get_nav_bar(4),
            controls=[ft.Container(content=content, alignment=ft.Alignment.CENTER)],
        )
