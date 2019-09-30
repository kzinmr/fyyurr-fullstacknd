from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    SelectMultipleField,
    DateTimeField,
    BooleanField,
)
from wtforms.validators import DataRequired, AnyOf, URL


class ShowForm(FlaskForm):
    artist_id = StringField("artist_id", validators=[DataRequired()])
    venue_id = StringField("venue_id", validators=[DataRequired()])
    start_time = DateTimeField(
        "start_time", validators=[DataRequired()], default=datetime.today()
    )


class VenueForm(FlaskForm):
    state_choices = [
        "AL",
        "AK",
        "AZ",
        "AR",
        "CA",
        "CO",
        "CT",
        "DE",
        "DC",
        "FL",
        "GA",
        "HI",
        "ID",
        "IL",
        "IN",
        "IA",
        "KS",
        "KY",
        "LA",
        "ME",
        "MT",
        "NE",
        "NV",
        "NH",
        "NJ",
        "NM",
        "NY",
        "NC",
        "ND",
        "OH",
        "OK",
        "OR",
        "MD",
        "MA",
        "MI",
        "MN",
        "MS",
        "MO",
        "PA",
        "RI",
        "SC",
        "SD",
        "TN",
        "TX",
        "UT",
        "VT",
        "VA",
        "WA",
        "WV",
        "WI",
        "WY",
    ]
    genres_choices = [
        "Alternative",
        "Blues",
        "Classical",
        "Country",
        "Electronic",
        "Folk",
        "Funk",
        "Hip-Hop",
        "Heavy Metal",
        "Instrumental",
        "Jazz",
        "Musical Theatre",
        "Pop",
        "Punk",
        "R&B",
        "Reggae",
        "Rock n Roll",
        "Soul",
        "Other",
    ]
    name = StringField("name", validators=[DataRequired()])
    city = StringField("city", validators=[DataRequired()])
    state = SelectField(
        "state",
        validators=[DataRequired(), AnyOf(state_choices)],
        choices=[(c, c) for c in state_choices],
    )
    address = StringField("address", validators=[DataRequired()])
    phone = StringField("phone")
    image_link = StringField("image_link")
    genres = SelectMultipleField(
        # TODO implement enum restriction
        "genres",
        validators=[DataRequired(), AnyOf(genres_choices)],
        choices=[(c, c) for c in genres_choices],
    )
    facebook_link = StringField("facebook_link", validators=[URL()])
    website = StringField("website", validators=[URL()])
    seeking_talent = BooleanField("seeking_talent")
    seeking_description = StringField("seeking_description")


class ArtistForm(FlaskForm):
    state_choices = [
        "AL",
        "AK",
        "AZ",
        "AR",
        "CA",
        "CO",
        "CT",
        "DE",
        "DC",
        "FL",
        "GA",
        "HI",
        "ID",
        "IL",
        "IN",
        "IA",
        "KS",
        "KY",
        "LA",
        "ME",
        "MT",
        "NE",
        "NV",
        "NH",
        "NJ",
        "NM",
        "NY",
        "NC",
        "ND",
        "OH",
        "OK",
        "OR",
        "MD",
        "MA",
        "MI",
        "MN",
        "MS",
        "MO",
        "PA",
        "RI",
        "SC",
        "SD",
        "TN",
        "TX",
        "UT",
        "VT",
        "VA",
        "WA",
        "WV",
        "WI",
        "WY",
    ]
    genres_choices = [
        "Alternative",
        "Blues",
        "Classical",
        "Country",
        "Electronic",
        "Folk",
        "Funk",
        "Hip-Hop",
        "Heavy Metal",
        "Instrumental",
        "Jazz",
        "Musical Theatre",
        "Pop",
        "Punk",
        "R&B",
        "Reggae",
        "Rock n Roll",
        "Soul",
        "Other",
    ]
    name = StringField("name", validators=[DataRequired()])
    city = StringField("city", validators=[DataRequired()])
    state = SelectField(
        "state",
        validators=[DataRequired(), AnyOf(state_choices)],
        choices=[(c, c) for c in state_choices],
    )
    phone = StringField(
        # TODO(?) implement validation logic for state
        "phone"
    )
    image_link = StringField("image_link")
    genres = SelectMultipleField(
        # TODO implement enum restriction
        "genres",
        validators=[DataRequired(), AnyOf(genres_choices)],
        choices=[(c, c) for c in genres_choices],
    )
    facebook_link = StringField(
        # TODO(?) implement enum restriction
        "facebook_link",
        validators=[URL()],
    )
    website = StringField("website", validators=[URL()])
    seeking_venue = BooleanField("seeking_venue")
    seeking_description = StringField("seeking_description")


# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM
