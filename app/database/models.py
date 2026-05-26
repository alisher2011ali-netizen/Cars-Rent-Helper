from datetime import datetime
from pathlib import Path
from sqlalchemy import (
    create_engine,
    ForeignKey,
    String,
    Integer,
    Boolean,
    Float,
    DateTime,
    func,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)

data_path = Path("data/")
if not data_path.exists():
    data_path.mkdir()
db_path = data_path / "main.db"

engine = create_engine(f"sqlite:///{db_path}", echo=False)
session_factory = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(primary_key=True)
    brand: Mapped[str] = mapped_column(String(50))
    model: Mapped[str] = mapped_column(String(50))
    year: Mapped[int] = mapped_column(Integer)
    plate_number: Mapped[str] = mapped_column(String(20), unique=True)
    status: Mapped[str] = mapped_column(
        String(20), default="available"
    )  # available/rented/maintenance
    notes: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, onupdate=func.now(), nullable=True
    )

    rentals: Mapped[list["Rental"]] = relationship(back_populates="car")
    images: Mapped[list["CarImage"]] = relationship(
        back_populates="car", cascade="all, delete-orphan"
    )


class CarImage(Base):
    __tablename__ = "car_images"

    id: Mapped[int] = mapped_column(primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"))
    image_path: Mapped[str] = mapped_column(String(300))

    car: Mapped["Car"] = relationship(back_populates="images")


class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(String(150))
    phone_number: Mapped[str] = mapped_column(String(20))
    duty_sum: Mapped[float] = mapped_column(
        Float, default=0.0
    )  # Total amount owed by tenant in rubles
    next_payment_due: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )  # Next payment due date

    avatar_path: Mapped[str | None] = mapped_column(String(300))
    passport_main_path: Mapped[str | None] = mapped_column(String(300))
    passport_sub_path: Mapped[str | None] = mapped_column(String(300))
    driver_license_path: Mapped[str | None] = mapped_column(String(300))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, onupdate=func.now(), nullable=True
    )

    rentals: Mapped[list["Rental"]] = relationship(back_populates="tenant")


class Rental(Base):
    __tablename__ = "rentals"

    id: Mapped[int] = mapped_column(primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"))
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"))

    start_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    end_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    weekly_price: Mapped[float] = mapped_column(Float)
    total_cost: Mapped[float] = mapped_column(
        Float, default=0.0
    )  # weekly_price * number_of_weeks
    status: Mapped[str] = mapped_column(
        String(20), default="active"
    )  # active/completed/cancelled
    notes: Mapped[str | None] = mapped_column(String(500))

    car: Mapped["Car"] = relationship(back_populates="rentals")
    tenant: Mapped["Tenant"] = relationship(back_populates="rentals")
    payments: Mapped[list["Payment"]] = relationship(back_populates="rental")


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    rental_id: Mapped[int | None] = mapped_column(
        ForeignKey("rentals.id"), nullable=True
    )

    amount: Mapped[float] = mapped_column(Float)
    type: Mapped[bool] = mapped_column(Boolean)  # True (income) / False (expense)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    comment: Mapped[str | None] = mapped_column(String(200))

    rental: Mapped["Rental"] = relationship(back_populates="payments")


def init_db():
    Base.metadata.create_all(engine)
