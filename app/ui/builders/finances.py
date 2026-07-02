from flet import (
    View,
    Container,
    Column,
    Text,
    TextField,
    Dropdown,
    DropdownOption,
    Icon,
    Icons,
    Alignment,
    Colors,
    AppBar,
    Row,
    FloatingActionButtonLocation,
    ElevatedButton,
)

from app.ui.builders.base import Builder


class FinanceBuilder(Builder):
    def build_finances_view(self) -> View:
        payments_list = self.db_manager.get_all_payments()
        fab = self._build_fab("/add_payment", self.localization.add_operation)

        if not payments_list:
            empty_message = self._build_not_data_container(
                Icon(
                    Icons.ATTACH_MONEY,
                    size=60,
                    color=Colors.GREY_400,
                    align=Alignment.CENTER,
                ),
                self.localization.no_operations_history,
                self.localization.add_operation,
                "/add_payment",
            )
            return View(
                route="/finances",
                navigation_bar=self._get_nav_bar(4),
                controls=[
                    Container(
                        content=Column(
                            [
                                AppBar(
                                    title=Text(
                                        f"💰 {self.localization.finances}",
                                        size=24,
                                        weight="bold",
                                    )
                                ),
                                empty_message,
                            ]
                        ),
                        alignment=Alignment.CENTER,
                    )
                ],
                floating_action_button=fab,
                floating_action_button_location=FloatingActionButtonLocation.END_FLOAT,
            )

        payments_content = Container(
            content=Column([], spacing=20),
            padding=40,
            bgcolor=Colors.WHITE,
            expand=True,
        )

        for payment in payments_list:
            payment_type = (
                self.localization.income if payment.type else self.localization.expense
            )
            text_color = Colors.GREEN_500 if payment.type else Colors.RED_500
            payment_card = Container(
                content=Column(
                    [
                        Row(
                            Text(f"{self.localization.type}:", size=14),
                            Text(payment_type, size=14, color=text_color),
                        ),
                        Text(
                            f"{self.localization.amount}: {payment.amount} руб.",
                            size=14,
                        ),
                        Text(
                            f"{self.localization.comment}: {payment.comment}",
                            size=12,
                            color=Colors.GREY_700,
                        ),
                    ]
                )
            )
            payments_content.content.controls.append(payment_card)

        return View(
            route="/finances",
            navigation_bar=self._get_nav_bar(4),
            controls=[payments_content],
            floating_action_button=fab,
            floating_action_button_location=FloatingActionButtonLocation.END_FLOAT,
        )

    def build_add_payment_view(self) -> View:
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

        amount_input = TextField(label=self.localization.amount, width=300)
        comment_input = TextField(label=self.localization.comment, width=300)
        type_dropdown = Dropdown(
            options=[
                DropdownOption(key="income", text=self.localization.income),
                DropdownOption(key="expense", text=self.localization.expense),
            ],
            value="income",
            width=200,
        )
        save_button = ElevatedButton(
            self.localization.save,
            icon=Icons.SAVE,
            on_click=save_payment,
        )

        content = Container(
            content=Column(
                [
                    Text(
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
        return View(
            route="/add_payment",
            navigation_bar=self._get_nav_bar(4),
            controls=[Container(content=content, alignment=Alignment.CENTER)],
        )
