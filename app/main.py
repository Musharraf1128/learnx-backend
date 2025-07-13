from fastapi import FastAPI
from app.database import init_db
from app.routers import users, topics, sections, progress, tutor
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# localhost POST access granted
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# initialise database on app startup
@app.on_event("startup")
def on_startup():
    init_db()

# Include API routers
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(topics.router, prefix="/topics", tags=["Topics"])
app.include_router(sections.router, prefix="/sections", tags=["Sections"])
app.include_router(progress.router, prefix="/progress", tags=["Progress"])
app.include_router(tutor.router, prefix="/ai", tags=["tutor"])
