# Database setup
from sqlalchemy import create_engine, Column, Integer, String, BOOLEAN
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Connect to database
engine = create_engine('sqlite:///userinfo.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Define user model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    name = Column(String)
    birth_date = Column(String)
    education = Column(String)
    city = Column(String)
    district = Column(String)
    phone = Column(String)
    workplace = Column(String)
    salary = Column(String)
    work_length = Column(String)
    language_known = Column(String)
    language_level = Column(String)
    additional_language = Column(String)
    additional_language_level = Column(String)
    marriage_status = Column(String)
    it_knowledge_level = Column(String)
    referral_source = Column(String)
    isLiked = Column(BOOLEAN)

# Create tables
Base.metadata.create_all(engine)
