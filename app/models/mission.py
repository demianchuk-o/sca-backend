from sqlalchemy import Boolean, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Mission(Base):
    __tablename__ = "missions"
    id = Column(Integer, primary_key=True, index=True)
    complete = Column(Boolean, default=False)
    cat_id = Column(Integer, ForeignKey("cats.id"), unique=True, nullable=True)

    cat = relationship("Cat", back_populates="cat")
    targets = relationship("Target", back_populates="mission", cascade="all, delete-orphan")