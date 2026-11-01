from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Monitor(Base):
    __tablename__ = "monitors"

    __table_args__ = (
        CheckConstraint(
            "length(trim(name)) > 0",
            name="ck_monitors_name_not_blank",
        ),
        CheckConstraint(
            "expected_status_code BETWEEN 200 AND 599",
            name="ck_monitors_expected_status_code",
        ),
        CheckConstraint(
            "interval_seconds IN (60, 300, 900)",
            name="ck_monitors_interval_seconds",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid4
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    url: Mapped[str] = mapped_column(String(2048), nullable=False)
    expected_status_code: Mapped[int] = mapped_column(nullable=False, default=200 )
    interval_seconds: Mapped[int] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)

