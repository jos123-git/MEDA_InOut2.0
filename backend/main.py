from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel  # Added for data validation
from passlib.context import CryptContext  # Added for security
from datetime import datetime

import models
import database

# --- 1. Security Setup ---
# This handles the logic for checking hashed passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI(title="Inout HR API")

# --- 2. Pydantic Schemas ---
# This defines what the Login JSON should look like
class UserLogin(BaseModel):
    email: str
    password: str

# Add this to your Pydantic schemas section
class EmployeeCreate(BaseModel):
    id: str
    name: str
    role: str

# Update your existing POST route
@app.post("/api/employees")
def create_employee(emp_data: EmployeeCreate, db: Session = Depends(database.get_db)):
    # Check if ID exists
    exists = db.query(models.Employee).filter(models.Employee.id == emp_data.id).first()
    if exists:
        raise HTTPException(status_code=400, detail="Employee ID already exists")

    new_emp = models.Employee(
        id=emp_data.id,
        name=emp_data.name,
        role=emp_data.role,
        status="Offline" # Default status
    )
    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)
    return new_emp

# --- 3. Database Initialization ---
models.Base.metadata.create_all(bind=database.engine)

# --- 4. CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 5. Routes ---

@app.get("/")
def read_root():
    return {"status": "Online", "database": "PostgreSQL Connected"}

# --- NEW: LOGIN ROUTE ---
@app.post("/api/login")
def login(credentials: UserLogin, db: Session = Depends(database.get_db)):
    # 1. Look for the HR User in the database
    user = db.query(models.User).filter(models.User.email == credentials.email).first()

    # 2. Check if user exists AND if the password matches the hash
    if not user or not pwd_context.verify(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # 3. Return user info to the frontend
    return {
        "user": {
            "email": user.email,
            "name": user.full_name,
            "role": user.role
        }
    }

# --- EMPLOYEE ROUTES ---

@app.get("/api/employees")
def get_employees(db: Session = Depends(database.get_db)):
    employees = db.query(models.Employee).all()
    return employees

@app.post("/api/employees/bulk")
def create_bulk_employees(emps:List[EmployeeCreate],db:Session=Depends(database.get_db)):
    new_list=[]
    for e in emps:
        if not db.query(models.Employee).filter(models.Employee.id==e.id).first():
            new_list.append(models.Employee(**e.dict(),status="Offline"))
    if new_list:
        db.add_all(new_list)
        db.commit()
    return {"msg":f"Added {len(new_list)} employees"}

# --- DELETE EMPLOYEE ---
@app.delete("/api/employees/{emp_id}")
def delete_employee(emp_id: str, db: Session = Depends(database.get_db)):
    # Find the target employee
    employee = db.query(models.Employee).filter(models.Employee.id == emp_id).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    try:
        # Delete the employee (Cascading must be handled in models.py)
        db.delete(employee)
        db.commit()
        return {"message": f"Employee {emp_id} successfully purged from system"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Check for linked activity logs before deleting.")

# --- LOGGING ROUTES ---

@app.post("/api/logs")
def create_log(emp_id: str, action: str, db: Session = Depends(database.get_db)):
    new_log = models.ActivityLog(employee_id=emp_id, action=action)
    db.add(new_log)
    db.commit()
    return {"message": "Log recorded successfully"}

@app.post("/api/logs/{emp_id}")
def log_activity(emp_id: str, activity_name: str, db: Session = Depends(database.get_db)):
    emp = db.query(models.Employee).filter(models.Employee.id == emp_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    new_log = models.ActivityLog(
        employee_id=emp_id,
        action=activity_name,
        timestamp=datetime.utcnow()
    )

    emp.status = "Online"
    emp.last_sync = datetime.utcnow()

    db.add(new_log)
    db.commit()

    return {"message": f"Log recorded for {emp.name}", "status": "Online"}
# --- LEAVE MANAGEMENT ROUTES ---
@app.get("/api/leaves")
def get_leaves(db:Session=Depends(database.get_db)):
    return db.query(models.LeaveRequest).all()

@app.patch("/api/leaves/{id}")
def update_leave(id:int, status:str, db:Session=Depends(database.get_db)):
    leave = db.query(models.LeaveRequest).filter(models.LeaveRequest.id==id).first()
    if not leave: raise HTTPException(404,"Request not found")
    leave.status = status
    db.commit()
    return {"msg": f"Request {status}"}
