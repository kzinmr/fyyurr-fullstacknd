from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()


def init_db(app):
    db.init_app(app)
    Migrate(app, db)


class Venue(db.Model):
    __tablename__ = "Venue"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String(120), nullable=True)
    seeking_talent = db.Column(db.Boolean, nullable=True)
    seeking_description = db.Column(db.String(120), nullable=True)

    shows = db.relationship(
        "Show", backref="venue", cascade="all, delete-orphan", lazy=True
    )

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = "Artist"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(120), nullable=True)
    image_link = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)

    website = db.Column(db.String(120), nullable=True)
    seeking_venue = db.Column(db.Boolean, nullable=True)
    seeking_description = db.Column(db.String(120), nullable=True)

    shows = db.relationship(
        "Show", backref="artist", cascade="all, delete-orphan", lazy=True
    )

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Show(db.Model):
    __tablename__ = "Show"

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DATETIME(), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey("Venue.id"), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey("Artist.id"), nullable=False)


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
