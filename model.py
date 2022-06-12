"""Models and database functions for Ratings project."""
from os import environ
from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of ratings website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)

    if email is None:
        email = 'Anonymous'

    def __repr__(self):
        return f'<User: user_id = {self.user_id}, Email = {self.email}>'


class Movie(db.Model):
    """Movie from ratings website."""

    __tablename__ = "movies"

    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String)
    released_at = db.Column(db.DateTime)
    imdb_url = db.Column(db.String)

    def __repr__(self):
        return f'<Movie: movie_id = {self.movie_id}, title = {self.title}>'

class Rating(db.Model):
    """Rating from the rating website."""
    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.movie_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    score = db.Column(db.Integer)

    #Defining the relationship it has with User
    user = db.relationship('User', backref=db.backref('ratings', order_by=rating_id))

    #Defining the relationship it has with Movie
    movie = db.relationship('Movie', backref=db.backref('ratings', order_by=rating_id))



    def __repr__(self):
        """ Helpful in representing what information/columns the rating table/class holds """
        return f'Rating: rating_id = {self.rating_id}, movie_id = {self.movie_id}, user_id = {self.user_id}, score = {self.score}>'

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = environ["POSTGRES_URI"]
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")
