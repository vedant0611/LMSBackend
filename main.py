from fastapi import FastAPI
from modules.auth.routes import router as auth_router
from modules.librarian.routes import router as librarian_router
from modules.member.routes import router as member_router

# Create an instance of the FastAPI application
app = FastAPI(title='Library Management System')

# Include the routers for different modules
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(librarian_router, prefix="/librarian", tags=["Librarian"])
app.include_router(member_router, prefix="/member", tags=["Member"])

# Optionally, add a health check endpoint
@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "ok"}

# You can add more global middleware, event handlers, or other configurations here if needed
