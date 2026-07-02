from flet import (
    Page,
    View,
    Container,
    Column,
    Text,
    TextButton,
    Image,
    GestureDetector,
    Icon,
    Icons,
    NavigationBar,
    NavigationBarDestination,
    Colors,
    Alignment,
    FloatingActionButton,
    SnackBar,
    SnackBarAction,
    Duration,
    Tooltip,
)

from app.database.manager import DatabaseManager
from app.database.models import Car
from app.services.connector import Connector
from app.services.localization import Localization


class Builder:
    def __init__(
        self,
        page: Page,
        db_manager: DatabaseManager | None = None,
        connector: Connector | None = None,
        current_image_indices: dict | None = None,
        localization: Localization | None = None,
    ):
        self.page = page
        self.db_manager = db_manager or DatabaseManager()
        self.connector = connector or Connector()
        self.current_image_indices = current_image_indices or {}
        self.localization = localization or Localization(
            self.db_manager.get_setting("language")
        )

    def _get_nav_bar(self, current_index: int):
        return NavigationBar(
            destinations=[
                NavigationBarDestination(
                    icon=Icons.HOME, label=self.localization.main_menu
                ),
                NavigationBarDestination(
                    icon=Icons.CAR_RENTAL, label=self.localization.cars
                ),
                NavigationBarDestination(
                    icon=Icons.PERSON, label=self.localization.tenants
                ),
                NavigationBarDestination(
                    icon=Icons.KEY, label=self.localization.rentals
                ),
                NavigationBarDestination(
                    icon=Icons.ATTACH_MONEY_OUTLINED, label=self.localization.finances
                ),
            ],
            selected_index=current_index,
            on_change=lambda e: self._handle_nav_change(e.control.selected_index),
        )

    def _handle_nav_change(self, index: int):
        match index:
            case 0:
                self.page.go("/")
            case 1:
                self.page.go("/cars")
            case 2:
                self.page.go("/tenants")
            case 3:
                self.page.go("/rentals")
            case 4:
                self.page.go("/finances")

    def _create_car_card(self, car: Car, car_images: list[str] | None = None):
        car_images = car_images or []
        self.current_image_indices[car.id] = 0

        if car_images:
            image_container = Container(
                content=Image(src=car_images[0]),
                width=300,
                height=200,
            )

            def on_pan_update(e):
                if e.delta_x > 50:
                    self._prev_image(car.id, car_images, image_container)
                elif e.delta_x < -50:
                    self._next_image(car.id, car_images, image_container)

            image_with_swipe = GestureDetector(
                content=image_container,
                on_pan_update=on_pan_update,
            )
            indicator = Text(
                f"1/{len(car_images)}",
                size=12,
                weight="bold",
                color=Colors.BLUE_700,
            )
        else:
            image_container = Container(
                content=Text(
                    self.localization.no_images,
                    size=14,
                    weight="bold",
                    color=Colors.GREY_700,
                ),
                bgcolor=Colors.GREY_200,
            )
            image_with_swipe = image_container
            indicator = Text(
                self.localization.no_images,
                size=12,
                weight="bold",
                color=Colors.GREY_700,
            )

        card = Container(
            content=Column(
                [
                    Text(
                        f"{car.brand} {car.model} ({car.plate_number})",
                        size=14,
                        weight="bold",
                    ),
                    image_with_swipe,
                    indicator,
                ],
                alignment=Alignment.CENTER,
                horizontal_alignment=Alignment.CENTER,
                spacing=10,
            ),
            padding=15,
            border_radius=12,
            bgcolor=Colors.GREY_100,
        )

        card.image_container = image_container
        card.indicator = indicator
        card.car_images = car_images

        return card

    def _next_image(self, car_id: int, images: list[str], image_container: Container):
        if not images:
            return
        if car_id not in self.current_image_indices:
            self.current_image_indices[car_id] = 0

        current = self.current_image_indices[car_id]
        if current < len(images) - 1:
            self.current_image_indices[car_id] += 1
            image_container.content = Image(
                src_base64=images[self.current_image_indices[car_id]]
            )
            image_container.update()

    def _prev_image(self, car_id: int, images: list[str], image_container: Container):
        if not images:
            return
        if car_id not in self.current_image_indices:
            self.current_image_indices[car_id] = 0

        current = self.current_image_indices[car_id]
        if current > 0:
            self.current_image_indices[car_id] -= 1
            image_container.content = Image(
                src_base64=images[self.current_image_indices[car_id]]
            )
            image_container.update()

    def _build_complete_snack_bar(self) -> SnackBar:
        return SnackBar(
            content=Text(self.localization.added_successfully),
            action=SnackBarAction(label="OK"),
            duration=Duration(seconds=5),
        )

    def _build_not_data_container(
        self, icon: Icon, text: str, button_text: str, route: str
    ) -> Container:
        return Container(
            content=Column(
                [
                    icon,
                    Text(
                        text,
                        size=18,
                        weight="bold",
                        color=Colors.BLACK_87,
                        align=Alignment.CENTER,
                    ),
                    TextButton(
                        button_text,
                        icon=Icons.ADD,
                        on_click=lambda _: self.page.go(route),
                        align=Alignment.CENTER,
                    ),
                ],
            ),
            padding=40,
            alignment=Alignment.CENTER,
        )

    def _build_fab(self, route: str, text: str) -> FloatingActionButton:
        return FloatingActionButton(
            icon=Icons.ADD,
            on_click=lambda e: self.page.go(route),
            tooltip=Tooltip(text),
        )

    def _make(self, builder_cls):
        return builder_cls(
            self.page,
            self.db_manager,
            self.connector,
            self.current_image_indices,
            self.localization,
        )

    def build_first_launch_view(self) -> View:
        from app.ui.builders.first_launch import FirstLaunchBuilder

        return self._make(FirstLaunchBuilder).build_first_launch_view()

    def build_home_view(self) -> View:
        from app.ui.builders.home import HomeBuilder

        return self._make(HomeBuilder).build_home_view()

    def build_cars_view(self) -> View:
        from app.ui.builders.cars import CarBuilder

        return self._make(CarBuilder).build_cars_view()

    def build_tenants_view(self) -> View:
        from app.ui.builders.tenants import TenantBuilder

        return self._make(TenantBuilder).build_tenants_view()

    def build_rentals_view(self) -> View:
        from app.ui.builders.rentals import RentalBuilder

        return self._make(RentalBuilder).build_rentals_view()

    def build_finances_view(self) -> View:
        from app.ui.builders.finances import FinanceBuilder

        return self._make(FinanceBuilder).build_finances_view()

    def build_add_car_view(self) -> View:
        from app.ui.builders.cars import CarBuilder

        return self._make(CarBuilder).build_add_car_view()

    def build_add_tenant_view(self) -> View:
        from app.ui.builders.tenants import TenantBuilder

        return self._make(TenantBuilder).build_add_tenant_view()

    def build_add_rental_view(self) -> View:
        return self._build_placeholder_view(
            route="/add_rental",
            title="Добавить аренду",
            description="Страница добавления аренды ещё не реализована.",
            nav_index=3,
        )

    def build_add_payment_view(self) -> View:
        return self._build_placeholder_view(
            route="/add_payment",
            title="Добавить операцию",
            description="Страница добавления платежа ещё не реализована.",
            nav_index=4,
        )

    def _build_placeholder_view(
        self,
        route: str,
        title: str,
        description: str,
        nav_index: int,
    ) -> View:
        content = Column(
            [
                Text(title, size=24, weight="bold"),
                Text(description, size=16, color=Colors.GREY_700),
            ],
            alignment=Alignment.CENTER,
            horizontal_alignment=Alignment.CENTER,
            spacing=20,
        )

        return View(
            route=route,
            navigation_bar=self._get_nav_bar(nav_index),
            controls=[
                Container(
                    content=content,
                    padding=40,
                    bgcolor=Colors.WHITE,
                    width=self.page.width,
                    height=self.page.height - 80,
                    alignment=Alignment.CENTER,
                )
            ],
        )
