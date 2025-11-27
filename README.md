# 📘 FastAPI Journal Management & Recommendation Backend

A powerful FastAPI-based backend for managing journal data, uploading Excel files, performing search, and generating recommendations using a **ChromaDB-based RAG (Retrieval-Augmented Generation) service**.

---

## 🚀 Features

### 📤 Excel Upload (Bulk Insert)
Upload `.xlsx` files for:
- Journal data  
- Associate data  
- Clean handling of NaN, NaT, Excel error values  
- Efficient bulk insert into PostgreSQL  

---

### 🔄 Excel-Based Update
Update existing rows in PostgreSQL using Excel:
- Detects existing `_id`
- Updates if exists  
- Inserts new row if missing  
- Works for both **JournalData** and **AssosiateData**

---

## 🔁 Recommendation Logic — How It Works

### ✔️ RAG Service Responsibilities  
The external ChromaDB RAG service returns:
- Vector-based matched journal suggestions  
- With similarity scores  

---

### ✔️ Backend Responsibilities  
Your FastAPI backend handles:

- 🔄 Forwarding topic to the RAG microservice  
- 🗃️ Searching PostgreSQL for matching journals  
- 🔗 Merging RAG similarity scores with SQL journal metadata  
- 📤 Returning the final enriched result to the frontend  

This separation keeps the backend **modular, lightweight, and scalable**.

---

## 📌 Key Endpoints

### 📤 Upload Excel Files
POST /uploadfile-Journal/
POST /upload-Assosiate/

shell
Copy code

### 🔄 Update Records from Excel
POST /update_from_excel

shell
Copy code

### 🔎 Search Journals
GET /journals/search

shell
Copy code

### 🧾 DataFrame-Style Fetching
GET /journals/dataframe
GET /assosiate/dataframe

shell
Copy code

### 📡 Forward Topic to RAG Service
POST /forward-topic/

yaml
Copy code

---

## 🧠 Tech Stack

- **FastAPI**  
- **PostgreSQL (AWS RDS)**  
- **SQLAlchemy ORM**  
- **Pandas for Excel Handling**  
- **ChromaDB (Vector Search)**  
- **Async HTTP (httpx)**  
- **CORS-enabled for React frontend**  
- **Deployed on AWS EC2**  

---

## 🏗️ Architecture Overview

React Frontend
↓
FastAPI Backend (This Project)
↓
ChromaDB RAG Service (Vector Search FastAPI App)
↓
PostgreSQL (Metadata Enrichment)

yaml
Copy code

---

## ⚙️ Cleaning Logic (Auto Fixing Excel Issues)

The backend automatically cleans:
- NaN → `None`
- NaT → `None`
- Excel errors (#REF!, #DIV/0!, #N/A, etc.)
- Blank spaces, “-”, “None”, “null”, etc.

Ensures smooth insertion **without DB failures**.

---

## 📬 Final Output Format (Recommendation API)

{
"message": "Topic forwarded successfully",
"data": [
{
"_id": "...",
"Journal_Name": "...",
"Special_Issue_Name": "...",
"Similarity_Score": 0.82,
...
}
]
}

yaml
Copy code

---

## 🤝 Contributions
Feel free to open issues or PRs — improvements are welcome!

---

## ⭐ Show Support
If you like this project, don’t forget to **star the repository**!

