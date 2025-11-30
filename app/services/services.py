from sqlalchemy.orm import Session
from datetime import datetime
from app.repositories.repos import UserRepository, ScheduleRepository, ProgramRepository, SystemRepository
from app.integration.adapters import SSOAdapter
from app.domain.rules import ScheduleDomain

class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
        self.sso_adapter = SSOAdapter()

    def login(self, mssv: str, password: str):
        if not self.sso_adapter.authenticate(mssv, password):
            return None
        user = self.user_repo.get_by_mssv(mssv)
        if user and user.password == password:
            return user
        return None

class ScheduleService:
    def __init__(self, db: Session):
        self.schedule_repo = ScheduleRepository(db)
        self.domain = ScheduleDomain()

    def get_tutor_schedule(self, tutor_id: int):
        return self.schedule_repo.get_slots_by_tutor(tutor_id)

    def add_slot(self, tutor_id: int, start_time_str: str):
        # Convert JS ISO string (e.g., '2025-12-10T14:00:00') to Python datetime
        clean_time = start_time_str.replace("T", " ")[:16]
        start_time = datetime.strptime(clean_time, "%Y-%m-%d %H:%M")
        end_time = self.domain.validate_slot_time(start_time)
        return self.schedule_repo.create_slot(tutor_id, start_time, end_time)

    def remove_slot(self, tutor_id: int, start_time_str: str):
        clean_time = start_time_str.replace("T", " ")[:16]
        start_time = datetime.strptime(clean_time, "%Y-%m-%d %H:%M")
        self.schedule_repo.delete_slot(tutor_id, start_time)

    def book_appointment(self, student_id: int, slot_id: int):
        slot = self.schedule_repo.get_slot_by_id(slot_id)
        if not slot or slot.is_booked:
            raise Exception("Khung giờ đã được đặt hoặc không tồn tại")
        self.schedule_repo.mark_booked(slot_id)
        self.schedule_repo.create_appointment(student_id, slot_id)

class CoordinationService:
    def __init__(self, db: Session):
        self.prog_repo = ProgramRepository(db)

    def get_available_programs(self):
        return self.prog_repo.get_open_programs()

    def register_student_to_program(self, student_id: int, program_id: int):
        return self.prog_repo.register_student(student_id, program_id)
    
    def create_new_program(self, name: str, semester: str):
        return self.prog_repo.create_program(name, semester)

class SysManagementService:
    def __init__(self, db: Session):
        self.sys_repo = SystemRepository(db)
        self.user_repo = UserRepository(db)

    def get_health(self): return {"status": "ok"}
    def get_all_users(self): return self.user_repo.get_all()
    
class MatchingService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def search_tutors(self, query: str = None):
        # In a real app, apply filters here.
        # For now, we fetch all and let frontend/controller mock the rich data
        return self.user_repo.get_all_tutors()

    def select_tutor(self, student_id: int, tutor_id: int):
        # Logic:
        # 1. Check if tutor exists
        # 2. Create a "Selection Request" in DB (Mocked here)
        # 3. Send Notification to Tutor (Mocked)
        # 4. Return success
        return True