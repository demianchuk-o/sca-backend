from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Target(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    country = Column(String)
    notes = Column(Text, nullable=True)
    complete = Column(Boolean, default=False)
    mission_id = Column(Integer, ForeignKey("mission.id"))

    mission = relationship("Mission", back_populates="targets")