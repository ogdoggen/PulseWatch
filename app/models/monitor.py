from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Monitor(Base):
    __tablename__ = "monitors"

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid4
    )
    name: Mapped[str] = mapped_column(
        String(100), CheckConstraint("length(trim(name)) > 0"), nullable=False
    )
    url: Mapped[str] = mapped_column(String(2048), nullable=False)
    expected_status_code: Mapped[int] = mapped_column(
        CheckConstraint("expected_status_code >= 200 AND expected_status_code <= 599"),
        nullable=False,
        default=200,
    )
    interval_seconds: Mapped[int] = mapped_column(
        CheckConstraint("interval_seconds IN (60, 300, 900)"), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
