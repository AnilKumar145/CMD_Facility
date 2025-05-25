from enum import Enum

class FacilityType(str, Enum):
    HOSPITAL = "HOSPITAL"
    CLINIC = "CLINIC"
    DIAGNOSTICS = "DIAGNOSTICS"