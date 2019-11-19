from flask import Blueprint, render_template, redirect, request, url_for, flash, Flask
from models.user import User
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from instagram_web.util.helpers import *


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


# /users/new
@users_blueprint.route('/new', methods=['GET'])
def new():
    #render_template is for you to display that html
    return render_template('users/new.html')

# /users/
@users_blueprint.route('/', methods=['POST']) #use POST request to submit the form
def create():
    # Form data is sent to this route
    # Get form data
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    hashed_password = generate_password_hash(password)
    u = User(name = request.form.get('username') , email = email, password = hashed_password )
    # Save it inside the db
    if u.save():
        flash('Sign up successfully !')
        return redirect(url_for('users.new'))
    else:
        return render_template('users/new.html', errors=u.errors)
   


@users_blueprint.route('/<username>/profile', methods=["GET"]) #to show profile
@login_required
def show(username):
    return render_template('users/show.html', username = current_user.name)


@users_blueprint.route('/', methods=["GET"]) #to show post feed
def index():
    return "USERS HI JOANA"


@users_blueprint.route('/<id>/edit', methods=['GET']) #to edit profile
@login_required
def edit(id):
    user = User.get_by_id(id) # the user we are modifying, based on id from form action

    if current_user.id ==  user.id: #and current_user.is_authenticated: # current_user method is from Flask-Login
        return render_template("users/edit.html", user=user)
    else:
        flash(f"You are not allowed to update {user.name}'s profile","danger")
        return render_template('users/show.html', user=current_user)


@users_blueprint.route('/<id>', methods=['POST']) #to update profile
@login_required
def update(id):
    user = User.get_by_id(id)
    if current_user ==  user: 
        user.name = request.form.get('username')
        user.email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password)        
        user.password = hashed_password
        if user.save():
            flash("Successfully updated", "success")
            return redirect(url_for('users.edit', id=id))
        else:
            flash("Cannot update profile","danger")
            return render_template("users/edit.html", user=user)
    else:
        flash(f"You are not allowed to update {user.name}'s profile","danger")
        return render_template("users/edit.html", user=user)
    
@users_blueprint.route('/<id>/picture', methods=['POST']) #to update profile
@login_required
def update_profile_picture(id):
    # get file from request
    if "user_file" not in request.files:
        flash("Unable to upload file, please try agian", "danger")
        return render_template('users/edit.html')
    file = request.files["user_file"]
    # if no file in request
    # if not file:
    #     error = "Please Try Agian!"
    #     return render_template('users/edit.html', error=error)
    # if file in request
    file.filename = secure_filename(file.filename)
    output = upload_file_to_s3(file) #upload_file_to_s3(file), this func is import from helpers.py
    # if no image link get from upload function
    if not output:
        flash("Unable to upload file, please try agian", "danger")
        return render_template('users/edit.html')
    # if img link return, means upload successful
    else:
        # get current_user
        user = User.update(profile_picture = file.filename).where(User.id == current_user.id)
        # save profile image link in user class
        user.execute()
        # print(output)
        flash("Profile picture updated", "success")
        return redirect(url_for('users.edit', id=id))