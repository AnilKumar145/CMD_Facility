from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.routers.facility_routes import router as facility_routes
from app.database import engine
from app.models import Base
from app.auth_utils import get_current_user, User

app = FastAPI(
    title="Facility Micro-services",
    description="API for managing Facilities in the system",
    version="1.0.0",
    swagger_ui_parameters={
        "deepLinking": True,
        "displayOperationId": True,
        "defaultModelsExpandDepth": 3,
        "defaultModelExpandDepth": 3,
        "docExpansion": "list",
        "filter": True,
        "showExtensions": True,
        "showCommonExtensions": True,
        "persistAuthorization": True  # This will keep the authorization token in the UI
    }
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(facility_routes)

@app.get("/")
def read_root():
    return {"message": "Facility Microservice Running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {
        "message": "This is a protected route",
        "user": current_user.username,
        "role": current_user.role
    }
app.include_router(facility_routes)
