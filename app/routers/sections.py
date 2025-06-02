from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models import Section
from app.schemas import SectionCreate, SectionRead
from app.database import get_session

router = APIRouter()

@router.post("/", response_model=SectionRead)
def create_section(section: SectionCreate, session: Session = Depends(get_session)):
    new_section = Section(
        topic_id=section.topic_id,
        title=section.title,
        base_content=section.base_content,
        template_type=section.template_type
    )
    session.add(new_section)
    session.commit()
    session.refresh(new_section)
    return new_section

@router.get("/by_topic/{topic_id}", response_model=list[SectionRead])
def get_sections_by_topic(topic_id: int, session: Session = Depends(get_session)):
    sections = session.exec(select(Section).where(Section.topic_id == topic_id)).all()
    return sections

@router.get("/{section_id}", response_model=SectionRead)
def get_section(section_id: int, session: Session = Depends(get_session)):
    section = session.get(Section, section_id)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    return section

