from flet import (
    View,
    Container,
    Column,
    Text,
    Icon,
    Icons,
    Alignment,
    Colors,
    AppBar,
    TextButton,
    FloatingActionButtonLocation,
)

from app.ui.builders.base import Builder


class TenantBuilder(Builder):
    def build_tenants_view(self) -> View:
        tenants_list = self.db_manager.get_all_tenants()
        fab = self._build_fab("/add_tenant", "Добавить водителя")

        if not tenants_list:
            empty_message = self._build_not_data_container(
                Icon(
                    Icons.PERSON, size=60, color=Colors.GREY_400, align=Alignment.CENTER
                ),
                "⚠ Нет добавленных водителей",
                "Добавить водителя",
                "/add_tenant",
            )
            return View(
                route="/tenants",
                navigation_bar=self._get_nav_bar(2),
                controls=[
                    Container(
                        content=Column(
                            [
                                AppBar(
                                    title=Text("👤 Водители", size=24, weight="bold")
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

        tenants_content = Container(
            content=Column([], spacing=20),
            padding=40,
            bgcolor=Colors.WHITE,
            expand=True,
        )

        for tenant in tenants_list:
            tenant_card = Container(
                content=Column(
                    [
                        Text(f"{tenant.fullname}", size=14, weight="bold"),
                        Text(f"Телефон: {tenant.phone_number}", size=12),
                        TextButton(
                            "Подробнее",
                            on_click=lambda e: self.page.go(f"/details_{tenant.id}"),
                        ),
                    ],
                    spacing=5,
                ),
                padding=15,
                border_radius=12,
                bgcolor=Colors.GREY_100,
                shadow=True,
            )
            tenants_content.content.controls.append(tenant_card)

        return View(
            route="/tenants",
            navigation_bar=self._get_nav_bar(2),
            controls=[tenants_content],
            floating_action_button=fab,
            floating_action_button_location=FloatingActionButtonLocation.END_FLOAT,
        )
