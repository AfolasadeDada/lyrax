from sqlalchemy import create_engine, Column, String, Float, Integer
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///claims.db", echo=False)
SessionLocal = sessionmaker(bind=engine)

class Claim(Base):
    __tablename__ = "claims"
    id = Column(Integer, primary_key=True)
    text = Column(String, unique=True)

class Contradiction(Base):
    __tablename__ = "contradictions"
    id = Column(Integer, primary_key=True)
    new_claim = Column(String)
    against = Column(String)
    score = Column(Float)

Base.metadata.create_all(engine)
