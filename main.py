from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import chatsbots  # Import your router
from mangum import Mangum  # For Vercel deployment

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (adjust in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Include routers
app.include_router(chatsbots.app)  # Mount the router

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Hello from FastAPI on Vercel!"}

# ✅ Ensure Mangum is properly used
handler = Mangum(app)  # Required for Vercel deployment