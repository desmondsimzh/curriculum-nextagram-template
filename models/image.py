from models.base_model import BaseModel
from models.user import User
from flask_login import UserMixin
from playhouse.hybrid import hybrid_property
from config import Config
import peewee as pw


class Image(UserMixin, BaseModel):
    user_id = pw.ForeignKeyField(User, backref='images')
    img_file_name = pw.CharField(null=True)

    
    @hybrid_property
    def user_images_url(self):
        return Config.S3_LOCATION + self.img_file_name

    def is_authenticated():
        return True

