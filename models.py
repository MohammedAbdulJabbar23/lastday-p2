# models.py
from tortoise.models import Model
from tortoise import fields

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    hashed_password = fields.CharField(max_length=100)
    role = fields.CharField(max_length=20)

class Patient(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    details = fields.TextField()

class DoctorPatientRelationship(Model):
    id = fields.IntField(pk=True)
    sender = fields.ForeignKeyField("models.User", related_name="sent_patients")
    receiver = fields.ForeignKeyField("models.User", related_name="received_patients")
    patient = fields.ForeignKeyField("models.Patient", related_name="related_doctors")
