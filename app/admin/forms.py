from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    TextAreaField,
    BooleanField,
    SelectField
)
from wtforms.validators import DataRequired, Length

POST_CATEGORIES = [
    ("consulting", "Consulting"),
    ("immigration", "Immigration"),
    ("news", "News"),
    ("events", "Events"),
]


class PostForm(FlaskForm):

    title = StringField(
        "Title",
        validators=[
            DataRequired(),
            Length(max=150)
        ]
    )

    summary = TextAreaField(
        "Summary",
        validators=[
            DataRequired(),
            Length(max=300)
        ]
    )

    category = SelectField(
        "Category",
        choices=POST_CATEGORIES,
        validators=[DataRequired()]
    )

    image = StringField(
        "Image",
        validators=[
            Length(max=200)
        ]
    )

    content = TextAreaField(
        "Content",
        validators=[DataRequired()]
    )

    submit = SubmitField("Save Post")

class UserAdminForm(FlaskForm):
    is_admin = BooleanField('Administrador')
    submit = SubmitField('Guardar')