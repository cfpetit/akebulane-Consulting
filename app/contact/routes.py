from flask import (
    render_template,
    redirect,
    url_for,
    flash
)

from . import contact_bp
from .forms import ContactForm
from .models import ContactMessage





@contact_bp.route("/contact", methods=["GET", "POST"])
def contact():

    form = ContactForm()

    if form.validate_on_submit():

        message = ContactMessage(
            name=form.name.data,
            email=form.email.data,
            company=form.company.data,
            phone=form.phone.data,
            subject=form.subject.data,
            message=form.message.data
        )

        message.save()

        flash(
            "Your message has been sent successfully. We will contact you as soon as possible.",
            "success"
        )

        return redirect(url_for("contact.contact_success"))

    return render_template(
        "contact/contact.html",
        form=form
    )


@contact_bp.route("/contact/success")
def contact_success():

    return render_template(
        "contact/contact_success.html"
    )


@contact_bp.route("/admin/contact-messages")
def admin_messages():

    messages = ContactMessage.get_all()

    return render_template(
        "contact/admin_contacts.html",
        messages=messages
    )


@contact_bp.route("/admin/contact-messages/<int:message_id>")
def mark_as_read(message_id):

    message = ContactMessage.get_by_id(message_id)

    if message:

        message.is_read = True
        message.save()

    return redirect(
        url_for("contact.admin_messages")
    )


@contact_bp.route("/admin/contact-messages/delete/<int:message_id>")
def delete_message(message_id):

    message = ContactMessage.get_by_id(message_id)

    if message:

        message.delete()

        flash(
            "Message deleted successfully.",
            "success"
        )

    return redirect(
        url_for("contact.admin_messages")
    )
