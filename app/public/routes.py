from flask import abort, render_template, current_app, request

from app.models import Post
from . import public_bp

import logging

logger = logging.getLogger(__name__)


@public_bp.route("/")
def index():
    logger.info('Mostrando los posts del blog')

    latest_posts = (
        Post.query
        .order_by(Post.created.desc())
        .limit(3)
        .all()
    )
    return render_template("public/index.html", latest_posts=latest_posts)


@public_bp.route("/p/<string:slug>/")
def show_post(slug):
    post = Post.get_by_slug(slug)
    if post is None:
        abort(404)
    return render_template("public/post_view.html", post=post)
