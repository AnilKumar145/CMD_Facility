from sqlalchemy import Column, Integer, String, Enum, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint
from .FacilityEnum import FacilityType
from app.models.base import Base

# Association table for facility departments
facility_departments = Table(
    'facility_departments',
    Base.metadata,
    Column('facility_id', Integer, ForeignKey('facilities.id', ondelete='CASCADE'), primary_key=True),
    Column('department_name', String, ForeignKey('departments.name', ondelete='CASCADE'), primary_key=True)
)


class Facility(Base):
    __tablename__ = 'facilities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    facility_id = Column(String, unique=True, nullable=False)
    facility_name = Column(String, unique=True, nullable=False)
    facility_type = Column(Enum(FacilityType), nullable=False)
    phone_number = Column(String)
    email = Column(String)
    location = Column(String)
    street_address = Column(String)
    city = Column(String)
    state = Column(String)
    pincode = Column(String)
    country = Column(String)
    
    # Relationship for departments
    departments = relationship(
        "Department",
        secondary=facility_departments,
        backref="facilities",
        cascade="all, delete"
    )

    __table_args__ = (
        UniqueConstraint('facility_id', name='uq_facility_id'),
        UniqueConstraint('facility_name', name='uq_facility_name'),
    )

    def __repr__(self):
        return f"<Facility(id={self.id}, name={self.facility_name}, type={self.facility_type})>"

# Department model
class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return f"<Department(name={self.name})>"
