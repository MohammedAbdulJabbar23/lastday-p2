# main.py
from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from tortoise.contrib.fastapi import register_tortoise
from typing import List
from models import User, Patient
from schemas import UserOut, PatientOut
from crud import get_user_by_username, create_user, get_patient_by_id, create_doctor_patient_relationship
from security import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_current_user, get_password_hash

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/register", response_model=UserOut)
async def register_user(username: str, password: str, role: str):
    hashed_password = get_password_hash(password)
    user = await create_user(username=username, hashed_password=hashed_password, role=role)
    return UserOut(id=user.id, username=user.username, role=user.role)

@app.post("/send-patient-info/{receiver_username}")
async def send_patient_info(receiver_username: str, patient_id: int, current_user: User = Depends(get_current_user)):
    if current_user.role != "Doctor":
        raise HTTPException(status_code=403, detail="Only doctors can send patient information")
    
    receiver = await get_user_by_username(receiver_username)
    if not receiver or receiver.role != "Doctor":
        raise HTTPException(status_code=404, detail="Receiver doctor not found")
    
    patient = await get_patient_by_id(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    await create_doctor_patient_relationship(sender=current_user, receiver=receiver, patient=patient)

@app.get("/received-patients", response_model=List[PatientOut])
async def get_received_patients(current_user: User = Depends(get_current_user)):
    if current_user.role != "Doctor":
        raise HTTPException(status_code=403, detail="Only doctors can view received patients")
    
    received_patients = await Patient.filter(related_doctors__receiver=current_user)
    return received_patients

register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
)
