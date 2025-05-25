from typing import List
from pydantic import BaseModel, EmailStr, Field, field_validator
from enum import Enum
from typing import Optional
import re

class FacilityType(str, Enum):
    HOSPITAL = "HOSPITAL"
    CLINIC = "CLINIC"
    DIAGNOSTICS = "DIAGNOSTICS"

class FacilityDTO(BaseModel):
    # Facility name with constraints
    facility_name: str = Field(
        ..., 
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9 ,.#'\-]*$",
        description="Facility name with alphanumeric characters and special characters"
    )
    facility_id: str = None
    
    facility_type: FacilityType = Field(
        ..., 
        description="Type of the facility"
    )
    
    phone_number: str = Field(
        ..., 
        description="Contact phone number"
    )
    
    email: EmailStr = Field(
        ..., 
        description="Valid email address"
    )
    
    location: str = Field(
        ..., 
        min_length=3,
        max_length=50,
        description="Location of the facility"
    )
    
    street_address: str = Field(
        ..., 
        min_length=3,
        max_length=50,
        description="Street address of the facility"
    )
    
    city: str = Field(
        ..., 
        min_length=3,
        max_length=20,
        description="City name"
    )
    
    state: str = Field(
        ..., 
        min_length=3,
        max_length=20,
        description="State name"
    )
    
    pincode: str = Field(
        ..., 
        min_length=6,
        max_length=6,
        pattern=r"^[0-9]*$",
        description="6-digit numeric pincode"
    )
    
    country: str = Field(
        ..., 
        min_length=3,
        max_length=20,
        description="Country name"
    )
    
    departments: List[str] = Field(
        default=[],
        description="List of department names"
    )

    @field_validator('departments', mode='before')
    @classmethod
    def convert_departments(cls, departments):
        if not departments:
            return []
        # Convert Department objects to strings if they're objects
        return [dept.name if hasattr(dept, 'name') else dept for dept in departments]

    @field_validator('departments')
    @classmethod
    def validate_departments(cls, departments: List[str]) -> List[str]:
        # Validate that department names contain only alphanumeric characters, commas, and spaces
        pattern = re.compile(r"^[a-zA-Z0-9, ]*$")
        for department in departments:
            if not pattern.match(department):
                raise ValueError(
                    "Department names can only contain alphanumeric characters, commas, and spaces"
                )
        return departments

    class Config:
        orm_mode = True  # This is necessary to convert ORM models
        from_attributes = True  # This is necessary to use from_orm
        json_schema_extra = {
            "example": {
                "facility_name": "City General Hospital",
                "facility_type": "HOSPITAL",
                "phone_number": "1234567890",
                "email": "contact@citygeneral.com",
                "location": "Downtown",
                "street_address": "123 Healthcare Ave",
                "city": "Metropolis",
                "state": "State",
                "pincode": "123456",
                "country": "Country",
                "departments": ["Emergency", "Surgery", "Pediatrics"]
            }
        }

class FacilityCreate(FacilityDTO):
    facility_name: str
    facility_type: FacilityType
    phone_number: Optional[str] = None
    email: EmailStr
    location: str
    street_address: str
    city: str
    state: str
    pincode: str
    country: str
    departments: List[str]

    class Config:
        orm_mode = True


