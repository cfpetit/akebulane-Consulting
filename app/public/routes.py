from flask import abort, render_template, current_app, request

from app.models import Post
from . import public_bp

import logging

logger = logging.getLogger(__name__)


@public_bp.route("/")
def index():
    logger.info('Mostrando los posts del blog')
    page = int(request.args.get('page', 1))
    per_page = current_app.config['ITEMS_PER_PAGE']
    posts_pagination = Post.all_paginated(page, per_page)
    return render_template("public/index.html", posts_pagination=posts_pagination)


@public_bp.route("/p/<string:slug>/")
def show_post(slug):
    post = Post.get_by_slug(slug)
    if post is None:
        abort(404)
    return render_template("public/post_view.html", post=post)
