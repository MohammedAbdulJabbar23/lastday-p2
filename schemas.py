# schemas.py
from pydantic import BaseModel

class UserOut(BaseModel):
    id: int
    username: str
    role: str

class PatientOut(BaseModel):
    id: int
    name: str
    details: str
