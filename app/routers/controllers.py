from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta

from app.database import get_db
from app.services.services import AuthService, ScheduleService, CoordinationService, SysManagementService, MatchingService
import random
router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# --- Helpers ---
def get_user_session(request: Request):
    return request.session.get("user")

def require_role(request: Request, role: str):
    user = get_user_session(request)
    if not user or user['role'] != role:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return user

# --- Input Models ---
class LoginRequest(BaseModel):
    mssv: str
    password: str

class ScheduleRequest(BaseModel):
    action: str
    slots: List[str]

class ProgramRegRequest(BaseModel):
    program_id: int

class BookRequest(BaseModel):
    slot_id: int

class TutorSelectRequest(BaseModel):
    tutor_id: int

# --- ROUTES ---

@router.post("/api/login")
def login(req: LoginRequest, request: Request, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    user = auth_service.login(req.mssv, req.password)
    if user:
        user_data = {"id": user.id, "ho_ten": user.ho_ten, "role": user.role}
        request.session["user"] = user_data
        return {"success": True, "user": user_data}
    return {"success": False, "message": "Sai MSSV hoặc mật khẩu"}
# --- Find Tutor Use Case (NEW) ---

@router.get("/find-tutor", response_class=HTMLResponse)
def view_find_tutor(request: Request):
    user = get_user_session(request)
    if not user or user['role'] != 'student': return RedirectResponse("/")
    return templates.TemplateResponse("find_tutor.html", {"request": request, "user": user})

@router.get("/api/find_tutor")
def api_find_tutor(request: Request, db: Session = Depends(get_db)):
    # 1. Auth check
    user = get_user_session(request)
    if not user: return []

    # 2. Get basic users from DB
    match_service = MatchingService(db)
    tutors_db = match_service.search_tutors()

    # 3. Enrich with Mock Data (since DB is simple) for UI display
    enriched_tutors = []
    departments = ["Khoa học Máy tính", "Điện - Điện tử", "Cơ khí", "Kỹ thuật Hóa học", "Khoa học Ứng dụng"]
    subjects_pool = ["Giải tích 1", "Vật lý 1", "Đại số tuyến tính", "Cấu trúc dữ liệu", "Lập trình C++", "Hóa đại cương"]

    for t in tutors_db:
        enriched_tutors.append({
            "id": t.id,
            "name": t.ho_ten,
            "mssv": t.mssv,
            # Mock details
            "department": random.choice(departments),
            "rating": round(random.uniform(4.0, 5.0), 1),
            "totalSessions": random.randint(10, 50),
            "subjects": random.sample(subjects_pool, k=2),
            "bio": "Sinh viên năm 3 với thành tích học tập xuất sắc. Nhiệt tình hỗ trợ các bạn mất gốc.",
            "avatar": f"https://api.dicebear.com/7.x/avataaars/svg?seed={t.mssv}" # Random avatar based on MSSV
        })
    
    return enriched_tutors

@router.post("/api/select_tutor")
def api_select_tutor(req: TutorSelectRequest, request: Request, db: Session = Depends(get_db)):
    user = require_role(request, 'student')
    match_service = MatchingService(db)
    
    # Logic:
    # 1. Create connection request in DB (Mocked)
    # 2. Send notification to Tutor (Mocked)
    if match_service.select_tutor(user['id'], req.tutor_id):
        return {"success": True, "message": "Đã gửi yêu cầu đến Tutor. Vui lòng chờ xác nhận."}
    return {"success": False, "message": "Có lỗi xảy ra."}
@router.get("/api/logout")
def logout(request: Request):
    request.session.clear()
    return {"success": True}

# --- Student Routes ---
@router.get("/register", response_class=HTMLResponse)
def view_register(request: Request, db: Session = Depends(get_db)):
    user = get_user_session(request)
    if not user or user['role'] != 'student': return RedirectResponse("/")
    
    coord_service = CoordinationService(db)
    programs = coord_service.get_available_programs()
    return templates.TemplateResponse("register.html", {"request": request, "user": user, "programs": programs})

@router.post("/api/register_program")
def register_program(req: ProgramRegRequest, request: Request, db: Session = Depends(get_db)):
    user = require_role(request, 'student')
    coord_service = CoordinationService(db)
    try:
        coord_service.register_student_to_program(user['id'], req.program_id)
        return {"success": True, "message": "Đăng ký thành công!"}
    except Exception as e:
        return {"success": False, "message": str(e)}

# --- Tutor Routes ---

@router.get("/tutor/dashboard", response_class=HTMLResponse)
def view_tutor_dashboard(request: Request):
    user = get_user_session(request)
    if not user or user['role'] != 'tutor': return RedirectResponse("/")
    
    # MOCK DATA from your React component
    # In a real app, you would fetch this from ScheduleService
    pending_requests = [
        {
            "id": 1,
            "date": datetime.now() + timedelta(days=1),
            "subject": "Giải tích 1",
            "studentName": "Nguyễn Văn A",
            "startTime": "08:00",
            "endTime": "10:00",
            "notes": "Em cần hỏi về tích phân suy rộng",
            "status": "pending"
        },
        {
            "id": 2,
            "date": datetime.now() + timedelta(days=2),
            "subject": "Vật lý đại cương",
            "studentName": "Trần Thị B",
            "startTime": "14:00",
            "endTime": "16:00",
            "status": "pending"
        }
    ]
    
    upcoming_sessions = [
        {
            "id": 3,
            "date": datetime.now() + timedelta(days=3),
            "subject": "Đại số tuyến tính",
            "studentName": "Lê Văn C",
            "startTime": "09:00",
            "endTime": "11:00",
            "status": "confirmed",
            "location": "H6-301"
        }
    ]

    return templates.TemplateResponse("tutor_dashboard.html", {
        "request": request, 
        "user": user,
        "pending_requests": pending_requests,
        "upcoming_sessions": upcoming_sessions,
        "total_sessions": 156,
        "active_students": 24,
        "rating": 4.8,
        "teaching_hours": 32.5
    })

@router.get("/schedule", response_class=HTMLResponse)
def view_schedule(request: Request):
    user = get_user_session(request)
    if not user or user['role'] != 'tutor': return RedirectResponse("/")
    return templates.TemplateResponse("schedule.html", {"request": request, "user": user})

@router.get("/api/get_schedule")
def get_schedule(request: Request, db: Session = Depends(get_db)):
    user = get_user_session(request)
    if not user: return []
    service = ScheduleService(db)
    slots = service.get_tutor_schedule(user['id'])
    
    events = []
    for s in slots:
        events.append({
            "title": "Rảnh",
            "start": str(s.start_time).replace(" ", "T"),
            "end": str(s.end_time).replace(" ", "T"),
            "color": "#28a745"
        })
    return events

@router.post("/api/update_schedule")
def update_schedule(req: ScheduleRequest, request: Request, db: Session = Depends(get_db)):
    user = require_role(request, 'tutor')
    service = ScheduleService(db)
    
    try:
        if req.action == 'add':
            for t in req.slots: service.add_slot(user['id'], t)
            msg = "Đã thêm khung giờ"
        elif req.action == 'delete':
            for t in req.slots: service.remove_slot(user['id'], t)
            msg = "Đã xóa khung giờ"
        return {"success": True, "message": msg}
    except Exception as e:
        return {"success": False, "message": str(e)}
    
@router.get("/sso", response_class=HTMLResponse)
async def sso_page(request: Request):
    """
    Simulates the external HCMUT SSO Page.
    """
    return templates.TemplateResponse("hcmut_sso.html", {"request": request})

# --- Admin & Coordinator Routes ---

@router.get("/admin/dashboard", response_class=HTMLResponse)
def view_admin(request: Request, db: Session = Depends(get_db)):
    user = get_user_session(request)
    if not user or user['role'] != 'admin': return RedirectResponse("/")
    sys = SysManagementService(db)
    return templates.TemplateResponse("admin_dashboard.html", {"request": request, "user": user, "users": sys.get_all_users()})

@router.get("/coordinator/dashboard", response_class=HTMLResponse)
def view_coord(request: Request, db: Session = Depends(get_db)):
    user = get_user_session(request)
    if not user or user['role'] != 'coordinator': return RedirectResponse("/")
    coord = CoordinationService(db)
    return templates.TemplateResponse("coordinator_dashboard.html", {"request": request, "user": user, "programs": coord.get_available_programs()})