from fastapi import FastAPI
from modules.auth.routes import router as auth_router
from modules.librarian.routes import router as librarian_router
from modules.member.routes import router as member_router

app = FastAPI(

    title='Library Management system'
)

app.include_router(auth_router)
app.include_router(librarian_router)
app.include_router(member_router)