from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Get DATABASE_URL from environment with fallback
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://cmd_user:GIxYa0Fx753DAD47VNY9pH8Dpuq3Le7l@dpg-d0p91j8dl3ps73aipd3g-a/cmd")

# Add SSL mode for Render if not present
if "sslmode" not in DATABASE_URL:
    DATABASE_URL += "?sslmode=require"

# Create engine with production settings
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    from app.models.facility import Base, Facility, Department
    print("Creating database tables...")
    Base.metadata.drop_all(bind=engine)  # Drop existing tables
    Base.metadata.create_all(bind=engine)  # Create new tables
    print("Database tables created successfully!")
