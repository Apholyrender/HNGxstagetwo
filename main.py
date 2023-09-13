from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.Account import router as user

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    )

app.include_router(user)

if __name__ == "__main__":
    uvicorn.run(app = "main:app", port= 5000, reload=True) 