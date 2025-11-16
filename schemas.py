"""
Database Schemas for Sirwa

Each Pydantic model represents a collection in MongoDB.
Collection name is the lowercase class name.
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

class Wardrobeitem(BaseModel):
    """
    Wardrobe items uploaded by users/partners
    Collection: "wardrobeitem"
    """
    title: str = Field(..., description="Item title")
    description: Optional[str] = Field(None, description="Item description")
    size: Optional[str] = Field(None, description="Size label")
    color: Optional[str] = Field(None, description="Color")
    image_url: Optional[str] = Field(None, description="Image URL")
    price_per_day: Optional[float] = Field(None, ge=0, description="Rental price per day in USD")
    tags: Optional[List[str]] = Field(default_factory=list, description="Search tags")

class Review(BaseModel):
    """
    User reviews and ratings
    Collection: "review"
    """
    name: str = Field(..., description="Reviewer name")
    rating: int = Field(..., ge=1, le=5, description="Rating 1-5")
    comment: str = Field(..., description="Review text")
    service: Optional[str] = Field(None, description="Service reviewed (wardrobe, laundry, pets, friend)")

class Pickuprequest(BaseModel):
    """
    Laundry pickup or item delivery pickup requests
    Collection: "pickuprequest"
    """
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Contact email")
    phone: Optional[str] = Field(None, description="Phone number")
    address: str = Field(..., description="Street address")
    latitude: Optional[float] = Field(None, description="Latitude")
    longitude: Optional[float] = Field(None, description="Longitude")
    note: Optional[str] = Field(None, description="Additional notes")
    service: str = Field(..., description="Service type: laundry | wardrobe | pets | friend")

class Luxurykyc(BaseModel):
    """
    Luxury KYC submissions for high-value experiences
    Collection: "luxurykyc"
    """
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    government_id_type: Optional[str] = Field(None, description="Passport, National ID, Driver's License")
    government_id_number: Optional[str] = None
    social_handles: Optional[str] = Field(None, description="Instagram, LinkedIn, etc.")
    purpose: Optional[str] = Field(None, description="Purpose of use")
    consent: bool = Field(..., description="User consents to data verification")
