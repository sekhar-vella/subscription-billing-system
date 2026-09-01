from sqlalchemy.orm import Session

from app import models


def create_audit_log(
    db: Session,
    entity_type: str,
    entity_id: int,
    action: str,
    old_value=None,
    new_value=None,
    performed_by: str = "system"
):
    audit_log = models.AuditLog(
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        old_value=old_value,
        new_value=new_value,
        performed_by=performed_by
    )

    db.add(audit_log)
    db.commit()
    db.refresh(audit_log)

    return audit_log