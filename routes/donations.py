from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.requests import Request
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from models.user import User, UserRole
from models.donation import Donation, DonationStatus
from models.humble_coin import HumbleCoin
from schemas.donation import DonationCreate, DonationResponse, DonationAssign, DonationList
from schemas.user import UserProfile
from auth.jwt import get_current_user
from models.donation import Address

router = APIRouter(prefix="/donations", tags=["donations"])

async def get_current_user_obj(current_user_email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == current_user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/donate", response_model=DonationResponse)
async def create_donation(
    request:Request,
    donation_data: DonationCreate,
    current_user: User = Depends(get_current_user_obj),
    db: Session = Depends(get_db)
):
    # Only donors can create donations
    
    print("request",request.body())
    breakpoint()
    if current_user.role != UserRole.DONOR and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only donors can create donations"
        )
    address_data = donation_data.pickup_address
    address = Address(
        street=address_data.street,
        city=address_data.city,
        state=address_data.state,
        postal_code=address_data.postal_code,
        country=address_data.country,
    )
    db.add(address)
    db.flush()       
    donation = Donation(
        item_name=donation_data.item_name,
        category=donation_data.category,
        description=donation_data.description,
        image_url=donation_data.image_url,
        donor_id=current_user.id,
        address_id=address.id
    )

    db.add(donation)
    db.commit()
    db.refresh(donation)

    
    return donation

@router.get("/", response_model=List[DonationList])
async def list_donations(
    current_user: User = Depends(get_current_user_obj),
    db: Session = Depends(get_db)
):
    # Volunteers and admins can see all donations
    if current_user.role in [UserRole.VOLUNTEER, UserRole.ADMIN]:
        donations = db.query(Donation).filter(Donation.status == DonationStatus.PENDING).all()
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only volunteers and admins can view all donations"
        )
    
    return donations

@router.get("/my-donations", response_model=List[DonationList])
async def get_my_donations(
    current_user: User = Depends(get_current_user_obj),
    db: Session = Depends(get_db)
):
    # Users can see their own donations
    donations = db.query(Donation).filter(Donation.donor_id == current_user.id).all()
    return donations

@router.post("/{donation_id}/assign", response_model=DonationResponse)
async def assign_donation(
    donation_id: int,
    assign_data: DonationAssign,
    current_user: User = Depends(get_current_user_obj),
    db: Session = Depends(get_db)
):
    # Only volunteers and admins can assign donations
    if current_user.role not in [UserRole.VOLUNTEER, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only volunteers and admins can assign donations"
        )
    
    donation = db.query(Donation).filter(Donation.id == donation_id).first()
    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")
    
    if donation.status != DonationStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Donation is not available for assignment"
        )
    
    # Verify volunteer exists
    volunteer = db.query(User).filter(User.id == assign_data.volunteer_id).first()
    if not volunteer or volunteer.role not in [UserRole.VOLUNTEER, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid volunteer ID"
        )
    
    donation.volunteer_id = assign_data.volunteer_id
    donation.status = DonationStatus.ASSIGNED
    
    db.commit()
    db.refresh(donation)
    
    return donation

@router.post("/{donation_id}/deliver", response_model=DonationResponse)
async def deliver_donation(
    donation_id: int,
    current_user: User = Depends(get_current_user_obj),
    db: Session = Depends(get_db)
):
    # Only volunteers and admins can mark donations as delivered
    if current_user.role not in [UserRole.VOLUNTEER, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only volunteers and admins can deliver donations"
        )
    
    donation = db.query(Donation).filter(Donation.id == donation_id).first()
    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")
    
    if donation.status != DonationStatus.ASSIGNED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Donation must be assigned before delivery"
        )
    
    # Check if current user is the assigned volunteer (unless admin)
    if current_user.role != UserRole.ADMIN and donation.volunteer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the assigned volunteer can mark as delivered"
        )
    
    donation.status = DonationStatus.DELIVERED
    
    # Award HumbleCoins to the donor
    donor_coins = db.query(HumbleCoin).filter(HumbleCoin.user_id == donation.donor_id).first()
    if donor_coins:
        donor_coins.coins += 10
    else:
        # Create HumbleCoin record if it doesn't exist
        donor_coins = HumbleCoin(user_id=donation.donor_id, coins=10)
        db.add(donor_coins)
    
    db.commit()
    db.refresh(donation)
    
    return donation 