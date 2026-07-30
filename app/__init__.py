from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
import logging

login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

def auto_seed_site_content():
    """Auto-populates missing default content on server startup."""
    from app.models import SiteContent
    from app import db

    DEFAULT_CONTENTS = [
    # --- HERO SECTION ---
        {
            "key": "home_hero_title",
            "description": "Homepage - Hero Section Headline",
            "content": "International Consulting<br>for Africa and Europe",
        },
        {
            "key": "home_hero_text",
            "description": "Homepage - Hero Section Paragraph",
            "content": "We provide international consulting, immigration support, market entry strategies and business advisory services connecting Europe and Africa.",
        },
        {
            "key": "home_hero_btn_contact",
            "description": "Homepage - Hero Primary Button Text",
            "content": "Contact Us",
        },
        {
            "key": "home_hero_btn_learn",
            "description": "Homepage - Hero Secondary Button Text",
            "content": "Learn More",
        },
    # --- SERVICES SECTION ---
        {
            "key": "home_services_title",
            "description": "Homepage - Services Section Heading",
            "content": "Our Services",
        },
        {
            "key": "home_services_subtitle",
            "description": "Homepage - Services Section Subtitle",
            "content": "Supporting businesses, institutions and individuals in building successful connections between Europe and Africa.",
        },
    # Service Card 1
        {
            "key": "home_services_card1_title",
            "description": "Homepage - Service Card 1 Title",
            "content": "Immigration Support",
        },
        {
            "key": "home_services_card1_desc",
            "description": "Homepage - Service Card 1 Description",
            "content": "Professional assistance with visas, residence permits, documentation and administrative procedures.",
        },
        {
            "key": "home_services_card1_link",
            "description": "Homepage - Service Card 1 Link Text",
            "content": "Learn More →",
        },
    # Service Card 2
        {
            "key": "home_services_card2_title",
            "description": "Homepage - Service Card 2 Title",
            "content": "Business Consulting",
        },
        {
            "key": "home_services_card2_desc",
            "description": "Homepage - Service Card 2 Description",
            "content": "Strategic advisory services helping organizations expand, optimize operations and achieve sustainable growth.",
        },
        {
            "key": "home_services_card2_link",
            "description": "Homepage - Service Card 2 Link Text",
            "content": "Learn More →",
        },
    # Service Card 3
        {
            "key": "home_services_card3_title",
            "description": "Homepage - Service Card 3 Title",
            "content": "Market Entry Strategies",
        },
        {
            "key": "home_services_card3_desc",
            "description": "Homepage - Service Card 3 Description",
            "content": "Market analysis, expansion planning and local expertise for successful entry into African and European markets.",
        },
        {
            "key": "home_services_card3_link",
            "description": "Homepage - Service Card 3 Link Text",
            "content": "Learn More →",
        },
    # Service Card 4
        {
            "key": "home_services_card4_title",
            "description": "Homepage - Service Card 4 Title",
            "content": "Strategic Partnerships",
        },
        {
            "key": "home_services_card4_desc",
            "description": "Homepage - Service Card 4 Description",
            "content": "Connecting businesses, NGOs and institutions with trusted partners to foster long-term international cooperation.",
        },
        {
            "key": "home_services_card4_link",
            "description": "Homepage - Service Card 4 Link Text",
            "content": "Learn More →",
        },
    # --- WHY AKEBULAN SECTION ---
        {
            "key": "home_why_title",
            "description": "Homepage - Why Akebulan Heading",
            "content": "Why Akebulan?",
        },
        {
            "key": "home_why_subtitle",
            "description": "Homepage - Why Akebulan Subtitle",
            "content": "At Akebulan International Consulting, we believe successful international projects are built on trust, local knowledge and long-term partnerships.",
        },
    # Why Feature 1
        {
            "key": "home_why_card1_title",
            "description": "Homepage - Why Feature 1 Title",
            "content": "Regional Expertise",
        },
        {
            "key": "home_why_card1_desc",
            "description": "Homepage - Why Feature 1 Description",
            "content": "Deep understanding of both African and European markets, allowing us to provide practical and informed guidance.",
        },
    # Why Feature 2
        {
            "key": "home_why_card2_title",
            "description": "Homepage - Why Feature 2 Title",
            "content": "Personalized Consulting",
        },
        {
            "key": "home_why_card2_desc",
            "description": "Homepage - Why Feature 2 Description",
            "content": "Every client receives solutions specifically tailored to their objectives, industry and international ambitions.",
        },
    # Why Feature 3
        {
            "key": "home_why_card3_title",
            "description": "Homepage - Why Feature 3 Title",
            "content": "Multilingual Support",
        },
        {
            "key": "home_why_card3_desc",
            "description": "Homepage - Why Feature 3 Description",
            "content": "Communication across languages and cultures to simplify international collaboration and business development.",
        },
    # Why CTA
        {
            "key": "home_why_cta_title",
            "description": "Homepage - Why Section Call-to-Action Heading",
            "content": "Ready to expand internationally?",
        },
        {
            "key": "home_why_cta_btn",
            "description": "Homepage - Why Section Call-to-Action Button",
            "content": "Contact Us Today",
        },
    # --- INSIGHTS & PUBLICATIONS SECTION ---
        {
            "key": "home_insights_title",
            "description": "Homepage - Insights Section Heading",
            "content": "Insights & Publications",
        },
        {
            "key": "home_insights_subtitle",
            "description": "Homepage - Insights Section Subtitle",
            "content": "Expert perspectives on international consulting, immigration, business expansion and African-European cooperation.",
        },
        {
            "key": "home_insights_read_more",
            "description": "Homepage - Insights Read Article Button Text",
            "content": "Read Article →",
        },
        {
            "key": "home_insights_view_all",
            "description": "Homepage - Insights View All Button Text",
            "content": "View All Publications →",
        },
# --- FOOTER SECTION ---
        {
            "key": "footer_about_text",
            "description": "Footer - Brand Description",
            "content": "Connecting Europe and Africa through strategic consulting, immigration support, and business development.",
        },
        {
            "key": "footer_nav_heading",
            "description": "Footer - Quick Links Heading",
            "content": "Quick Links",
        },
        {
            "key": "footer_link_home",
            "description": "Footer - Home Link Label",
            "content": "Home",
        },
        {
            "key": "footer_link_contact",
            "description": "Footer - Contact Link Label",
            "content": "Contact Us",
        },
        {
            "key": "footer_contact_heading",
            "description": "Footer - Contact Info Heading",
            "content": "Contact Info",
        },
        {
            "key": "footer_address",
            "description": "Footer - Physical Address",
            "content": "Madrid, Spain & Nairobi, Kenya",
        },
        {
            "key": "footer_email",
            "description": "Footer - Contact Email",
            "content": "info@akebulanconsulting.com",
        },
        {
            "key": "footer_phone",
            "description": "Footer - Phone Number",
            "content": "+34 123 456 789",
        },
        {
            "key": "footer_copyright",
            "description": "Footer - Copyright Notice",
            "content": "© Akebulan International Consulting. All rights reserved.",
        },
        {
            "key": "footer_company_name",
            "description": "Footer - Company / Brand Name Heading",
            "content": "Akebulan",
        },
    ]
    try:
        for item in DEFAULT_CONTENTS:
            existing = SiteContent.query.filter_by(key=item["key"]).first()
            if not existing:
                new_content = SiteContent(
                    key=item["key"],
                    description=item["description"],
                    content=item["content"]
                )
                db.session.add(new_content)
        db.session.commit()
    except Exception:
        db.session.rollback()

def create_app(settings_module):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(settings_module)
    if app.config.get('TESTING', False):
        app.config.from_pyfile('config-testing.py', silent=True)
    else:
        app.config.from_pyfile('config.py', silent=True)

    configure_logging(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    db.init_app(app)
    migrate.init_app(app,db)
    mail.init_app(app)

    # Registro de los Blueprints
    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    from .admin import admin_bp
    app.register_blueprint(admin_bp)

    from .public import public_bp
    app.register_blueprint(public_bp)

    from .contact import contact_bp
    app.register_blueprint(contact_bp)

    register_error_handlers(app)

    # Inject site texts globally for all Jinja templates
    @app.context_processor
    def inject_site_texts():
        try:
            from app.models import SiteContent
            items = SiteContent.get_all()
            return dict(texts={item.key: item.content for item in items})
        except Exception:
            # Fallback if database is not migrated yet
            return dict(texts={})

    with app.app_context():
        auto_seed_site_content()

    return app

def register_error_handlers(app):
    @app.errorhandler(500)
    def base_error_handler(e):
        return render_template('500.html'), 500

    @app.errorhandler(404)
    def base_error_handler(e):
        return render_template('404.html'), 404

    @app.errorhandler(403)
    def base_error_handler(e):
        return render_template('403.html'), 403


def configure_logging(app):
    del app.logger.handlers[:]

    loggers = [app.logger, ]
    handlers = []

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(verbose_formatter())

    if(app.config['APP_ENV'] == app.config['APP_ENV_LOCAL']) or (app.config['APP_ENV'] == app.config['APP_ENV_TESTING']) or (app.config['APP_ENV'] == app.config['APP_ENV_DEVELOPMENT']):
        console_handler.setLevel(logging.DEBUG)
        handlers.append(console_handler)
    elif app.config['APP_ENV'] == app.config['APP_ENV_PRODUCTION']:
        console_handler.setLevel(logging.INFO)
        handlers.append(console_handler)

        mail_handler = SMTPHandler((app.config['MAIL_SERVER'], app.config['MAIL_PORT']), app.config['DONT_REPLY_FROM_EMAIL'], app.config['ADMINS'], '[Error]{} La aplicación falló'.format(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']), ())
        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(mail_handler_formatter())
        handlers.append(mail_handler)

    for l in loggers:
        for handler in handlers:
            l.addHandler(handler)
        l.propagate = False
        l.setLevel(logging.DEBUG)

def verbose_formatter():
    return logging.Formatter(
        '[%(asctime)s.%(msecs)d]\t %(levelname)s \t[%(name)s.%(funcName)s:%(lineno)d]\t %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S'
    )

def mail_handler_formatter():
    return logging.Formatter(
        '''
            Message type:       %(levelname)s
            Location:           %(pathname)s:%(lineno)d
            Module:             %(module)s
            Function:           %(funcName)s
            Time:               %(asctime)s.%(msecs)d

            Message:

            %(message)s
        ''',
        datefmt='%d/%m/%Y %H:%M:%S'
    )
