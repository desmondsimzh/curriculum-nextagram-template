from flask import Blueprint, render_template, redirect


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
    
    # Create a new user from that data

    # Use pw to create a new instance of a user
    # Save it inside the db
    username = request.form.get('username')


    print(username)

    return redirect(url_for('users.new'))
   


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
