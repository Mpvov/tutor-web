from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    mssv = Column(String(20), unique=True, index=True)
    password = Column(String(255)) # Stored as plain text per original PHP logic
    ho_ten = Column(String(100))
    role = Column(Enum('student', 'tutor', 'admin', 'coordinator'), default='student')
    
    registrations = relationship("Registration", back_populates="student")
    time_slots = relationship("TimeSlot", back_populates="tutor")
    appointments = relationship("Appointment", back_populates="student")

class Program(Base):
    __tablename__ = "programs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    semester = Column(String(50))
    status = Column(Enum('open', 'closed'), default='open')
    registrations = relationship("Registration", back_populates="program")

class Registration(Base):
    __tablename__ = "registrations"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    program_id = Column(Integer, ForeignKey("programs.id"))
    
    student = relationship("User", back_populates="registrations")
    program = relationship("Program", back_populates="registrations")

class TimeSlot(Base):
    __tablename__ = "time_slots"
    id = Column(Integer, primary_key=True)
    tutor_id = Column(Integer, ForeignKey("users.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    is_booked = Column(Boolean, default=False)
    
    tutor = relationship("User", back_populates="time_slots")
    appointment = relationship("Appointment", back_populates="slot", uselist=False)

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    slot_id = Column(Integer, ForeignKey("time_slots.id"))
    status = Column(Enum('pending', 'confirmed', 'cancelled'), default='confirmed')
    
    student = relationship("User", back_populates="appointments")
    slot = relationship("TimeSlot", back_populates="appointment")