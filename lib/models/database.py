from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# Create an SQLite database file
ENGINE = create_engine('sqlite:///finance_tracker.db')
Session = sessionmaker(bind=ENGINE)

def init_db():
    Base.metadata.create_all(ENGINE)
    print("Database initialized!")

if __name__ == "__main__":
    init_db()