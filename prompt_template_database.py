from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid

# Define the SQLAlchemy base
Base = declarative_base()

# Define the PromptTemplate model
class PromptTemplate(Base):
    __tablename__ = 'prompt_templates'

    id = Column(String, primary_key=True)
    name = Column(String)
    purpose = Column(String)
    template = Column(Text)
    def __init__(self, name, purpose, template):
        self.id = str(uuid.uuid4())
        self.name = name
        self.purpose = purpose
        self.template = template

# Define the database connection
engine = create_engine('sqlite:///prompt_templates.db')

# Create tables
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()
