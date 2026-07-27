"""Pydantic models for API requests/responses"""
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class UserProfile(BaseModel):
    email: EmailStr
    name: str
    topics: Optional[List[str]] = []
    posts_per_day: int = 3
    platforms: Optional[List[str]] = []


class PostRequest(BaseModel):
    text: str
    hashtags: str
    platforms: List[str]
    image_url: Optional[str] = None
    schedule_time: Optional[datetime] = None


class GenerateIdeaRequest(BaseModel):
    topics: Optional[List[str]] = None
    num_ideas: int = 3


class ChatMessage(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class PostResponse(BaseModel):
    id: str
    text: str
    hashtags: str
    platforms: List[str]
    status: str
    created_at: datetime
    published_at: Optional[datetime] = None


class IdeaResponse(BaseModel):
    topic: str
    angle: str
    key_points: List[str]
    target_audience: str
    platform: str
