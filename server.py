"""Movie Ratings."""

from os import environ
from jinja2 import StrictUndefined

from flask import Flask, request, render_template, redirect, session, flash, url_for
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


@app.route('/users/<int:user_id>')
def user_details(user_id):
    """ Shows User's details by selected by grabbing user_id from parameters """
    user = User.query.get(user_id)
    return render_template('user.html', user=user)


@app.route('/movies')
def movie_list():
    """ Shows a list of all movies (sorted by title)"""
    movies = Movie.query.order_by(Movie.title).all()
    return render_template('movie_list.html', movies=movies)


@app.route('/movies/<movie_id>', methods=["GET", "POST"])
def movie_detail(movie_id):
    """ 
        Shows movie's details by selecting movie_id through parameters.
        Allows current logged in user to give own rating.
    """
    
    if request.method == "POST":

        score = int(request.form['score'])
        user_id = session['user_id']
        
        if not user_id:
            flash("You're not logged in!")

        rating = Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first()

        if rating:
            rating.score = score
            flash('Rating updated.')
        else:
            rating = Rating(user_id=user_id, movie_id=movie_id, score=score)
            flash("Rating added.")
            db.session.add(rating)

        db.session.commit()

        return redirect(f'/movies/{movie_id}')

    # If not post, then by default is a GET request:
    movie = Movie.query.get(movie_id) # Grabbing movie by movie_id passed in by parameters
    user_id = session.get('user_id')

    if user_id:
        user_rating = Rating.query.filter_by(movie_id=movie_id, user_id=user_id).first()
    else:
        user_rating = None

    return render_template('movie.html', movie=movie, user_rating=user_rating)


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

        user_info = User.query.filter_by(email=email).first()

        if user_info:
            flash(f'{email} is already in use!', "danger")
            return redirect('/register')

        new_user = User(email=email, password=password, age=age, zipcode = zipcode)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Successfully signed up with email: {email}!', "success")
        return redirect('/login')
    
    return render_template('registration.html')
       

@app.route('/login', methods=["GET", "POST"])
def user_login():

    if request.method == "POST":
        email = request.form['login-email']
        password = request.form['login-password']

        user = User.query.filter_by(email=email).first()

        if not user:
            flash('Incorrect email! Check spelling and try again.', "danger")

        elif user.password != password:
            flash('Password is incorrect!!', "danger")

        else:
            session['user_id'] = user.user_id
            flash(f'Logged in!', "info")
            return redirect(f'/user/{user.user_id}')
            

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id')
    flash("Logged out!", "info")
    return redirect('/')


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
