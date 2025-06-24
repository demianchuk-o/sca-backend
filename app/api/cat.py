from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.api import deps
from app.services.cat_api import get_valid_cat_breeds, CatBreedServiceError
from app.crud import cat as cat_crud

router = APIRouter()


@router.post("/", response_model=schemas.Cat)
async def create_cat(
    *,
    db: Session = Depends(deps.get_db),
    cat_in: schemas.CatCreate,
) -> models.Cat:
    """
    Create a new cat.
    """
    try:
        valid_breeds = await get_valid_cat_breeds()
    except CatBreedServiceError as e:
        raise HTTPException(status_code=500, detail=str(e))

    if cat_in.breed not in valid_breeds:
        raise HTTPException(status_code=400, detail="Invalid cat breed")

    cat = cat_crud.create(db, obj_in=cat_in)
    return cat


@router.get("/{cat_id}", response_model=schemas.Cat)
def read_cat(
    *,
    db: Session = Depends(deps.get_db),
    cat_id: int,
) -> models.Cat:
    """
    Get a cat by ID.
    """
    cat = cat_crud.get(db, cat_id=cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    return cat


@router.get("/", response_model=list[schemas.Cat])
def read_cats(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> list[models.Cat]:
    """
    Get all cats with pagination.
    """
    cats = cat_crud.get_multi(db, skip=skip, limit=limit)
    return cats


@router.put("/{cat_id}", response_model=schemas.Cat)
def update_cat(
    *,
    db: Session = Depends(deps.get_db),
    cat_id: int,
    cat_in: schemas.CatUpdate,
) -> models.Cat:
    """
    Update a cat.
    """
    cat = cat_crud.get(db, cat_id=cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    cat = cat_crud.update(db, db_obj=cat, obj_in=cat_in)
    return cat


@router.delete("/{cat_id}", response_model=schemas.Cat)
def delete_cat(
    *,
    db: Session = Depends(deps.get_db),
    cat_id: int,
) -> models.Cat:
    """
    Delete a cat.
    """
    cat = cat_crud.remove(db, cat_id=cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    return cat