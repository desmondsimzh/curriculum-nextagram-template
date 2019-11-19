from models.base_model import BaseModel
from models.user import User
from models.image import Image
from flask_login import UserMixin
from playhouse.hybrid import hybrid_property
from config import Config
import peewee as pw


class Donate(UserMixin, BaseModel):
    user_id = pw.ForeignKeyField(User, backref='donations')
    image_id = pw.ForeignKeyField(Image, backref='donations')
    donate_amount = pw.CharField(null=True)

    def is_authenticated():
        return True