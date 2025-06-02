from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models import UserSectionProgress, SectionState
from app.database import get_session
from typing import Dict
from datetime import datetime

router = APIRouter()

@router.post("/open/")
def mark_section_opened(user_id: int, section_id: int, session: Session = Depends(get_session)):
    progress = session.exec(
        select(UserSectionProgress).where(
            UserSectionProgress.user_id == user_id,
            UserSectionProgress.section_id == section_id
        )
    ).first()

    if not progress:
        progress = UserSectionProgress(user_id=user_id, section_id=section_id, opened_at=datetime.utcnow())
        session.add(progress)
    else:
        progress.opened_at = datetime.utcnow()
    
    session.commit()
    return {"message": "Section marked as opened"}

@router.post("/complete/")
def mark_section_completed(user_id: int, section_id: int, session: Session = Depends(get_session)):
    progress = session.exec(
        select(UserSectionProgress).where(
            UserSectionProgress.user_id == user_id,
            UserSectionProgress.section_id == section_id
        )
    ).first()

    if not progress:
        progress = UserSectionProgress(
            user_id=user_id, section_id=section_id, completed=True, completed_at=datetime.utcnow()
        )
        session.add(progress)
    else:
        progress.completed = True
        progress.completed_at = datetime.utcnow()
    
    session.commit()
    return {"message": "Section marked as completed"}

@router.post("/state/")
def update_section_state(user_id: int, section_id: int, state: Dict, session: Session = Depends(get_session)):
    existing = session.exec(
        select(SectionState).where(
            SectionState.user_id == user_id,
            SectionState.section_id == section_id
        )
    ).first()

    if not existing:
        new_state = SectionState(user_id=user_id, section_id=section_id, state=state)
        session.add(new_state)
    else:
        existing.state.update(state)
    
    session.commit()
    return {"message": "State updated"}

@router.get("/state/")
def get_section_state(user_id: int, section_id: int, session: Session = Depends(get_session)):
    state = session.exec(
        select(SectionState).where(
            SectionState.user_id == user_id,
            SectionState.section_id == section_id
        )
    ).first()
    return {"state": state.state if state else {}}

