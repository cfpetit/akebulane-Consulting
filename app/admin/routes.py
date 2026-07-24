from flask import render_template, redirect, url_for, abort
from flask_login import login_required, current_user

from app.decorators import admin_required
from app.models import Post
from . import admin_bp
from .forms import PostForm


@admin_bp.route("/admin/post/", methods=['GET', 'POST'], defaults={'post_id': None})
@admin_bp.route("/admin/post/<int:post_id>/", methods=['GET', 'POST'])
@login_required
@admin_required
def post_form(post_id):

    if not current_user.is_admin:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        summary = form.summary.data
        category = form.category.data
        image = form.image.data
        content = form.content.data


        post = Post(user_id=current_user.id, title=title, content=content, summary=summary, category=category, image=image)
        post.save()

        return redirect(url_for('public.index'))
    return render_template("admin/post_form.html", form=form)
