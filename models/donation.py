from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum 
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base
import enum

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=True)
    postal_code = Column(String, nullable=True)
    country = Column(String, nullable=True)

    # Relationship
    donation = relationship("Donation", back_populates="pickup_address", uselist=False)
    user = relationship("User", back_populates="pickup_address", uselist=False)  # ✅ added


class DonationStatus(str, enum.Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class DonationCategory(str, enum.Enum):
    CLOTHES = "clothes"
    BOOKS = "books"
    ELECTRONICS = "electronics"
    FURNITURE = "furniture"
    FOOD = "food"
    OTHER = "other"

class Donation(Base):
    __tablename__ = "donations"
    
    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String, nullable=False)
    category = Column(Enum(DonationCategory), nullable=False)
    description = Column(Text)
    # pickup_address = Column(String, nullable=False)
    address_id = Column(Integer, ForeignKey("addresses.id"), nullable=False)
    pickup_address = relationship("Address", back_populates="donation", uselist=False)
    image_url = Column(String)
    status = Column(Enum(DonationStatus), default=DonationStatus.PENDING, nullable=False)
    
    # Foreign Keys
    donor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    volunteer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    donor = relationship("User", back_populates="donations", foreign_keys=[donor_id])
    volunteer = relationship("User", back_populates="assigned_donations", foreign_keys=[volunteer_id]) 