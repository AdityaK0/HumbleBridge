from sqlalchemy import Column, Integer, String, DateTime, Enum,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base
import enum
from models.donation import Address




class UserRole(str, enum.Enum):
    DONOR = "donor"
    VOLUNTEER = "volunteer"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.DONOR, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    address_id = Column(Integer, ForeignKey("addresses.id"), nullable=True)
    pickup_address = relationship("Address", back_populates="user", uselist=False)
    
    # Relationships
    donations = relationship("Donation", back_populates="donor", foreign_keys="Donation.donor_id")
    assigned_donations = relationship("Donation", back_populates="volunteer", foreign_keys="Donation.volunteer_id")
    humble_coins = relationship("HumbleCoin", back_populates="user", uselist=False) 
    
    
    

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
