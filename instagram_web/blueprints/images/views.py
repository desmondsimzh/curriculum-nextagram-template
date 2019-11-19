from flask import Blueprint, render_template, redirect, request, url_for, flash, Flask
from models.image import Image
from models.user import User
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from instagram_web.util.helpers import *


images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')



@images_blueprint.route('/<id>/new', methods=['GET'])
@login_required
def new(id):
    return render_template('images/new.html')
    
@images_blueprint.route('/<id>/picture', methods=['POST']) #to update profile
@login_required
def create_picture(id):
    # get file from request
    file = request.files["img_file"]
    # if no file in request
    if not file:
        flash("Please choose a file.", 'danger')
        return render_template('images/new.html')
    # if file in request
    file.filename = secure_filename(file.filename)
    output = upload_file_to_s3(file)
    # if no image link get from upload function
    if not output:
        flash("Unable to upload file, please try agian", "danger")
        return render_template('images/new.html')
    # if img link return, means uploaod successful
    else:
        # get current_user
        user = User.get_or_none(User.id == id)
        image = Image.create(img_file_name = file.filename, user_id = user)
        # save profile image link in user class
        image.save()
        flash("Image uploaded successfully!", "success")
        return redirect(url_for('images.new', id=id))

@images_blueprint.route('/<id>/delete') #to update profile
@login_required
def delete_picture(id):
    delete_image = Image.delete().where(Image.id == id )
    delete_image.execute()
    flash("Image has been deleted!", "primary")
    return redirect(url_for('home'))
