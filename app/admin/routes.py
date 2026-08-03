from flask import render_template, redirect, url_for, abort, request, current_app, flash
from flask_login import login_required, current_user

from app.auth.decorators import admin_required
from app.models import Post, SiteContent
from app.auth.models import User
from app.contact.models import ContactMessage
from . import admin_bp
from .forms import PostForm, UserAdminForm, SiteContentForm
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
@admin_required
def delete_contact(id):

    if not current_user.is_admin:
        abort(403)

    message = ContactMessage.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    flash("Message deleted successfully.", "success")
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
    """Actualiza un post existente, incluyendo su imagen"""
    post = Post.get_by_id(post_id)
    if post is None:
        logger.info(f'El post {post_id} no existe')
        abort(404)
    # Initialize the form with existing post data
    form = PostForm(obj=post)
    if form.validate_on_submit():
        # Update text fields
        post.title = form.title.data
        post.summary = form.summary.data
        post.category = form.category.data
        post.content = form.content.data
        # Handle potential new image upload
        file = form.post_image.data
        if file:
            image_name = secure_filename(file.filename)
            images_dir = current_app.config['POST_IMAGES_DIR'] # Ensure this points to media/posts
            os.makedirs(images_dir, exist_ok=True)
            file_path = os.path.join(images_dir, image_name)
            # Save the new file
            file.save(file_path)
            # Optional: Delete the old image file to save space
            if post.image_name:
                old_file_path = os.path.join(images_dir, post.image_name)
                if os.path.exists(old_file_path):
                    try:
                        os.remove(old_file_path)
                    except OSError as e:
                        logger.error(f"Error deleting old image {old_file_path}: {e}")
            # Update the model with the new filename
            post.image_name = image_name

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


@admin_bp.route("/admin/content")
@login_required
@admin_required
def list_content():
    """Muestra todos los textos dinámicos de la página organizados por sección"""
    items = SiteContent.get_all()

    SECTION_ORDER = ["Title", "Services", "Why", "Contacts", "Footer", "Insights", "General"]

    def get_section_category(item):
        key = getattr(item, 'key', '').lower()
        sec = (getattr(item, 'section', '') or '').lower()
        combined = f"{key} {sec}"

        if any(w in combined for w in ['title', 'hero', 'header', 'home']):
            return "Title"
        elif any(w in combined for w in ['service', 'services', 'offering']):
            return "Services"
        elif any(w in combined for w in ['why', 'about', 'choose', 'value', 'mission', 'reason']):
            return "Why"
        elif any(w in combined for w in ['contact', 'email', 'phone', 'address', 'form', 'touch']):
            return "Contacts"
        elif any(w in combined for w in ['footer', 'legal', 'terms', 'privacy', 'cookie', 'copyright']):
            return "Footer"
        elif any(w in combined for w in ['insight', 'insights', 'blog', 'article', 'news']):
            return "Insights"
        else:
            return "General"

    for item in items:
        setattr(item, 'display_section', get_section_category(item))

    items.sort(key=lambda x: (
        SECTION_ORDER.index(x.display_section) if x.display_section in SECTION_ORDER else 99,
        getattr(x, 'key', '')
    ))

    return render_template("admin/content_list.html", items=items)
@admin_bp.route("/admin/content/new/", methods=['GET', 'POST'])
@login_required
@admin_required
def create_content():
    """Crea un nuevo bloque de texto dinámico"""
    form = SiteContentForm()
    if form.validate_on_submit():
        item = SiteContent(
            key=form.key.data,
            description=form.description.data,
            content=form.content.data
        )
        item.save()
        logger.info(f'Nuevo contenido creado: {item.key}')
        flash('Contenido creado exitosamente.')
        return redirect(url_for('admin.list_content'))
    return render_template("admin/content_form.html", form=form)

@admin_bp.route("/admin/content/<int:item_id>/", methods=['GET', 'POST'])
@login_required
@admin_required
def edit_content(item_id):
    """Edita un bloque de texto dinámico existente"""
    item = SiteContent.query.get(item_id)
    if item is None:
        abort(404)
    form = SiteContentForm(obj=item)
    if form.validate_on_submit():
        item.key = form.key.data
        item.description = form.description.data
        item.content = form.content.data
        item.save()
        logger.info(f'Contenido actualizado: {item.key}')
        flash('Contenido actualizado exitosamente.')
        return redirect(url_for('admin.list_content'))
    return render_template("admin/content_form.html", form=form, item=item)

@admin_bp.route("/admin/content/delete/<int:item_id>/", methods=['POST'])
@login_required
@admin_required
def delete_content(item_id):
    """Elimina un bloque de texto dinámico"""
    item = SiteContent.query.get(item_id)
    if item is None:
        abort(404)
    db.session.delete(item)
    db.session.commit()
    flash('Contenido eliminado exitosamente.')
    return redirect(url_for('admin.list_content'))
