import datetime

from app import db


class ContactMessage(db.Model):

    __tablename__ = "contact_message"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), nullable=False)

    email = db.Column(db.String(255), nullable=False)

    company = db.Column(db.String(255))

    phone = db.Column(db.String(50))

    subject = db.Column(db.String(255), nullable=False)

    message = db.Column(db.Text, nullable=False)

    created = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )

    is_read = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    def __repr__(self):
        return f"<ContactMessage {self.email}>"

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_id(message_id):
        return ContactMessage.query.get(message_id)

    @staticmethod
    def get_all():
        return (
            ContactMessage.query
            .order_by(ContactMessage.created.desc())
            .all()
        )

    @staticmethod
    def get_unread():
        return (
            ContactMessage.query
            .filter_by(is_read=False)
            .order_by(ContactMessage.created.desc())
            .all()
        )
