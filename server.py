"""Movie Ratings."""

from os import environ
from jinja2 import StrictUndefined

from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Movie, Rating, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = environ["SERVER_SECRET_KEY"]

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """ Homepage """
    return render_template('home.html')


@app.route('/users')
def user_list():
    """ Show a list of all users """
    users = User.query.all()
    return render_template('user_list.html', users=users)


@app.route('/movies')
def movie_list():
    pass

@app.route('/register', methods=["GET", "POST"])
def register_user():
    """ Provide a page with a form for a user to register """


    if request.method == "POST":
        # User filled out forms, making this a post request.
        # Process the form info & redirect
        email =  request.form['register-email']
        password = request.form['register-pass']
        age = request.form['age']
        zipcode = request.form['zipcode']

        if bool(User.query.filter_by(email = email).all()):
            return flash(f'{email} is already in use!')
        else:
            new_user = User(email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash(f'Hi { email }, you are logged in!')
            return redirect('home.html')
    
    return render_template('registration.html')
    



@app.route('/login', methods=["GET"])
def show_login():
    """ Provide a page with a form for a user to login """
    return render_template('login.html')
   

@app.route('/login', )
def process_login():
     return redirect('home.html')



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
