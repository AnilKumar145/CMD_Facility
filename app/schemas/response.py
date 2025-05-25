from typing import Generic, TypeVar, Optional, List
from pydantic import BaseModel

T = TypeVar('T')

class ResponseDTO(BaseModel, Generic[T]):
    status_code: int
    message: str
    data: Optional[T] = None

class AddressResponseDTO(BaseModel):
    street_address: str
    city: str
    state: str
    pincode: str
    country: str