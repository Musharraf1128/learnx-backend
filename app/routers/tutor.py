from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.database import get_session
from app.models import Section, SectionState
from app.utils.llm import generate_section_content

router = APIRouter()

@router.get("/generate/")
def generate_section(user_id: int, section_id: int, session: Session = Depends(get_session)):
    # Step 1: Get section
    section = session.exec(
        select(Section).where(Section.id == section_id)
    ).first()

    if not section:
        return {"error": "Section not found"}

    # Step 2: Get previous section state (if any)
    previous_section_state = session.exec(
        select(SectionState)
        .where(SectionState.user_id == user_id)
        .where(SectionState.section_id == section_id - 1)
    ).first()

    previous_state_dict = previous_section_state.state if previous_section_state else {}

    # Step 3: Craft prompt
    prompt = f"""You are an AI tutor. Generate content for the topic: '{section.title}'.
Given this previous context: {previous_state_dict}

Create a structured response:
- Explanation
- 1 or 2 Examples
- A mini quiz with 2 MCQs and their answers
"""

    # Step 4: Call LLM
    generated = generate_section_content(prompt)

    return {
        "section_id": section.id,
        "title": section.title,
        "content": generated
    }

