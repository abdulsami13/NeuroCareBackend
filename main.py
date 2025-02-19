from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import chatsbots
from mangum import Mangum  # ✅ Ensure this is imported

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chatsbots.app)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Hello from FastAPI on Vercel!"}

# ✅ Ensure Mangum is properly used
handler = Mangum(app)