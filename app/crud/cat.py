from sqlalchemy.orm import Session

from app.models.cat import Cat
from app.schemas.cat import CatCreate, CatUpdate


def get(db: Session, cat_id: int) -> Cat | None:
    """
    Retrieve a cat by its ID.
    """
    return db.query(Cat).filter(Cat.id == cat_id).first()

def get_multi(db: Session, skip: int = 0, limit: int = 100) -> list[Cat]:
    """
    Retrieve multiple cats with pagination.
    """
    return db.query(Cat).offset(skip).limit(limit).all()

def create(db: Session, *, obj_in: CatCreate) -> Cat:
    """
    Create a new cat record.
    """
    db_obj = Cat(
        name=obj_in.name,
        years_of_experience=obj_in.years_of_experience,
        breed=obj_in.breed,
        salary=obj_in.salary
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(db: Session, *, db_obj: Cat, obj_in: CatUpdate) -> Cat:
    """
    Update an existing cat record.
    """
    db_obj.salary = obj_in.salary
    db.commit()
    db.refresh(db_obj)
    return db_obj

def remove(db: Session, *, cat_id: int) -> Cat | None:
    """
    Remove a cat record by its ID.
    """
    db_obj = db.query(Cat).filter(Cat.id == cat_id).first()
    if db_obj:
        db.delete(db_obj)
        db.commit()
    return db_obj