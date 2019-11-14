from flask import Blueprint, render_template, redirect, request, url_for, flash, Flask,session
from models.user import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash


sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')


@sessions_blueprint.route('/new', methods=['GET'])
def new():
    #make get request to display 
    return render_template('sessions/new.html')


@sessions_blueprint.route('/', methods=['POST'])
def create():
    # get username/email and password
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.get_or_none(name=username)
    error = None
    if user:
        # if has user
        result = check_password_hash(user.password, password)
        
        if result:
            # loggin user
            # session["user_id"] = user.id
            login_user(user)
            flash('Logged in successfully !')   
            return redirect(url_for('users.edit', id=current_user))
        else:
            #flash error message :wrong password
            error = "Incorrect password! Please Try Agian!"
            return render_template('sessions/new.html', error = error)
    else:
        # if no user
        # flash no user found
        error = "User not found! Please Try Agian!"
        return render_template('sessions/new.html', error = error)
        

@sessions_blueprint.route('/delete')
@login_required
def delete():
    # remove the username from the session if it's there
    # session.pop('user_id', None)
    logout_user()
    return redirect(url_for('sessions.new'))