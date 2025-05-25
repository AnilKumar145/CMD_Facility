from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from .models.facility import Facility
from .models.facility import Department
from .schemas.facility import FacilityDTO, FacilityCreate
from .schemas.response import AddressResponseDTO

class FacilityService:

    @staticmethod
    def create_facility(db: Session, facility_dto: FacilityCreate) -> FacilityCreate:
        # Get the last facility and extract the numeric part of the ID
        last_facility = db.query(Facility).order_by(Facility.facility_id.desc()).first()
        
        if last_facility:
            last_id = int(last_facility.facility_id[3:])  # Extract number after 'FAC'
            next_id = last_id + 1
        else:
            next_id = 1
        
        facility_dto.facility_id = f"FAC{str(next_id).zfill(4)}"  # Format: FAC0001, FAC0002, etc.

        existing_facility_name = db.query(Facility).filter(
            Facility.facility_name == facility_dto.facility_name
        ).first()

        if existing_facility_name:
            raise HTTPException(status_code=400, detail="Facility name already exists")

        # Create departments (if they don't exist already)
        departments = []  # type: ignore
        for dept_name in facility_dto.departments:
            department = db.query(Department).filter(Department.name == dept_name).first()
            if not department:
                department = Department(name=dept_name)
                db.add(department)
                db.commit()
                db.refresh(department)
            departments.append(department)

        # Create facility
        facility = Facility(
            facility_id=facility_dto.facility_id,
            facility_name=facility_dto.facility_name,
            facility_type=facility_dto.facility_type,
            phone_number=facility_dto.phone_number,
            email=facility_dto.email,
            location=facility_dto.location,
            street_address=facility_dto.street_address,
            city=facility_dto.city,
            state=facility_dto.state,
            pincode=facility_dto.pincode,
            country=facility_dto.country,
            departments=departments
        )

        db.add(facility)
        db.commit()
        db.refresh(facility)

        # Convert departments to list of names (strings)
        facility_dto.departments = [dept.name for dept in facility.departments]

        return facility_dto

    
    @staticmethod
    def get_facility_by_id(db: Session, id: int) -> FacilityDTO:
        facility = db.query(Facility).filter(
            Facility.id == id  # Use the numeric id column instead of facility_id
        ).first()

        if not facility:
            raise HTTPException(status_code=404, detail=f"Facility with ID {id} not found")
        
        # Convert to DTO format
        facility_data = {
            "facility_id": facility.facility_id,
            "facility_name": facility.facility_name,
            "facility_type": facility.facility_type,
            "phone_number": facility.phone_number,
            "email": facility.email,
            "location": facility.location,
            "street_address": facility.street_address,
            "city": facility.city,
            "state": facility.state,
            "pincode": facility.pincode,
            "country": facility.country,
            "departments": [dept.name for dept in facility.departments]
        }
        
        return FacilityDTO(**facility_data)

    @staticmethod
    def get_all_facilities(db: Session) -> List[FacilityDTO]:
        facilities = db.query(Facility).all()
        facility_dtos = []
    
        for facility in facilities:
            # Create a dictionary with the facility data
            facility_data = {
                "facility_id": facility.facility_id,
                "facility_name": facility.facility_name,
                "facility_type": facility.facility_type,
                "phone_number": facility.phone_number,
                "email": facility.email,
                "location": facility.location,
                "street_address": facility.street_address,
                "city": facility.city,
                "state": facility.state,
                "pincode": facility.pincode,
                "country": facility.country,
                "departments": [dept.name for dept in facility.departments]
            }
            facility_dtos.append(FacilityDTO(**facility_data))
    
        return facility_dtos
    
    @staticmethod
    def update_facility(db: Session, id: int, facility_dto: FacilityDTO) -> FacilityDTO:
        facility = db.query(Facility).filter(Facility.id == id).first()
        
        if not facility:
            raise HTTPException(status_code=404, detail="Facility not found")
        
        # Convert the DTO to dict and exclude unset values
        update_data = facility_dto.model_dump(exclude_unset=True)
        
        # Handle departments separately
        if 'departments' in update_data:
            department_names = update_data.pop('departments')
            departments = []
            for dept_name in department_names:
                department = db.query(Department).filter(Department.name == dept_name).first()
                if not department:
                    department = Department(name=dept_name)
                    db.add(department)
                    db.commit()
                    db.refresh(department)
                departments.append(department)
            facility.departments = departments

        # Update other fields
        for key, value in update_data.items():
            setattr(facility, key, value)
        
        db.commit()
        db.refresh(facility)

        # Convert to DTO format
        facility_data = {
            "facility_id": facility.facility_id,
            "facility_name": facility.facility_name,
            "facility_type": facility.facility_type,
            "phone_number": facility.phone_number,
            "email": facility.email,
            "location": facility.location,
            "street_address": facility.street_address,
            "city": facility.city,
            "state": facility.state,
            "pincode": facility.pincode,
            "country": facility.country,
            "departments": [dept.name for dept in facility.departments]
        }
        
        return FacilityDTO(**facility_data)

    @staticmethod
    def delete_facility(db: Session, id: int) -> None:
        facility = db.query(Facility).filter(Facility.id == id).first()
        
        if not facility:
            raise HTTPException(status_code=404, detail="Facility not found")
        
        db.delete(facility)
        db.commit()


    @staticmethod
    def get_facility_address(db: Session, facility_id: str) -> AddressResponseDTO:
        facility = db.query(Facility).filter(
            Facility.facility_id == facility_id  # Use facility_id instead of id
        ).first()
        
        if not facility:
            raise HTTPException(
                status_code=404,
                detail=f"Facility with ID {facility_id} not found"
            )
        
        return AddressResponseDTO(
            street_address=facility.street_address,
            city=facility.city,
            state=facility.state,
            country=facility.country,
            pincode=facility.pincode
        )


    @staticmethod
    def get_facility_names(db: Session) -> List[str]:
        return [f.facility_name for f in db.query(Facility.facility_name).all()]

    @staticmethod
    def get_facility_by_facility_id(db: Session, facility_id: str) -> FacilityDTO:
        facility = db.query(Facility).filter(
            Facility.facility_id == facility_id  # Use the string facility_id column
        ).first()

        if not facility:
            raise HTTPException(status_code=404, detail=f"Facility with ID {facility_id} not found")
        
        # Convert to DTO format
        facility_data = {
            "facility_id": facility.facility_id,
            "facility_name": facility.facility_name,
            "facility_type": facility.facility_type,
            "phone_number": facility.phone_number,
            "email": facility.email,
            "location": facility.location,
            "street_address": facility.street_address,
            "city": facility.city,
            "state": facility.state,
            "pincode": facility.pincode,
            "country": facility.country,
            "departments": [dept.name for dept in facility.departments]
        }
        
        return FacilityDTO(**facility_data)
