from sqlmodel import SQLModel, Field, Relationship, JSON
from typing import Optional, Dict
from datetime import datetime
from sqlalchemy import Column, JSON

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    name: str

class Topic(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None

class Section(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    topic_id: int = Field(foreign_key="topic.id")
    title: str
    base_content: str
    template_type: Optional[str] = None  # e.g. "lesson", "quiz"

class UserSectionState(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    section_id: int = Field(foreign_key="section.id")
    stored_key_value_json: Optional[str] = None
    completed: bool = False
    last_visited: datetime = Field(default_factory=datetime.utcnow)

class UserSectionProgress(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    section_id: int = Field(foreign_key="section.id")
    completed: bool = False
    opened_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class SectionState(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    section_id: int = Field(foreign_key="section.id")
    state: Dict = Field(default_factory=dict, sa_column=Column(JSON))

