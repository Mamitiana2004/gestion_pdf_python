from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import usersRoute,pdfRoute,adminRoute,shipperRoute,consigneRoute,manifestRoute,cargoRoute,rechercheRoute
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


app.include_router(pdfRoute.router, prefix="/api/pdf",tags=["PDFs"])
app.include_router(usersRoute.router, prefix="/users", tags=["Users"])
app.include_router(shipperRoute.router,prefix="/api/shipper",tags=["shippers"])
app.include_router(consigneRoute.router,prefix="/api/consigne",tags=["consignees"])
app.include_router(adminRoute.router,prefix="/api/admin",tags=["ADMIN"])
app.include_router(manifestRoute.router,prefix="/api/manifest",tags=["Manifests"])
app.include_router(cargoRoute.router,prefix="/api/cargo",tags=["cargos"])
app.include_router(rechercheRoute.router,prefix="/api/search",tags=["recherches"])