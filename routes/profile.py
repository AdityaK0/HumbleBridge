from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models.user import User
from models.donation import Donation
from models.humble_coin import HumbleCoin
from schemas.user import UserProfile
from auth.jwt import get_current_user

router = APIRouter(prefix="/profile", tags=["profile"])

async def get_current_user_obj(current_user_email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == current_user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=UserProfile)
async def get_profile(
    current_user: User = Depends(get_current_user_obj),
    db: Session = Depends(get_db)
):
    # Get user's HumbleCoin balance
    current_role = current_user.role
    pending_donations = db.query(Donation).filter(Donation.donor_id == current_user.id,Donation.status == "pending").count()    
    delivered_donations = db.query(Donation).filter(Donation.donor_id == current_user.id,Donation.status == "assigned").count()  
    
   

    # total_donations =  db.query(Donation).filter(Donation.volunteer_id == current_user.id).count()  if current_role == "volunteer" else  db.query(Donation).filter(Donation.donor_id == current_user.id).count()
    total_donations = len(current_user.assigned_donations) if current_role == "volunteer" else len(current_user.donations)
    
        
           
    
    humble_coins = db.query(HumbleCoin).filter(HumbleCoin.user_id == current_user.id).first()
    coins = humble_coins.coins if humble_coins else 0
    
    return UserProfile(
        id=current_user.id,
        email=current_user.email,
        role=current_user.role,
        created_at=current_user.created_at,
        pending_donations = pending_donations,
        delivered_donations = delivered_donations,
        total_donations = total_donations,
        coins=coins
    ) 