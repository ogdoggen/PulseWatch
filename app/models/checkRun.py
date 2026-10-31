from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Uuid, ForeignKey, CheckConstraint

from app.db.base import Base


class CheckRun(Base):
    __tablename__ = "checkRuns"

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid4()
    )
    monitor_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("monitor.id"), nullable=False
    )
    scheduled_at: Mapped[datetime] = mapped_column(nullable=False)
    completed_at: Mapped[datetime | None]
    status: Mapped[str] = mapped_column(
        String(20),
        CheckConstraint("status IN ('pending', 'running', 'completed')"),
        nullable=False,
        default="pending",
    )
    is_success: Mapped[bool | None]
    http_status_code: Mapped[int | None]
    response_time_ms: Mapped[int | None]
    error_type: Mapped[str | None]
