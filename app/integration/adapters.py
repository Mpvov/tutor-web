# Simulates the SSOAdapter component in the diagram
class SSOAdapter:
    def authenticate(self, mssv: str, password: str) -> bool:
        # In a real scenario, this would send a REST/SOAP request to HCMUT SSO
        # For now, we return True to allow the AuthService to proceed with local DB check
        # or implement mock logic here.
        return True

# Simulates DataCoreAdapter
class DataCoreAdapter:
    def sync_user_data(self, mssv: str):
        # Mocking fetching data from HCMUT_DATACORE
        return {"ho_ten": "Nguyen Van A (Synced)", "major": "Computer Science"}

# Simulates LibraryAdapter
class LibraryAdapter:
    def get_documents(self, subject_code: str):
        return ["Book A", "Slide B"]