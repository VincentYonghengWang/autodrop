from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Session

from app.models import RobotActivity


def log_activity(
    db: Session,
    robot_name: str,
    message: str,
    status: str = "success",
    metadata: dict | None = None,
) -> None:
    db.add(
        RobotActivity(
            robot_name=robot_name,
            message=message,
            status=status,
            metadata_json=metadata,
            created_at=datetime.utcnow(),
        )
    )
    db.commit()

