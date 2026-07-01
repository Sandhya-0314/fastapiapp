from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine
from routers.auth import router as auth_router
from routers.company import router as company_router
from routers.job import router as job_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print(engine)

app.include_router(auth_router)
app.include_router(company_router)
app.include_router(job_router)

@app.get("/")
def read_root():
    return {"hello":"world"}
@app.get("/about")
def read_about():
    return {"about":"this is about page"}

@app.get("/contact")
def read_contact():
    return {"contact":"this is contact page"}