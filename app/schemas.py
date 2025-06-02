from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    name: str

class UserRead(BaseModel):
    id: int
    email: str 
    name: str

# ─────── Topic ───────
class TopicCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TopicRead(BaseModel):
    id: int
    title: str
    description: Optional[str] = None

# ─────── Section ───────
class SectionCreate(BaseModel):
    topic_id: int
    title: str
    base_content: str
    template_type: Optional[str] = None

class SectionRead(BaseModel):
    id: int
    topic_id: int
    title: str
    base_content: str
    template_type: Optional[str] = None
