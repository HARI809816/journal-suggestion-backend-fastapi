from sqlalchemy import create_engine #connector to the database
from sqlalchemy.orm import sessionmaker , declarative_base     #to create a session  and  orm model combine with base class
import os
#from dotenv import load_dotenv

#load_dotenv()

#endpoint = 'database-1.cb042k6ospb1.us-east-1.rds.amazonaws.com'

DATABASE_URL=f"postgresql://d2f2d02328d7d4fc47732019c411df7540f5130d6a6c6460b3dcbb230410fdf7:sk_NGSc_R3hKYu7TQcfCyF2D@db.prisma.io:5432/postgres?sslmode=require"
#DATABASE_URL=f"postgresql+psycopg2://postgres:HariKumar2003@database-1.cb042k6ospb1.us-east-1.rds.amazonaws.com:5432/FastApi"

engine=create_engine(DATABASE_URL)

SessionLocal = sessionmaker( autoflush=False, bind=engine)
Base = declarative_base()
