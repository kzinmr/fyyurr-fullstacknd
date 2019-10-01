# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

# import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, flash, redirect, url_for  # Response
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler

from forms import ShowForm, VenueForm, ArtistForm
from models import init_db, Venue, Artist, Show
import datetime
from collections import defaultdict
import sys

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object("config")
# TODO: connect to a local postgresql database
db = init_db(app)

# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


def format_datetime(value, format="medium"):
    date = dateutil.parser.parse(value)
    if format == "full":
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == "medium":
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters["datetime"] = format_datetime

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.route("/")
def index():
    return render_template("pages/home.html")


#  Venues
#  ----------------------------------------------------------------


@app.route("/venues")
def venues():
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    nowtime = datetime.datetime.utcnow()
    id2num = defaultdict(int)
    upcoming_shows = dict(
        db.session.query(Venue.id, db.func.count(Show.id))
        .join(Show, Show.venue_id == Venue.id)
        .filter(Show.start_time > nowtime)
        .group_by(Venue.id)
        .all()
    )
    id2num.update(upcoming_shows)

    dd = defaultdict(list)
    for u in db.session.query(Venue.id, Venue.name, Venue.city, Venue.state).all():
        dd[(u.city, u.state)].append(
            {"id": u.id, "name": u.name, "num_upcoming_shows": id2num[u.id]}
        )
    data = [
        {"city": city, "state": state, "venues": venues}
        for (city, state), venues in dd.items()
    ]

    return render_template("pages/venues.html", areas=data)


@app.route("/venues/search", methods=["POST"])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    nowtime = datetime.datetime.utcnow()
    id2num = defaultdict(int)
    upcoming_shows = dict(
        db.session.query(Venue.id, db.func.count(Show.id))
        .join(Show, Show.venue_id == Venue.id)
        .filter(Show.start_time > nowtime)
        .group_by(Venue.id)
        .all()
    )
    id2num.update(upcoming_shows)

    search_term = request.form.get("search_term", "")
    data = (
        db.session.query(Venue.id, Venue.name)
        .filter(Venue.name.ilike(f"%{search_term}%"))
        .all()
    )
    response = {
        "count": len(data),
        "data": [
            {"id": r.id, "name": r.name, "num_upcoming_shows": id2num[r.id]}
            for r in data
        ],
    }
    return render_template(
        "pages/search_venues.html", results=response, search_term=search_term
    )


@app.route("/venues/<int:venue_id>")
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    nowtime = datetime.datetime.utcnow()
    show_artist = (
        db.session.query(Show, Artist).join(Artist, Artist.id == Show.artist_id).all()
    )
    showid2entry = {show.id: (show.start_time, artist) for show, artist in show_artist}
    venue_show = (
        db.session.query(Venue, Show).outerjoin(Show, Show.venue_id == Venue.id).all()
    )
    data_dict = defaultdict(list)
    for venue, show in venue_show:
        if venue.id not in data_dict:
            venue_d = venue.__dict__
            if "_sa_instance_state" in venue_d:
                del venue_d["_sa_instance_state"]
            data_dict[venue.id] = venue_d
            d = data_dict[venue.id]
            d["past_shows"] = []
            d["upcoming_shows"] = []
            d["past_shows_count"] = 0
            d["upcoming_shows_count"] = 0
        else:
            d = data_dict[venue.id]

        if show is not None:
            start_time, artist = showid2entry[show.id]
            show_d = {
                "artist_id": artist.id,
                "artist_name": artist.name,
                "artist_image_link": artist.image_link,
                "start_time": start_time.isoformat(),
            }
            if start_time > nowtime:
                d["upcoming_shows"].append(show_d)
                d["upcoming_shows_count"] += 1
            else:
                d["past_shows"].append(show_d)
                d["past_shows_count"] += 1
    data = data_dict[venue_id]

    return render_template("pages/show_venue.html", venue=data)


#  Create Venue
#  ----------------------------------------------------------------


@app.route("/venues/create", methods=["GET"])
def create_venue_form():
    form = VenueForm()
    return render_template("forms/new_venue.html", form=form)


@app.route("/venues/create", methods=["POST"])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO(?): modify data to be the data object returned from db insertion
    error = False
    try:
        formdata = {k: v[0] if k != "genres" else v for k, v in request.form.lists()}
        venue = Venue(**formdata)
        db.session.add(venue)
        db.session.commit()
    except Exception:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if not error:
        # on successful db insert, flash success
        flash("Venue " + request.form["name"] + " was successfully listed!")
    else:
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        flash(
            "An error occurred. Venue " + request.form["name"] + " could not be listed."
        )
        # abort(400)

    return render_template("pages/home.html")


@app.route("/venues/<venue_id>", methods=["DELETE"])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    error = False
    try:
        venue = Venue.query.get(venue_id)
        db.session.delete(venue)
        db.session.commit()
    except Exception:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    if not error:
        # on successful db insert, flash success
        flash("Venue " + venue.name + " has successfully been deleted!")
    else:
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        flash("An error occurred. Venue could not be deleted.")

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage

    # FIXME: No redirect occurs
    return render_template("pages/home.html")


#  Artists
#  ----------------------------------------------------------------
@app.route("/artists")
def artists():
    # TODO: replace with real data returned from querying the database
    data = db.session.query(Artist.id, Artist.name).all()
    return render_template("pages/artists.html", artists=data)


@app.route("/artists/search", methods=["POST"])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    nowtime = datetime.datetime.utcnow()
    id2num = defaultdict(int)
    upcoming_shows = dict(
        db.session.query(Artist.id, db.func.count(Show.id))
        .join(Show, Show.artist_id == Artist.id)
        .filter(Show.start_time > nowtime)
        .group_by(Artist.id)
        .all()
    )
    id2num.update(upcoming_shows)

    search_term = request.form.get("search_term", "")
    data = (
        db.session.query(Artist.id, Artist.name)
        .filter(Artist.name.ilike(f"%{search_term}%"))
        .all()
    )
    response = {
        "count": len(data),
        "data": [
            {"id": r.id, "name": r.name, "num_upcoming_shows": id2num[r.id]}
            for r in data
        ],
    }
    return render_template(
        "pages/search_artists.html", results=response, search_term=search_term
    )


@app.route("/artists/<int:artist_id>")
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    nowtime = datetime.datetime.utcnow()
    show_venue = (
        db.session.query(Show, Venue).join(Venue, Venue.id == Show.venue_id).all()
    )
    showid2entry = {show.id: (show.start_time, venue) for show, venue in show_venue}
    artist_show = (
        db.session.query(Artist, Show)
        .outerjoin(Show, Show.artist_id == Artist.id)
        .all()
    )
    data_dict = defaultdict(list)
    for artist, show in artist_show:
        if artist.id not in data_dict:
            artist_d = artist.__dict__
            if "_sa_instance_state" in artist_d:
                del artist_d["_sa_instance_state"]
            data_dict[artist.id] = artist_d
            d = data_dict[artist.id]
            d["past_shows"] = []
            d["upcoming_shows"] = []
            d["past_shows_count"] = 0
            d["upcoming_shows_count"] = 0
        else:
            d = data_dict[artist.id]

        if show is not None:
            start_time, venue = showid2entry[show.id]
            show_d = {
                "venue_id": venue.id,
                "venue_name": venue.name,
                "venue_image_link": venue.image_link,
                "start_time": start_time.isoformat(),
            }
            if start_time > nowtime:
                d["upcoming_shows"].append(show_d)
                d["upcoming_shows_count"] += 1
            else:
                d["past_shows"].append(show_d)
                d["past_shows_count"] += 1
    data = data_dict[artist_id]

    return render_template("pages/show_artist.html", artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route("/artists/<int:artist_id>/edit", methods=["GET"])
def edit_artist(artist_id):
    artist = Artist.query.get(artist_id)
    form = ArtistForm(obj=artist)
    if form.validate():
        form.populate_obj(artist)
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template("forms/edit_artist.html", form=form, artist=artist)


@app.route("/artists/<int:artist_id>/edit", methods=["POST"])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    artist = Artist.query.get(artist_id)
    error = False
    try:
        formdata = {k: v[0] if k != "genres" else v for k, v in request.form.lists()}
        for k, v in formdata.items():
            setattr(artist, k, v)
        db.session.add(artist)
        db.session.commit()
    except Exception:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if not error:
        # on successful db insert, flash success
        flash("Artist " + request.form["name"] + " was successfully updated!")
    else:
        flash(
            "An error occurred. Artist "
            + request.form["name"]
            + " could not be updated."
        )
        # abort(400)
    return redirect(url_for("show_artist", artist_id=artist_id))


@app.route("/venues/<int:venue_id>/edit", methods=["GET"])
def edit_venue(venue_id):
    venue = Venue.query.get(venue_id)
    form = VenueForm(obj=venue)
    if form.validate():
        form.populate_obj(venue)
    # TODO: populate form with values from venue with ID <venue_id>

    return render_template("forms/edit_venue.html", form=form, venue=venue)


@app.route("/venues/<int:venue_id>/edit", methods=["POST"])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    venue = Venue.query.get(venue_id)
    error = False
    try:
        formdata = {k: v[0] if k != "genres" else v for k, v in request.form.lists()}
        for k, v in formdata.items():
            setattr(venue, k, v)
        db.session.add(venue)
        db.session.commit()
    except Exception:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if not error:
        # on successful db insert, flash success
        flash("Venue " + request.form["name"] + " was successfully updated!")
    else:
        flash(
            "An error occurred. Venue "
            + request.form["name"]
            + " could not be updated."
        )
        # abort(400)
    return redirect(url_for("show_venue", venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------


@app.route("/artists/create", methods=["GET"])
def create_artist_form():
    form = ArtistForm()
    return render_template("forms/new_artist.html", form=form)


@app.route("/artists/create", methods=["POST"])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO(?): modify data to be the data object returned from db insertion
    error = False
    try:
        formdata = {k: v[0] if k != "genres" else v for k, v in request.form.lists()}
        artist = Artist(**formdata)
        db.session.add(artist)
        db.session.commit()
    except Exception:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if not error:
        # on successful db insert, flash success
        flash("Artist " + request.form["name"] + " was successfully listed!")
    else:
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
        flash(
            "An error occurred. Artist "
            + request.form["name"]
            + " could not be listed."
        )
        # abort(400)

    return render_template("pages/home.html")


#  Shows
#  ----------------------------------------------------------------


@app.route("/shows")
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    show_venue = (
        db.session.query(Show, Venue).join(Venue, Venue.id == Show.venue_id).all()
    )
    showid2entry = {show.id: (show.start_time, venue) for show, venue in show_venue}
    show_artist = (
        db.session.query(Show, Artist).join(Artist, Artist.id == Show.artist_id).all()
    )

    data = []
    for show, artist in show_artist:
        start_time, venue = showid2entry[show.id]
        data.append(
            {
                "venue_id": venue.id,
                "venue_name": venue.name,
                "artist_id": artist.id,
                "artist_name": artist.name,
                "artist_image_link": artist.image_link,
                "start_time": start_time.isoformat(),
            }
        )

    return render_template("pages/shows.html", shows=data)


@app.route("/shows/create")
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template("forms/new_show.html", form=form)


@app.route("/shows/create", methods=["POST"])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead

    error = False
    try:
        formdata = request.form.to_dict()
        show = Show(**formdata)
        db.session.add(show)
        db.session.commit()
    except Exception:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if not error:
        # on successful db insert, flash success
        flash("Show was successfully listed!")
    else:
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Show could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        flash("An error occurred. Show could not be listed.")
        # abort(400)

    return render_template("pages/home.html")


@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("errors/500.html"), 500


if not app.debug:
    file_handler = FileHandler("error.log")
    file_handler.setFormatter(
        Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info("errors")

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == "__main__":
    app.run()

# Or specify port manually:
"""
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
"""
