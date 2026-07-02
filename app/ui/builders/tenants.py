from flet import (
    View,
    Container,
    Column,
    Row,
    Text,
    TextField,
    Icon,
    Icons,
    Image,
    CircleAvatar,
    Alignment,
    Colors,
    AppBar,
    TextButton,
    ElevatedButton,
    FloatingActionButtonLocation,
    FilePicker,
    FilePickerFileType,
    FilePickerUploadEvent,
    SnackBar,
)

from app.ui.builders.base import Builder


class TenantBuilder(Builder):
    def build_tenants_view(self) -> View:
        tenants_list = self.db_manager.get_all_tenants()
        fab = self._build_fab("/add_tenant", self.localization.add_tenant)

        if not tenants_list:
            empty_message = self._build_not_data_container(
                Icon(
                    Icons.PERSON, size=60, color=Colors.GREY_400, align=Alignment.CENTER
                ),
                self.localization.no_added_tenants,
                self.localization.add_tenant,
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
                                    title=Text(
                                        f"👤 {self.localization.tenants}",
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

        def on_phone_number_tap(tenant_phone: str):
            self.page.clipboard.set(tenant_phone)
            snack = SnackBar(self.localization.copied, open=True)
            self.page.overlay.append(snack)

        tenants_content = Column(
            controls=[],
            expand=True,
        )

        for tenant in tenants_list:
            if not tenant.avatar:
                avatar = CircleAvatar(
                    content=Text(tenant.fullname[0].upper(), color=Colors.WHITE),
                    bgcolor=Colors.BLUE_GREY_400,
                    radius=30,
                )
            else:
                avatar = CircleAvatar(
                    content=Image(src=tenant.avatar.path, align=Alignment.CENTER),
                )
            tenant_card = Container(
                content=Column(
                    [
                        Row(
                            controls=[
                                Container(
                                    Column(
                                        [
                                            Text(
                                                f"{tenant.fullname}",
                                                size=20,
                                                weight="bold",
                                                width=280,
                                            ),
                                            Text(
                                                f"{self.localization.phone}: {tenant.phone_number}",
                                                size=16,
                                                on_tap=lambda e: on_phone_number_tap(
                                                    tenant.phone_number
                                                ),
                                            ),
                                            TextButton(
                                                self.localization.details,
                                                on_click=lambda e, t_id: self.page.go(
                                                    f"/details_{t_id}"
                                                ),
                                            ),
                                        ]
                                    ),
                                ),
                                avatar,
                            ]
                        )
                    ],
                    spacing=5,
                ),
                padding=15,
                alignment=Alignment.CENTER_LEFT,
                border_radius=10,
                bgcolor=Colors.GREY_100,
            )
            tenants_content.controls.append(tenant_card)

        return View(
            route="/tenants",
            navigation_bar=self._get_nav_bar(2),
            controls=[Container(content=tenants_content)],
            floating_action_button=fab,
            floating_action_button_location=FloatingActionButtonLocation.END_FLOAT,
        )

    def build_add_tenant_view(self) -> View:
        avatar_path = None
        passport_path = None
        sub_passport_path = None
        drive_license_path = None

        async def _on_avatar_picker_result(self, e: FilePickerUploadEvent):
            if e.files:
                nonlocal avatar_path
                avatar_path = e.files[0].path

        async def _on_passport_picker_result(self, e: FilePickerUploadEvent):
            if e.files:
                nonlocal passport_path
                passport_path = e.files[0].path

        async def _on_sub_passport_picker_result(self, e: FilePickerUploadEvent):
            if e.files:
                nonlocal sub_passport_path
                sub_passport_path = e.files[0].path

        async def _on_drive_license_picker_result(self, e: FilePickerUploadEvent):
            if e.files:
                nonlocal drive_license_path
                drive_license_path = e.files[0].path

        avatar_picker = FilePicker(on_upload=_on_avatar_picker_result)
        passport_picker = FilePicker(on_upload=_on_passport_picker_result)
        sub_passport_picker = FilePicker(on_upload=_on_sub_passport_picker_result)
        drive_license_picker = FilePicker(on_upload=_on_drive_license_picker_result)

        async def pick_avatar_click(e):
            await avatar_picker.pick_files(
                allow_multiple=False, file_type=FilePickerFileType.IMAGE
            )

        async def pick_passport_click(e):
            await passport_picker.pick_files(
                allow_multiple=False, file_type=FilePickerFileType.IMAGE
            )

        async def pick_sub_passport_click(e):
            await sub_passport_picker.pick_files(
                allow_multiple=False, file_type=FilePickerFileType.IMAGE
            )

        async def pick_drive_license_click(e):
            await drive_license_picker.pick_files(
                allow_multiple=False, file_type=FilePickerFileType.IMAGE
            )

        async def save_tenant(e=None):
            tenant_id = self.db_manager.add_tenant(
                fullname=fullname_input.value,
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

        fullname_input = TextField(label=self.localization.fullname, width=300)
        phone_input = TextField(label=self.localization.phone, width=300)
        debt_sum_input = TextField(label=self.localization.debt_in_total, width=300)
        input = Container(
            content=Column(
                [
                    Text(self.localization.new_tenant, size=24, weight="bold"),
                    fullname_input,
                    phone_input,
                    debt_sum_input,
                    TextButton(
                        self.localization.upload_avatar,
                        icon=Icons.UPLOAD_FILE,
                        on_click=pick_avatar_click,
                    ),
                    TextButton(
                        self.localization.upload_passport,
                        icon=Icons.UPLOAD_FILE,
                        on_click=pick_passport_click,
                    ),
                    TextButton(
                        self.localization.upload_subpassport,
                        icon=Icons.UPLOAD_FILE,
                        on_click=pick_sub_passport_click,
                    ),
                    TextButton(
                        self.localization.upload_driver_license,
                        icon=Icons.UPLOAD_FILE,
                        on_click=pick_drive_license_click,
                    ),
                    ElevatedButton(
                        self.localization.save,
                        icon=Icons.SAVE,
                        on_click=save_tenant,
                    ),
                    ElevatedButton(
                        self.localization.back,
                        icon=Icons.ARROW_BACK,
                        on_click=lambda e: self.page.go("/tenants"),
                    ),
                ],
                spacing=15,
            ),
            padding=40,
        )

        return View(
            route="/add_tenant",
            navigation_bar=self._get_nav_bar(2),
            controls=[
                input,
            ],
        )
