import flet as ft

from ui.builders.base import Builder


class TenantBuilder(Builder):
    def build_tenants_view(self) -> ft.View:
        tenants_list = self.db_manager.get_all_tenants()
        fab = self._build_fab("/add_tenant", self.localization.add_tenant)

        if not tenants_list:
            empty_message = self._build_not_data_container(
                ft.Icon(
                    ft.Icons.PERSON,
                    size=60,
                    color=ft.Colors.GREY_400,
                    align=ft.Alignment.CENTER,
                ),
                self.localization.no_added_tenants,
                self.localization.add_tenant,
                "/add_tenant",
            )
            return ft.View(
                route="/tenants",
                navigation_bar=self._get_nav_bar(2),
                controls=[
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.AppBar(
                                    title=ft.Text(
                                        f"👤 {self.localization.tenants}",
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

        def on_phone_number_tap(tenant_phone: str):
            self.page.clipboard.set(tenant_phone)
            snack = ft.SnackBar(self.localization.copied, open=True)
            self.page.overlay.append(snack)

        tenants_content = ft.Column(
            controls=[],
            expand=True,
        )

        for tenant in tenants_list:
            if not tenant.avatar:
                avatar = ft.CircleAvatar(
                    content=ft.Text(
                        tenant.last_name[0].upper(), size=50, color=ft.Colors.WHITE
                    ),
                    bgcolor=ft.Colors.BLUE_GREY_400,
                    radius=65,
                    expand=False,
                )
            else:
                avatar = ft.CircleAvatar(
                    content=ft.Image(src=tenant.avatar.path, align=ft.Alignment.CENTER),
                    radius=65,
                    expand=False,
                )
            tenant_card = ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            controls=[
                                ft.Container(
                                    ft.Column(
                                        [
                                            ft.Text(
                                                f"{tenant.last_name} {tenant.first_name}",
                                                size=20,
                                                weight="bold",
                                                width=200,
                                            ),
                                            ft.Text(
                                                tenant.phone_number,
                                                size=20,
                                                on_tap=lambda e: on_phone_number_tap(
                                                    tenant.phone_number
                                                ),
                                            ),
                                            ft.TextButton(
                                                ft.Text(
                                                    self.localization.details, size=16
                                                ),
                                                on_click=lambda e, t_id: self.page.go(
                                                    f"/details_{t_id}"
                                                ),
                                            ),
                                        ],
                                    ),
                                ),
                                avatar,
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        )
                    ],
                    spacing=5,
                ),
                padding=10,
                alignment=ft.Alignment.CENTER_LEFT,
                bgcolor=ft.Colors.GREY_100,
            )
            tenants_content.controls.append(tenant_card)

        return ft.View(
            route="/tenants",
            navigation_bar=self._get_nav_bar(2),
            controls=[ft.Container(content=tenants_content)],
            floating_action_button=fab,
            floating_action_button_location=ft.FloatingActionButtonLocation.END_FLOAT,
        )

    def build_add_tenant_view(self) -> ft.View:
        avatar_path = None
        passport_path = None
        sub_passport_path = None
        drive_license_path = None

        async def _on_avatar_picker_result(self, e: ft.FilePickerUploadEvent):
            if e.files:
                nonlocal avatar_path
                avatar_path = e.files[0].path

        async def _on_passport_picker_result(self, e: ft.FilePickerUploadEvent):
            if e.files:
                nonlocal passport_path
                passport_path = e.files[0].path

        async def _on_sub_passport_picker_result(self, e: ft.FilePickerUploadEvent):
            if e.files:
                nonlocal sub_passport_path
                sub_passport_path = e.files[0].path

        async def _on_drive_license_picker_result(self, e: ft.FilePickerUploadEvent):
            if e.files:
                nonlocal drive_license_path
                drive_license_path = e.files[0].path

        avatar_picker = ft.FilePicker(on_upload=_on_avatar_picker_result)
        passport_picker = ft.FilePicker(on_upload=_on_passport_picker_result)
        sub_passport_picker = ft.FilePicker(on_upload=_on_sub_passport_picker_result)
        drive_license_picker = ft.FilePicker(on_upload=_on_drive_license_picker_result)

        async def pick_avatar_click(e):
            await avatar_picker.pick_files(
                allow_multiple=False, file_type=ft.FilePickerFileType.IMAGE
            )

        async def pick_passport_click(e):
            await passport_picker.pick_files(
                allow_multiple=False, file_type=ft.FilePickerFileType.IMAGE
            )

        async def pick_sub_passport_click(e):
            await sub_passport_picker.pick_files(
                allow_multiple=False, file_type=ft.FilePickerFileType.IMAGE
            )

        async def pick_drive_license_click(e):
            await drive_license_picker.pick_files(
                allow_multiple=False, file_type=ft.FilePickerFileType.IMAGE
            )

        async def save_tenant(e=None):
            tenant_id = self.db_manager.add_tenant(
                last_name=last_name_input.value.strip(),
                first_name=first_name_input.value.strip(),
                middle_name=middle_name_input.value.strip(),
                phone_number=phone_input.value,
                debt_sum=float(debt_sum_input.value) if debt_sum_input.value else 0.0,
            ).id

            if avatar_path:
                await self.connector.save_image(
                    image_path=avatar_path,
                    object_id=tenant_id,
                    object_type="tenant",
                    category="avatar",
                )
            if passport_path:
                await self.connector.save_image(
                    image_path=passport_path,
                    object_id=tenant_id,
                    object_type="tenant",
                    category="passport",
                )
            if sub_passport_path:
                await self.connector.save_image(
                    image_path=sub_passport_path,
                    object_id=tenant_id,
                    object_type="tenant",
                    category="sub_passport",
                )
            if drive_license_path:
                await self.connector.save_image(
                    image_path=drive_license_path,
                    object_id=tenant_id,
                    object_type="tenant",
                    category="drive_license",
                )

            self._build_complete_snack_bar()
            self.page.go("/tenants")

        last_name_input = ft.TextField(label=self.localization.last_name, width=300)
        first_name_input = ft.TextField(label=self.localization.first_name, width=300)
        middle_name_input = ft.TextField(label=self.localization.middle_name, width=300)

        phone_input = ft.TextField(label=self.localization.phone, width=300)
        debt_sum_input = ft.TextField(label=self.localization.debt_in_total, width=300)
        input = ft.Container(
            content=ft.Column(
                [
                    ft.Text(self.localization.new_tenant, size=24, weight="bold"),
                    last_name_input,
                    first_name_input,
                    middle_name_input,
                    phone_input,
                    debt_sum_input,
                    ft.TextButton(
                        self.localization.upload_avatar,
                        icon=ft.Icons.UPLOAD_FILE,
                        on_click=pick_avatar_click,
                    ),
                    ft.TextButton(
                        self.localization.upload_passport,
                        icon=ft.Icons.UPLOAD_FILE,
                        on_click=pick_passport_click,
                    ),
                    ft.TextButton(
                        self.localization.upload_subpassport,
                        icon=ft.Icons.UPLOAD_FILE,
                        on_click=pick_sub_passport_click,
                    ),
                    ft.TextButton(
                        self.localization.upload_driver_license,
                        icon=ft.Icons.UPLOAD_FILE,
                        on_click=pick_drive_license_click,
                    ),
                    ft.ElevatedButton(
                        self.localization.save,
                        icon=ft.Icons.SAVE,
                        on_click=save_tenant,
                    ),
                    ft.ElevatedButton(
                        self.localization.back,
                        icon=ft.Icons.ARROW_BACK,
                        on_click=lambda e: self.page.go("/tenants"),
                    ),
                ],
                spacing=15,
            ),
            padding=40,
        )

        return ft.View(
            route="/add_tenant",
            navigation_bar=self._get_nav_bar(2),
            controls=[
                input,
            ],
        )
