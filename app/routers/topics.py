from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.models import Topic
from app.schemas import TopicCreate, TopicRead
from app.database import get_session

router = APIRouter()

@router.post("/", response_model=TopicRead)
def create_topic(topic: TopicCreate, session: Session = Depends(get_session)):
    new_topic = Topic(title=topic.title, description=topic.description)
    session.add(new_topic)
    session.commit()
    session.refresh(new_topic)
    return new_topic

@router.get("/", response_model=list[TopicRead])
def list_topics(session: Session = Depends(get_session)):
    topics = session.exec(select(Topic)).all()
    return topics

