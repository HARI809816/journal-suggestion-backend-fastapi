import pandas as pd 
from fastapi import FastAPI, HTTPException, UploadFile, File, Depends, Query
from typing import Optional, List
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from db import SessionLocal, engine, Base
from models import *
import numpy as np
from schemas import JournalColumnsResponse, RecommendationInput
from sqlalchemy import text
import requests
from httpx import AsyncClient
import httpx
import asyncio

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # Allow all origins or add your React domain
    allow_credentials=True,
    allow_methods=["*"],            # IMPORTANT — allows OPTIONS, POST, GET, etc.
    allow_headers=["*"],            # IMPORTANT — allows Content-Type, Authorization
)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def clean_dataframe(df):
    """Clean the dataframe to handle all problematic values"""
    # Replace Excel error strings and problematic values with None
    df = df.replace([
        '#N/A', '#NAME?', '#NULL!', '#NUM!', '#REF!', '#VALUE!', '#DIV/0!',
        'NaN', 'nan', 'NAN', 'None', 'none', 'NONE', 'null', 'NULL',
        '', ' ', '-', 'Not Available'
    ], None)
    
    # Handle date columns specifically to convert NaT to None
    date_columns = [
        'Login_Received_Date', 'Deadline', 'SI_Status_Updated_Date',
        'Login_Status_Last_Updated_Date', 'Deadline_Last_Updated_Date',
        'Updated_Date', 'Date_of_Editorial_Sent'
    ]
    
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            # Replace NaT with None
            df[col] = df[col].apply(lambda x: x.date() if pd.notna(x) else None)
    
    # Clean all remaining NaN/NaT values
    for col in df.columns:
        df[col] = df[col].apply(lambda x: 
            None if (pd.isna(x) or 
                    (hasattr(x, '__class__') and x.__class__.__name__ in ['NaType', 'NaTType']) or
                    str(x) == 'NaT' or str(x) == 'nan' or str(x) == 'NaN' or 
                    (isinstance(x, float) and np.isnan(x))) 
            else x)
    
    return df

@app.post("/uploadfile-Journal/")
async def create_upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Read the uploaded file directly
    #print("helooooooooooo")
    
    # Read with object dtype to avoid initial type conversion issues
    df = pd.read_excel(file.file, engine="openpyxl", dtype=object, keep_default_na=False, na_values=[])
    #print("helooooooooooo")
    
    # Clean the dataframe
    df = clean_dataframe(df)
    
    # Convert DataFrame to list of dictionaries
    records = df.to_dict(orient="records")
    
    # Final check to ensure no problematic values remain in records
    for record in records:
        for key, value in record.items():
            if (pd.isna(value) or 
                (hasattr(value, '__class__') and value.__class__.__name__ in ['NaType', 'NaTType']) or
                str(value) == 'NaT' or str(value) == 'nan' or str(value) == 'NaN' or
                (isinstance(value, float) and np.isnan(value))):
                record[key] = None  # This becomes NULL in SQL

    # Bulk insert
    db.bulk_insert_mappings(JournalData, records)
    db.commit()

    return {
        "message": f"Successfully inserted {len(records)} records"
    }

@app.post("/upload-Assosiate/")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    
    # Read with object dtype to avoid initial type conversion issues
    df = pd.read_excel(file.file, engine="openpyxl", dtype=object, keep_default_na=False, na_values=[])
    
    # Clean the dataframe
    df = clean_dataframe(df)
    
    # Convert DataFrame to list of dictionaries
    records = df.to_dict(orient="records")
    
    # Final check to ensure no problematic values remain in records
    for record in records:
        for key, value in record.items():
            if (pd.isna(value) or 
                (hasattr(value, '__class__') and value.__class__.__name__ in ['NaType', 'NaTType']) or
                str(value) == 'NaT' or str(value) == 'nan' or str(value) == 'NaN' or
                (isinstance(value, float) and np.isnan(value))):
                record[key] = None  # This becomes NULL in SQL

    # Bulk insert
    db.bulk_insert_mappings(AssosiateData, records)
    db.commit()

    return {
        "message": f"Successfully inserted {len(records)} records"
    }



# @app.get("/journals/selected/")
# def get_selected_journals(db: Session = Depends(get_db)):
#     result = db.execute(text("""
#         SELECT _id, "Journal_Name", "Special_Issue_Name", "Special_Issue_keywords" 
#         FROM journal_data
#     """)).fetchall()
    
#     # Return raw data without Pydantic validation to see what's happening
#     raw_data = []
#     for row in result:
#         raw_data.append({
#             "_id": str(row[0]) if row[0] is not None else None,
#             "Journal_Name": row[1],
#             "Special_Issue_Name": row[2],
#             "Special_Issue_keywords": row[3]
#         })
    
#     return raw_data




# @app.get("/journals/csv-pandas")
# def get_journals_csv_pandas(db: Session = Depends(get_db)):
#     # Get the data using pandas
#     df = pd.read_sql_query("""
#         SELECT _id, "Journal_Name", "Special_Issue_Name", "Special_Issue_keywords" 
#         FROM journal_data
#     """, db.bind)
    
#     # Convert to CSV
#     csv_buffer = io.StringIO()
#     df.to_csv(csv_buffer, index=False)
#     csv_data = csv_buffer.getvalue()
#     csv_buffer.close()
    
#     response = StreamingResponse(io.StringIO(csv_data), media_type="text/csv")
#     response.headers["Content-Disposition"] = "attachment; filename=journals.csv"
    
#     return response

@app.get("/journals/dataframe")
def get_journals_dataframe(db: Session = Depends(get_db)):
    # Get the data using pandas
    df = pd.read_sql_query("""
        SELECT _id, "Journal_Name", "Special_Issue_Name", "Special_Issue_keywords" 
        FROM journal_data
    """, db.bind)
    
    # Return the DataFrame as JSON (easiest for your model)
    return df.to_dict(orient='records')





@app.post("/update_from_excel")
async def update_from_excel(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # 1️⃣ Save uploaded excel temporarily
    temp_path = "temp_update.xlsx"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    # 2️⃣ Read excel
    df = pd.read_excel(temp_path, dtype=str)

    df = clean_dataframe(df)
    
    records = df.to_dict(orient="records")

    # 3️⃣ Loop all rows
    for rec in records:

        _id = rec.get("_id")   # primary key

        db_obj = db.query(JournalData).filter(JournalData._id == _id).first()

        if db_obj:
            # -------- UPDATE ----------
            for key, value in rec.items():
                setattr(db_obj, key, value)
        else:
            # -------- INSERT NEW ROW ----------
            new_row = JournalData(**rec)
            db.add(new_row)

    db.commit()

    return {"message": "Database updated successfully"}


@app.get("/journals/search")
def search_journals(
    query: Optional[str] = Query(None, description="Search by Journal Name or Keywords"),
    publisher: Optional[str] = Query(None, description="Filter by Publisher"),
    issn: Optional[str] = Query(None, description="Filter by ISSN"),
    db: Session = Depends(get_db)
):
    sql_query = db.query(JournalData)

    if query:
        search = f"%{query}%"
        sql_query = sql_query.filter(
            (JournalData.Journal_Name.ilike(search)) |
            (JournalData.Special_Issue_keywords.ilike(search))
        )
    
    if publisher:
        sql_query = sql_query.filter(JournalData.Publisher.ilike(f"%{publisher}%"))
        
    if issn:
        sql_query = sql_query.filter(JournalData.ISSN_No == issn)

    results = sql_query.all()
    return results


@app.post("/journals/recommendations")
def get_recommendations(
    recommendations: List[RecommendationInput],
    db: Session = Depends(get_db)
):
    results = []
    for rec in recommendations:
        # Match by Journal_Name and Special_Issue_Name
        # Using ilike for case-insensitive matching to be safer
        db_obj = db.query(JournalData).filter(
            JournalData.Journal_Name.ilike(rec.Journal_Name),
            JournalData.Special_Issue_Name.ilike(rec.Special_Issue_Name)
        ).first()
        
        if db_obj:
            # Convert SQLAlchemy object to dictionary
            obj_dict = {c.name: getattr(db_obj, c.name) for c in JournalData.__table__.columns}
            
            # Add the similarity score from the input
            obj_dict['Similarity_Score'] = rec.Similarity_Score
            
            results.append(obj_dict)
            
    return results

@app.post("/forward-topic/")
async def forward_topic(topic: str):
    # Receive topic from React frontend
    print(f"Received topic from frontend: {topic}")
    
    # Forward the topic to another FastAPI service
    async with AsyncClient() as client:
        try:
            # Replace with your actual target service URL
            response = await client.post(
                "http://other-fastapi-service.com/api/topic",  # Replace with actual URL
                json={"topic": topic},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                return {"message": "Topic forwarded successfully", "data": response.json()}
            else:
                raise HTTPException(status_code=response.status_code, detail="Error from target service")
                
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")

@app.post("/test/")
def test_endpoint(data: dict):
    print("Received data:", data)
    return {"message": "Data received successfully", "data": data}