from sqlalchemy.orm import Session
from app.models.mission import Mission
from app.models.target import Target
from app.schemas.mission import MissionCreate

def get(db: Session, id: int) -> Mission | None:
    return db.query(Mission).filter(Mission.id == id).first()

def get_multi(db: Session, *, skip: int = 0, limit: int = 100) -> list[Mission]:
    return db.query(Mission).offset(skip).limit(limit).all()

def create_with_targets(db: Session, *, obj_in: MissionCreate) -> Mission:
    db_mission = Mission()
    db.add(db_mission)
    db.commit()
    db.refresh(db_mission)

    for target_in in obj_in.targets:
        db_target = Target(**target_in.model_dump(), mission_id=db_mission.id)
        db.add(db_target)
    db.commit()
    db.refresh(db_mission)
    return db_mission

def assign_cat(db: Session, *, mission: Mission, cat_id: int) -> Mission:
    mission.cat_id = cat_id
    db.add(mission)
    db.commit()
    db.refresh(mission)
    return mission

def remove(db: Session, *, id: int) -> Mission | None:
    db_obj = db.query(Mission).get(id)
    if db_obj:
        if db_obj.cat_id:
            raise ValueError("Cannot delete a mission that is assigned to a cat.")
        db.delete(db_obj)
        db.commit()
    return db_obj