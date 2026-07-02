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
