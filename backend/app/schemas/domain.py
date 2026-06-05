from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class CampaignBase(BaseModel):
    campaign_name: str
    goal: str
    budget: float
    status: str = "Active"

class CampaignCreate(CampaignBase):
    pass

class Campaign(CampaignBase):
    campaign_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class PostBase(BaseModel):
    content: str
    platform: str
    status: str = "Draft"
    scheduled_time: Optional[datetime] = None

class PostCreate(PostBase):
    campaign_id: int

class Post(PostBase):
    post_id: int
    campaign_id: int
    published_time: Optional[datetime] = None
    
    class Config:
        from_attributes = True
