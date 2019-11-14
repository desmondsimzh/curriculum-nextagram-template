from flask import Blueprint, render_template, redirect, request, url_for, flash, Flask
from models.image import Image
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from instagram_web.util.helpers import *


images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')



@images_blueprint.route('/new', methods=['GET'])
@login_required
def new():
    return render_template('images/new.html')
    
@images_blueprint.route('/<id>/picture', methods=['POST']) #to update profile
@login_required
def update_picture(id):
    # get file from request
    file = request.files["user_file"]
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
        user = User.update(profile_picture = output).where
        # save profile image link in user class
        user.execute()
        # print(output)
        flash("Profile picture updated", "success")
        return redirect(url_for('user.show', username=current_user.name))

