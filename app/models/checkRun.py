from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class CheckRun(Base):
    __tablename__ = "checkRuns"

    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'running', 'completed')",
            name="ck_check_runs_status",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid4
    )
    monitor_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("monitors.id"), nullable=False
    )
    scheduled_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pending",
    )
    is_success: Mapped[bool | None]
    http_status_code: Mapped[int | None]
    response_time_ms: Mapped[int | None]
    error_type: Mapped[str | None]
