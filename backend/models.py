from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True) # <--- Make sure this exists!
    full_name = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="Admin")

class Employee(Base):
    """
    This table stores the staff members being monitored
    by the desktop harvester.
    """
    __tablename__ = "employees"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    role = Column(String)
    status = Column(String, default="Offline")
    last_sync = Column(DateTime, default=datetime.datetime.utcnow)

    # Optional: Relationship to easily pull an employee's logs
    logs = relationship("ActivityLog", back_populates="employee")

class LeaveRequest(Base):
    __tablename__ = "leave_requests"
    id = Column(Integer, primary_key=True)
    emp_id = Column(String, ForeignKey("employees.id"))
    leave_type = Column(String) # Vacation, Sick, Personal
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(String, default="Pending") # Pending, Approved, Rejected

class ActivityLog(Base):
    """
    This table records every action sent by the desktop app.
    """
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    # Linked to the 'id' in the employees table
    employee_id = Column(String, ForeignKey("employees.id"))
    action = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    # Optional: Relationship to easily find which employee own this log
    employee = relationship("Employee", back_populates="logs")
