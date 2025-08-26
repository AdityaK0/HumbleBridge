from pydantic import BaseModel,HttpUrl
from typing import Optional,List
from datetime import datetime
from models.donation import DonationStatus, DonationCategory


class AddressCreate(BaseModel):
    full_address : str
    street: str
    city: str
    state: str | None = None
    postal_code: str | None = None
    country: str | None = None


class DonationBase(BaseModel):
    item_name: str
    category: DonationCategory
    description: Optional[str] = None
    # pickup_address: str
    pickup_address: AddressCreate
    image_urls: Optional[List[str]] = None

class DonationCreate(DonationBase):
    pass



class AddressResponse(BaseModel):
    id: int
    street: str
    city: str
    state: str | None = None
    postal_code: str | None = None
    country: str | None = None

    class Config:
        orm_mode = True

class DonationResponse(DonationBase):
    id: int
    status: DonationStatus
    donor_id: int
    volunteer_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    pickup_address: AddressResponse

    class Config:
        from_attributes = True

class DonationAssign(BaseModel):
    volunteer_id: int

class DonationList(BaseModel):
    id: int
    item_name: str
    category: DonationCategory
    description: Optional[str] = None
    pickup_address: AddressResponse
    image_url: Optional[str] = None
    status: DonationStatus
    donor_id: int
    volunteer_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True 