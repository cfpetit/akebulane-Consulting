from flask import render_template, redirect, url_for, abort, request, current_app, flash
from flask_login import login_required, current_user

from app.auth.decorators import admin_required
from app.models import Post
from app.auth.models import User
from app.contact.models import ContactMessage
from . import admin_bp
from .forms import PostForm, UserAdminForm
from werkzeug.utils import secure_filename
import logging
import os
from app import db

logger = logging.getLogger(__name__)

@admin_bp.route("/admin/")
@login_required
@admin_required
def index():
    return render_template("admin/index.html")


@admin_bp.route("/contacts")
@login_required
def contacts():

    if not current_user.is_admin:
        abort(403)

    messages = ContactMessage.get_all()

    return render_template(
        "contact/admin_contacts.html",
        messages=messages
    )


@admin_bp.route("/contacts/<int:id>")
@login_required
def contact_detail(id):

    if not current_user.is_admin:
        abort(403)

    message = ContactMessage.get_by_id(id)

    if not message:
        abort(404)

    message.is_read = True
    db.session.commit()

    return render_template(
        "admin/contact_details.html",
        message=message
    )


@admin_bp.route("/contacts/delete/<int:id>", methods=["POST"])
@login_required
def delete_contact(id):

    if not current_user.is_admin:
        abort(403)

    message = ContactMessage.get_by_id(id)

    if message:
        message.delete()

    flash("Message deleted successfully.")

    return redirect(url_for("admin.contacts"))

@admin_bp.route("/admin/users")
@login_required
@admin_required
def list_users():
    users = User.get_all()
    return render_template("admin/users.html", users=users)

@admin_bp.route("/admin/user/<int:user_id>/", methods=['GET', 'POST'])
@login_required
@admin_required
def update_user_form(user_id):
    user = User.get_by_id(user_id)
    if user is None:
        logger.info(f'El usuario {user_id} no existe')
        abort(404)

    form = UserAdminForm(obj=user)
    if form.validate_on_submit():
        user.is_admin = form.is_admin.data
        user.save()
        logger.info(f'Guardando el usuario {user_id}')
        return redirect(url_for('admin.list_users'))
    return render_template("admin/user_form.html", form=form, user=user)

@admin_bp.route("/admin/user/delete/<int:user_id>/", methods=['POST', ])
@login_required
@admin_required
def delete_user(user_id):
    logger.info(f'Se va a eliminar al usuario {user_id}')
    user = User.get_by_id(user_id)
    if user is None:
        logger.info(f'El usuario {user_id} no existe')
        abort(404)
    user.delete()
    logger.info(f'El usuario {user_id} ha sido eliminado')
    return redirect(url_for('admin.list_users'))

@admin_bp.route("/admin/posts")
@login_required
@admin_required
def list_posts():
    posts = Post.get_all()
    return render_template("admin/posts.html", posts=posts)

@admin_bp.route("/admin/post/", methods=['GET', 'POST'])
@login_required
@admin_required
def post_form():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        summary = form.summary.data
        category = form.category.data
        file = form.post_image.data
        image_name = None
        if file:
           image_name = secure_filename(file.filename)
           images_dir = current_app.config['POST_IMAGES_DIR']
           os.makedirs(images_dir, exist_ok=True)
           file_path = os.path.join(images_dir, image_name)
           file.save(file_path)
        content = form.content.data
        post = Post(user_id=current_user.id, title=title, content=content, summary=summary, category=category)
        post.image_name = image_name
        post.save()
        return redirect(url_for('admin.list_posts'))
    return render_template("admin/post_form.html", form=form)

@admin_bp.route("/admin/post/<int:post_id>/", methods=['GET', 'POST'])
@login_required
@admin_required
def update_post_form(post_id):
    """Actualiza un post existente"""
    post = Post.get_by_id(post_id)
    if post is None:
        logger.info(f'El post {post_id} no existe')
        abort(404)
    # Crea un formulario inicializando los campos con
    # los valores del post.
    form = PostForm(obj=post)
    if form.validate_on_submit():
        # Actualiza los campos del post existente
        post.title = form.title.data
        post.content = form.content.data
        post.save()
        logger.info(f'Guardando el post {post_id}')
        return redirect(url_for('admin.list_posts'))
    return render_template("admin/post_form.html", form=form, post=post)

from flask import abort

@admin_bp.route("/admin/post/delete/<int:post_id>/", methods=['POST', ])
@login_required
@admin_required
def delete_post(post_id):
    logger.info(f'Se va a eliminar el post {post_id}')
    post = Post.get_by_id(post_id)
    if post is None:
        logger.info(f'El post {post_id} no existe')
        abort(404)
    post.delete()
    logger.info(f'El post {post_id} ha sido eliminado')
    return redirect(url_for('admin.list_posts'))
