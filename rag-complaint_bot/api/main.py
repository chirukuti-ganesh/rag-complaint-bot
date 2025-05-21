# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel, EmailStr
# from uuid import uuid4
# from datetime import datetime
# import sqlite3

# app = FastAPI()

# # Create DB and table
# conn = sqlite3.connect("complaints.db", check_same_thread=False)
# cursor = conn.cursor()
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS complaints (
#     complaint_id TEXT PRIMARY KEY,
#     name TEXT,
#     phone_number TEXT,
#     email TEXT,
#     complaint_details TEXT,
#     created_at TEXT
# )
# """)
# conn.commit()

# class Complaint(BaseModel):
#     name: str
#     phone_number: str
#     email: EmailStr
#     complaint_details: str

# @app.post("/complaints")
# def create_complaint(complaint: Complaint):
#     try:
#         print("Received complaint:", complaint.dict())  # Log incoming payload
#         complaint_id = str(uuid4())[:8].upper()
#         created_at = datetime.utcnow().isoformat()
#         cursor.execute(
#             "INSERT INTO complaints VALUES (?, ?, ?, ?, ?, ?)",
#             (complaint_id, complaint.name, complaint.phone_number,
#              complaint.email, complaint.complaint_details, created_at)
#         )
#         conn.commit()
#         print("Inserted complaint successfully")
#         return {"complaint_id": complaint_id, "message": "Complaint created successfully"}
#     except Exception as e:
#         print("❌ Error in /complaints:", e)
#         raise HTTPException(status_code=500, detail=str(e))


# @app.get("/complaints/{complaint_id}")
# def get_complaint(complaint_id: str):
#     cursor.execute("SELECT * FROM complaints WHERE complaint_id = ?", (complaint_id,))
#     row = cursor.fetchone()
#     if not row:
#         raise HTTPException(status_code=404, detail="Complaint not found")
#     return {
#         "complaint_id": row[0],
#         "name": row[1],
#         "phone_number": row[2],
#         "email": row[3],
#         "complaint_details": row[4],
#         "created_at": row[5]
#     }
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr, validator
from uuid import uuid4
from datetime import datetime
import sqlite3
import traceback

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS Middleware (for frontend like Streamlit to access this API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency for DB connection
def get_db():
    conn = sqlite3.connect("complaints.db")
    try:
        yield conn
    finally:
        conn.close()

# Create table on startup
@app.on_event("startup")
def create_table():
    with sqlite3.connect("complaints.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            complaint_id TEXT PRIMARY KEY,
            name TEXT,
            phone_number TEXT,
            email TEXT,
            complaint_details TEXT,
            created_at TEXT
        )
        """)
        conn.commit()

# Request model
class Complaint(BaseModel):
    name: str
    phone_number: str
    email: EmailStr
    complaint_details: str

    @validator('phone_number')
    def validate_phone(cls, v):
        if not v.isdigit() or len(v) not in [10, 11, 12]:
            raise ValueError("Invalid phone number")
        return v

# Endpoint to create complaint
@app.post("/complaints")
def create_complaint(complaint: Complaint, db: sqlite3.Connection = Depends(get_db)):
    try:
        print("Received complaint:", complaint.dict())
        cursor = db.cursor()  # ✅ Fixed: get cursor from db connection
        complaint_id = str(uuid4())[:8].upper()
        created_at = datetime.utcnow().isoformat()

        cursor.execute(
            "INSERT INTO complaints VALUES (?, ?, ?, ?, ?, ?)",
            (complaint_id, complaint.name, complaint.phone_number,
             complaint.email, complaint.complaint_details, created_at)
        )
        db.commit()
        print("Inserted complaint successfully")
        return {"complaint_id": complaint_id, "message": "Complaint created successfully"}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Endpoint to retrieve complaint
@app.get("/complaints/{complaint_id}")
def get_complaint(complaint_id: str, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM complaints WHERE complaint_id = ?", (complaint_id,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return {
        "complaint_id": row[0],
        "name": row[1],
        "phone_number": row[2],
        "email": row[3],
        "complaint_details": row[4],
        "created_at": row[5]
    }
