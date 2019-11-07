from models.base_model import BaseModel
from werkzeug.security import generate_password_hash
import peewee as pw


class User(BaseModel):
    name = pw.CharField(unique=False)
    password = pw.CharField()
    email = pw.CharField(unique=True)
