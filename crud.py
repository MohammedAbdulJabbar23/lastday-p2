# crud.py
from tortoise.contrib.fastapi import HTTPNotFoundError
from models import User, Patient, DoctorPatientRelationship

async def get_user_by_username(username: str):
    return await User.filter(username=username).first()

async def create_user(username: str, hashed_password: str, role: str):
    return await User.create(username=username, hashed_password=hashed_password, role=role)

async def get_patient_by_id(patient_id: int):
    return await Patient.filter(id=patient_id).first()

async def create_doctor_patient_relationship(sender, receiver, patient):
    return await DoctorPatientRelationship.create(sender=sender, receiver=receiver, patient=patient)
