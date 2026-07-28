from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    TextAreaField,
    SelectField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    Optional
)


class ContactForm(FlaskForm):

    name = StringField(
        "Full Name",
        validators=[
            DataRequired(),
            Length(max=120)
        ]
    )

    email = StringField(
        "Email Address",
        validators=[
            DataRequired(),
            Email(),
            Length(max=255)
        ]
    )

    company = StringField(
        "Company",
        validators=[
            Optional(),
            Length(max=255)
        ]
    )

    phone = StringField(
        "Phone Number",
        validators=[
            Optional(),
            Length(max=50)
        ]
    )

    subject = SelectField(
        "Subject",
        choices=[
            ("Immigration Support", "Immigration Support"),
            ("Business Consulting", "Business Consulting"),
            ("Market Entry Strategies", "Market Entry Strategies"),
            ("Strategic Partnerships", "Strategic Partnerships"),
            ("General Inquiry", "General Inquiry")
        ],
        validators=[
            DataRequired()
        ]
    )

    message = TextAreaField(
        "Message",
        validators=[
            DataRequired(),
            Length(min=20, max=5000)
        ]
    )

    submit = SubmitField("Send Message")
