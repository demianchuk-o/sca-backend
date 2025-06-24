from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.crud import crud_target
from app.api import deps

router = APIRouter()

@router.put("/{target_id}", response_model=schemas.Target)
def update_target(
    *,
    db: Session = Depends(deps.get_db),
    target_id: int,
    target_in: schemas.TargetUpdate,
):
    """
    Update target notes or completion status.
    """
    target = crud_target.get(db=db, id=target_id)
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")

    try:
        updated_target = crud_target.update(db=db, db_obj=target, obj_in=target_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if updated_target.complete:
        mission = updated_target.mission
        if all(t.complete for t in mission.targets):
            mission.complete = True
            db.add(mission)
            db.commit()

    return updated_target