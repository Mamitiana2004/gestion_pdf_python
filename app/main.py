from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import usersRoute,pdfRoute
from app.middleware.auth_middleware import JWTAuthMiddleware


app = FastAPI()

origins = [
    "http://localhost:3000"
]

@app.get("/")
def read_root():
    return {"message": "ATO"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(JWTAuthMiddleware)


app.include_router(pdfRoute.router, prefix="/api/protected/pdf",tags=["PDFs"])
app.include_router(usersRoute.router, prefix="/users", tags=["Users"])
