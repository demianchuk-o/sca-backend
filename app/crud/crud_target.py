from sqlalchemy.orm import Session
from app.models.target import Target
from app.schemas.target import TargetUpdate

def get(db: Session, id: int) -> Target | None:
    return db.query(Target).filter(Target.id == id).first()

def update(db: Session, *, db_obj: Target, obj_in: TargetUpdate) -> Target:
    if db_obj.mission.complete or db_obj.complete:
        raise ValueError("Cannot update a completed target or mission.")

    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj