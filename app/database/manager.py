from app.database.models import (
    Setting,
    Car,
    Image,
    ImageCategory,
    Tenant,
    Rental,
    Payment,
    session_factory,
)


class DatabaseManager:
    def __init__(self):
        self.session = session_factory()

    def add_car(
        self,
        brand: str,
        model: str,
        year: int,
        plate_number: str,
        notes: str | None = None,
    ) -> Car:
        new_car = Car(
            brand=brand,
            model=model,
            year=year,
            plate_number=plate_number,
            notes=notes,
        )
        self.session.add(new_car)
        self.session.commit()
        return new_car

    def add_tenant(
        self,
        fullname: str,
        phone_number: str,
        debt_sum: float = 0.0,
    ) -> Tenant:
        new_tenant = Tenant(
            fullname=fullname,
            phone_number=phone_number,
            debt_sum=debt_sum,
        )
        self.session.add(new_tenant)
        self.session.commit()
        return new_tenant

    def get_last_added_cars(self, limit: int = 5):

        last_added_cars = (
            self.session.query(Car).order_by(Car.id.desc()).limit(limit).all()
        )
        images = {}
        for car in last_added_cars:
            if car.images:
                images[car.id] = car.images[0].path
            else:
                images[car.id] = None
        return last_added_cars

    def get_all_cars(self):
        return self.session.query(Car).order_by(Car.updated_at.desc()).all()

    def get_all_tenants(self):
        return self.session.query(Tenant).order_by(Tenant.updated_at.desc()).all()

    def get_all_rentals(self):
        return self.session.query(Rental).order_by(Rental.status.desc()).all()

    def get_all_payments(self):
        return self.session.query(Payment).order_by(Payment.date.desc()).all()

    def save_image_path(
        self, object_type: str, object_id: int, category: ImageCategory, image_path: str
    ) -> str:
        new_image = Image(
            object_id=object_id,
            object_type=object_type,
            category=category,
            path=image_path,
        )
        self.session.add(new_image)
        self.session.commit()
        return image_path

    def get_setting(self, key: str):
        return self.session.query(Setting.value).where(Setting.key == key).scalar()

    def set_setting(self, key: str, value: str = None):
        setting = self.session.query(Setting).where(Setting.key == key).first()
        if setting:
            setting.value = value
        else:
            new_setting = Setting(key=key, value=value)
            self.session.add(new_setting)
        self.session.commit()

    def add_payment(
        self,
        amount: float,
        comment: str | None = None,
        rental_id: int | None = None,
    ) -> Payment:
        new_payment = Payment(
            rental_id=rental_id,
            amount=amount,
            comment=comment,
        )
        self.session.add(new_payment)
        self.session.commit()
        return new_payment
