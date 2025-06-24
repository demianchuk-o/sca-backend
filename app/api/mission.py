from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.crud import crud_mission, cat as cat_crud
from app.api import deps

router = APIRouter()

@router.post("/", response_model=schemas.Mission)
def create_mission(*, db: Session = Depends(deps.get_db), mission_in: schemas.MissionCreate):
    """Create new mission with targets."""
    return crud_mission.create_with_targets(db=db, obj_in=mission_in)

@router.get("/", response_model=list[schemas.Mission])
def read_missions(db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100):
    """Retrieve missions."""
    return crud_mission.get_multi(db, skip=skip, limit=limit)

@router.get("/{mission_id}", response_model=schemas.Mission)
def read_mission(*, db: Session = Depends(deps.get_db), mission_id: int):
    """Get mission by ID."""
    mission = crud_mission.get(db=db, id=mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission

@router.post("/{mission_id}/assign/{cat_id}", response_model=schemas.Mission)
def assign_cat_to_mission(*, db: Session = Depends(deps.get_db), mission_id: int, cat_id: int):
    """Assign a cat to a mission."""
    mission = crud_mission.get(db=db, id=mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    if mission.cat_id:
        raise HTTPException(status_code=400, detail="Mission is already assigned")

    cat = cat_crud.get(db=db, cat_id=cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    if cat.mission:
        raise HTTPException(status_code=400, detail="Cat is already on a mission")

    return crud_mission.assign_cat(db=db, mission=mission, cat_id=cat_id)

@router.delete("/{mission_id}", response_model=schemas.Mission)
def delete_mission(*, db: Session = Depends(deps.get_db), mission_id: int):
    """Delete a mission."""
    mission = crud_mission.get(db=db, id=mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    try:
        return crud_mission.remove(db=db, id=mission_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))