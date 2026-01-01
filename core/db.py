from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

Base = declarative_base()
engine = create_engine("sqlite:///claims.db", echo=False)
SessionLocal = sessionmaker(bind=engine)

class Claim(Base):
    __tablename__ = "claims"
    id = Column(Integer, primary_key=True)
    text = Column(String, unique=True)
    claim_type = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Contradiction(Base):
    __tablename__ = "contradictions"
    id = Column(Integer, primary_key=True)
    new_claim = Column(String)
    against = Column(String)
    score = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)
