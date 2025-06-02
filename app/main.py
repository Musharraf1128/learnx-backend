from fastapi import FastAPI
from app.database import init_db
from app.routers import users, topics, sections, progress, tutor

app = FastAPI(title="learnX-backend")

@app.on_event("startup")
def on_startup():
    init_db()

# Include API routers
# app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(topics.router, prefix="/topics", tags=["Topics"])
app.include_router(sections.router, prefix="/sections", tags=["Sections"])
app.include_router(progress.router, prefix="/progress", tags=["Progress"])
app.include_router(tutor.router, prefix="/ai", tags=["tutor"])
