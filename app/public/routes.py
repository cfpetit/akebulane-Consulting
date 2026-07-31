from flask import abort, render_template, current_app, request

from app.models import Post, SiteContent
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

    content_items = SiteContent.get_all()
    site_texts = {item.key: item.content for item in content_items}
    return render_template("public/index.html", latest_posts=latest_posts, texts=site_texts)


@public_bp.route("/p/<string:slug>/")
def show_post(slug):
    post = Post.get_by_slug(slug)
    if post is None:
        abort(404)
    return render_template("public/post_view.html", post=post)

@public_bp.route("/services/immigration-support")
def immigration_support():
    """Renders the Immigration Support service detail page."""
    return render_template("public/services/immigration.html")

@public_bp.route("/services/business-consulting")
def business_consulting():
    """Renders the Business Consulting service detail page."""
    return render_template("public/services/business_consulting.html")

@public_bp.route("/services/market-entry")
def market_entry():
    """Renders the Market Entry Strategies service detail page."""
    return render_template("public/services/market_entry.html")

@public_bp.route("/services/strategic-partnerships")
def strategic_partnerships():
    """Renders the Strategic Partnerships service detail page."""
    return render_template("public/services/strategic_partnerships.html")

@public_bp.route("/terms-of-service")
def terms_of_service():
    """Renders the Terms of Service page."""
    return render_template("public/terms.html")

@public_bp.route("/privacy-policy")
def privacy_policy():
    """Renders the Privacy Policy page."""
    return render_template("public/privacy.html")

@public_bp.route("/cookie-policy")
def cookie_policy():
    """Renders the Cookie Policy and Declaration page."""
    return render_template("public/cookie_policy.html")
