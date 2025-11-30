from datetime import datetime, timedelta

class ScheduleDomain:
    """
    Contains business logic for scheduling.
    Does NOT interact with DB directly.
    """
    
    @staticmethod
    def validate_slot_time(start_time: datetime) -> datetime:
        """Ensures slot is in the future and calculates end time"""
        if start_time < datetime.now():
            raise ValueError("Cannot schedule slot in the past")
        return start_time + timedelta(hours=1)

    @staticmethod
    def check_conflicts(new_start: datetime, existing_slots: list):
        # Pure logic to check if new_start overlaps with existing list
        # Implementation omitted for brevity
        pass

class MatchingDomain:
    """
    Logic for matching students to tutors (Advanced Feature)
    """
    pass