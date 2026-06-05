from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(String) # Admin, Content Manager, Reviewer, etc.
    password_hash = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    approvals = relationship("Approval", back_populates="reviewer")

class Campaign(Base):
    __tablename__ = "campaigns"
    
    campaign_id = Column(Integer, primary_key=True, index=True)
    campaign_name = Column(String, index=True)
    goal = Column(String)
    budget = Column(Float)
    status = Column(String) # Active, Completed, Draft
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    posts = relationship("Post", back_populates="campaign")

class Post(Base):
    __tablename__ = "posts"
    
    post_id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.campaign_id"))
    content = Column(String)
    platform = Column(String) # LinkedIn, Twitter, etc.
    status = Column(String) # Draft, Pending Review, Scheduled, Published
    scheduled_time = Column(DateTime(timezone=True))
    published_time = Column(DateTime(timezone=True), nullable=True)
    
    campaign = relationship("Campaign", back_populates="posts")
    approvals = relationship("Approval", back_populates="post")
    analytics = relationship("Analytics", back_populates="post", uselist=False)

class Approval(Base):
    __tablename__ = "approvals"
    
    approval_id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.post_id"))
    reviewer_id = Column(Integer, ForeignKey("users.user_id"))
    decision = Column(String) # Approved, Rejected
    comments = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    post = relationship("Post", back_populates="approvals")
    reviewer = relationship("User", back_populates="approvals")

class Analytics(Base):
    __tablename__ = "analytics"
    
    analytics_id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.post_id"), unique=True)
    likes = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    reach = Column(Integer, default=0)
    impressions = Column(Integer, default=0)
    
    post = relationship("Post", back_populates="analytics")
