from fastapi import Depends, FastAPI
from routers import  chatsbots
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(chatsbots.app) 


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}    


from mangum import Mangum
handler = Mangum(app)