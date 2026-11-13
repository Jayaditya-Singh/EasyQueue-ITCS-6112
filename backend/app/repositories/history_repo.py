from sqlalchemy.orm import Session

from app.models.staff_action import StaffAction


def log_action(
        db: Session,
        customer_id: int,
        action_type: str
):
    action = StaffAction(
        customer_id=customer_id,
        action_type=action_type
    )

    db.add(action)
    db.commit()
    db.refresh(action)

    return action


def get_actions_for_customer(db: Session, customer_id: int):
    return (
        db.query(StaffAction)
        .filter(StaffAction.customer_id == customer_id)
        .order_by(StaffAction.timestamp, StaffAction.action_id)
        .all()
    )


def get_recent_actions(db: Session, limit: int = 50):
    return (
        db.query(StaffAction)
        .order_by(StaffAction.timestamp.desc(), StaffAction.action_id.desc())
        .limit(limit)
        .all()
    )
