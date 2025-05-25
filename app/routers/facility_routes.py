from app.models.facility import Facility
from fastapi import APIRouter, Depends, status, Security
from sqlalchemy.orm import Session
from typing import List
from app.schemas.facility import FacilityDTO, FacilityCreate
from app.schemas.response import ResponseDTO, AddressResponseDTO
from app.FacilityCrud import FacilityService
from app.database import get_db
from app.auth_utils import get_current_user, get_admin_user, get_staff_user, User

router = APIRouter(prefix="/api/facilities", tags=["facilities"])

@router.post("/addFacility", response_model=ResponseDTO[FacilityDTO])
def create_facility(
    facility_dto: FacilityCreate,
    db: Session = Depends(get_db),
    current_user: User = Security(get_current_user, scopes=["ADMIN"])
) -> ResponseDTO[FacilityDTO]:
    # Directly call the static method without creating an instance of FacilityService
    created_facility = FacilityService.create_facility(db, facility_dto)
    return ResponseDTO(
        status_code=status.HTTP_201_CREATED,
        message="Facility created successfully",
        data=created_facility
    )

@router.get("/getFacilityById/{id}", response_model=ResponseDTO[FacilityCreate])
def get_facility_by_id(
    id: int,  # Keep as int since we're querying the id column
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ResponseDTO[FacilityCreate]:
    facility_service = FacilityService()
    facility = facility_service.get_facility_by_id(db, id)
    return ResponseDTO(
        status_code=status.HTTP_200_OK,
        message="Facility retrieved successfully",
        data=facility
    )


@router.get("/getAllFacilities", response_model=ResponseDTO[List[FacilityDTO]])
def get_all_facilities(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ResponseDTO[List[FacilityDTO]]:
    # Call the static method directly without creating an instance
    facilities = FacilityService.get_all_facilities(db)
    return ResponseDTO(
        status_code=status.HTTP_200_OK,
        message="Facilities retrieved successfully",
        data=facilities
    )

@router.patch("/{id}", response_model=ResponseDTO[FacilityDTO])
def update_facility(
    id: int,
    facility_dto: FacilityDTO,
    db: Session = Depends(get_db),
    current_user: User = Security(get_current_user, scopes=["ADMIN", "STAFF"])
) -> ResponseDTO[FacilityDTO]:
    updated_facility = FacilityService.update_facility(db, id, facility_dto)
    return ResponseDTO(
        status_code=status.HTTP_200_OK,
        message="Facility updated successfully",
        data=updated_facility
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_facility(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Security(get_current_user, scopes=["ADMIN"])
) -> None:
    FacilityService.delete_facility(db, id)



@router.get("/{facilityId}/address", response_model=ResponseDTO[AddressResponseDTO])
def get_facility_address(
    facilityId: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ResponseDTO[AddressResponseDTO]:
    address = FacilityService.get_facility_address(db, facilityId)
    return ResponseDTO(
        status_code=status.HTTP_200_OK,
        message="Facility address retrieved successfully",
        data=address
    )

@router.get("/{facilityId}/getFacilityIdAndName", response_model=ResponseDTO[FacilityDTO])
def get_facility_id_and_name(
    facilityId: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ResponseDTO[FacilityDTO]:
    # Create a new method to get facility by facility_id string
    facility = FacilityService.get_facility_by_facility_id(db, facilityId)
    return ResponseDTO(
        status_code=status.HTTP_200_OK,
        message="Facility ID and name retrieved successfully",
        data=facility
    )

@router.get("/facilityNames", response_model=ResponseDTO[List[str]])
def get_facility_names(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ResponseDTO[List[str]]:
    names = FacilityService.get_facility_names(db)
    return ResponseDTO(
        status_code=status.HTTP_200_OK,
        message="Facility names retrieved successfully",
        data=names
    )
