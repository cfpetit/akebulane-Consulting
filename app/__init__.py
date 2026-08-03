from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from logging.handlers import SMTPHandler
import logging

login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
csrf = CSRFProtect()

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
    # --- IMMIGRATION SERVICE PAGE ---
        {
            "key": "immigration_hero_title",
            "description": "Immigration Page - Hero Title",
            "content": "Professional Immigration & Residency Support",
        },
        {
            "key": "immigration_hero_subtitle",
            "description": "Immigration Page - Hero Subtitle",
            "content": "Streamlining visa applications, residency permits, and administrative procedures between Europe and Africa.",
        },
        {
            "key": "immigration_overview_title",
            "description": "Immigration Page - Overview Section Title",
            "content": "Navigating Cross-Border Mobility",
        },
        {
            "key": "immigration_overview_text",
            "description": "Immigration Page - Overview Paragraph",
            "content": "International regulations and administrative requirements can be complex and time-consuming. We provide personalized, legal, and operational guidance to ensure individuals, corporate teams, and investors secure the proper authorization smoothly and in full compliance with local laws.",
        },
        {
            "key": "immigration_item1_title",
            "description": "Immigration Page - Feature 1 Title",
            "content": "Visas & Work Permits",
        },
        {
            "key": "immigration_item1_desc",
            "description": "Immigration Page - Feature 1 Description",
            "content": "End-to-end management for business visas, highly qualified worker permits, and investor mobility frameworks.",
        },
        {
            "key": "immigration_item2_title",
            "description": "Immigration Page - Feature 2 Title",
            "content": "Residency Permits",
        },
        {
            "key": "immigration_item2_desc",
            "description": "Immigration Page - Feature 2 Description",
            "content": "Assistance with initial residency filings, renewals, family reunification, and long-term stay authorizations.",
        },
        {
            "key": "immigration_item3_title",
            "description": "Immigration Page - Feature 3 Title",
            "content": "Corporate Relocation",
        },
        {
            "key": "immigration_item3_desc",
            "description": "Immigration Page - Feature 3 Description",
            "content": "Strategic mobility solutions for companies transferring executives, specialists, or entire project teams abroad.",
        },
        {
            "key": "immigration_cta_title",
            "description": "Immigration Page - Bottom CTA Title",
            "content": "Require Expert Guidance for Your Visa or Residency?",
        },
        {
            "key": "immigration_cta_btn",
            "description": "Immigration Page - Bottom CTA Button",
            "content": "Request Immigration Consultation",
        },

    # --- BUSINESS CONSULTING SERVICE PAGE ---
        {
            "key": "business_hero_title",
            "description": "Business Page - Hero Title",
            "content": "Strategic Business Consulting",
        },
        {
            "key": "business_hero_subtitle",
            "description": "Business Page - Hero Subtitle",
            "content": "Driving sustainable growth, operational excellence, and international competitiveness for your organization.",
        },
        {
            "key": "business_overview_title",
            "description": "Business Page - Overview Section Title",
            "content": "Transforming Vision into Action",
        },
        {
            "key": "business_overview_text",
            "description": "Business Page - Overview Paragraph",
            "content": "Whether you are a startup looking to scale or an established enterprise navigating cross-border challenges, our advisory services are tailored to optimize your operations, mitigate risks, and uncover new revenue streams across European and African markets.",
        },
        {
            "key": "business_item1_title",
            "description": "Business Page - Feature 1 Title",
            "content": "Operational Optimization",
        },
        {
            "key": "business_item1_desc",
            "description": "Business Page - Feature 1 Description",
            "content": "Streamline processes, reduce overhead costs, and improve overall efficiency to maximize your profitability.",
        },
        {
            "key": "business_item2_title",
            "description": "Business Page - Feature 2 Title",
            "content": "Risk Management",
        },
        {
            "key": "business_item2_desc",
            "description": "Business Page - Feature 2 Description",
            "content": "Identify, assess, and develop comprehensive strategies to mitigate financial, operational, and market risks.",
        },
        {
            "key": "business_item3_title",
            "description": "Business Page - Feature 3 Title",
            "content": "Growth & Strategy",
        },
        {
            "key": "business_item3_desc",
            "description": "Business Page - Feature 3 Description",
            "content": "Data-driven strategic planning to help you capture new market share, innovate products, and outpace the competition.",
        },
        {
            "key": "business_cta_title",
            "description": "Business Page - Bottom CTA Title",
            "content": "Ready to elevate your business performance?",
        },
        {
            "key": "business_cta_btn",
            "description": "Business Page - Bottom CTA Button",
            "content": "Schedule a Strategy Session",
        },

    # --- MARKET ENTRY SERVICE PAGE ---
        {
            "key": "market_hero_title",
            "description": "Market Entry Page - Hero Title",
            "content": "Market Entry Strategies",
        },
        {
            "key": "market_hero_subtitle",
            "description": "Market Entry Page - Hero Subtitle",
            "content": "Confidently expand your business footprint across African and European markets with data-driven insights and local expertise.",
        },
        {
            "key": "market_overview_title",
            "description": "Market Entry Page - Overview Section Title",
            "content": "Your Bridge to New Markets",
        },
        {
            "key": "market_overview_text",
            "description": "Market Entry Page - Overview Paragraph",
            "content": "Entering a new country requires more than just capital; it requires deep local knowledge, cultural intelligence, and regulatory foresight. We guide you through every phase of your expansion to ensure a successful, profitable, and compliant market launch.",
        },
        {
            "key": "market_item1_title",
            "description": "Market Entry Page - Feature 1 Title",
            "content": "Market Research & Feasibility",
        },
        {
            "key": "market_item1_desc",
            "description": "Market Entry Page - Feature 1 Description",
            "content": "Comprehensive analysis of market demand, competitor landscapes, and economic indicators to validate your expansion plans.",
        },
        {
            "key": "market_item2_title",
            "description": "Market Entry Page - Feature 2 Title",
            "content": "Regulatory & Compliance",
        },
        {
            "key": "market_item2_desc",
            "description": "Market Entry Page - Feature 2 Description",
            "content": "Navigating local corporate laws, tax frameworks, and industry-specific regulations to ensure your operations are fully compliant.",
        },
        {
            "key": "market_item3_title",
            "description": "Market Entry Page - Feature 3 Title",
            "content": "Localization & Go-To-Market",
        },
        {
            "key": "market_item3_desc",
            "description": "Market Entry Page - Feature 3 Description",
            "content": "Tailoring your value proposition, pricing strategies, and marketing channels to resonate with local consumers and stakeholders.",
        },
        {
            "key": "market_cta_title",
            "description": "Market Entry Page - Bottom CTA Title",
            "content": "Planning an international expansion?",
        },
        {
            "key": "market_cta_btn",
            "description": "Market Entry Page - Bottom CTA Button",
            "content": "Discuss Your Expansion Goals",
        },

     # --- STRATEGIC PARTNERSHIPS SERVICE PAGE ---
        {
            "key": "partnerships_hero_title",
            "description": "Partnerships Page - Hero Title",
            "content": "Strategic Partnerships",
        },
        {
            "key": "partnerships_hero_subtitle",
            "description": "Partnerships Page - Hero Subtitle",
            "content": "Forging high-value alliances between European and African organizations for mutual growth and sustainable impact.",
        },
        {
            "key": "partnerships_overview_title",
            "description": "Partnerships Page - Overview Section Title",
            "content": "Connecting the Right Stakeholders",
        },
        {
            "key": "partnerships_overview_text",
            "description": "Partnerships Page - Overview Paragraph",
            "content": "Building the right relationships is critical to international success. We leverage our extensive network to connect businesses, NGOs, and public institutions with trusted local and global partners, fostering long-term cooperation and shared value.",
        },
        {
            "key": "partnerships_item1_title",
            "description": "Partnerships Page - Feature 1 Title",
            "content": "Partner Identification",
        },
        {
            "key": "partnerships_item1_desc",
            "description": "Partnerships Page - Feature 1 Description",
            "content": "Rigorous vetting and selection of potential local partners, distributors, suppliers, and joint venture candidates.",
        },
        {
            "key": "partnerships_item2_title",
            "description": "Partnerships Page - Feature 2 Title",
            "content": "Negotiation & Structuring",
        },
        {
            "key": "partnerships_item2_desc",
            "description": "Partnerships Page - Feature 2 Description",
            "content": "Expert facilitation of partnership agreements, ensuring fair, compliant, and mutually beneficial frameworks.",
        },
        {
            "key": "partnerships_item3_title",
            "description": "Partnerships Page - Feature 3 Title",
            "content": "Institutional Alliances",
        },
        {
            "key": "partnerships_item3_desc",
            "description": "Partnerships Page - Feature 3 Description",
            "content": "Bridging the gap between private enterprises, public institutions, NGOs, and international trade organizations.",
        },
        {
            "key": "partnerships_cta_title",
            "description": "Partnerships Page - Bottom CTA Title",
            "content": "Looking for the right international partner?",
        },
        {
            "key": "partnerships_cta_btn",
            "description": "Partnerships Page - Bottom CTA Button",
            "content": "Explore Partnership Opportunities",
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

    # --- LEGAL PAGES ---
        {
            "key": "terms_title",
            "description": "Terms of Service - Page Title",
            "content": "Terms of Service",
        },
        {
            "key": "terms_content",
            "description": "Terms of Service - Body Content (HTML allowed)",
            "content": "<h2>1. Terms</h2><p>Terms of service placeholder content. Edit this from your Admin Dashboard.</p>",
        },
        {
            "key": "privacy_title",
            "description": "Privacy Policy - Page Title",
            "content": "Privacy Policy",
        },
        {
            "key": "privacy_content",
            "description": "Privacy Policy - Body Content (HTML allowed)",
            "content": "<h2>1. Data Protection</h2><p>Privacy policy placeholder content. Edit this from your Admin Dashboard.</p>",
        },
        {
            "key": "cookie_policy_title",
            "description": "Cookie Policy - Page Title",
            "content": "Cookie Policy & Declaration",
        },
        {
            "key": "cookie_policy_content",
            "description": "Cookie Policy - Body Content (HTML allowed)",
            "content": "<h2>1. Cookie Declaration</h2><p>Cookie policy placeholder content. Edit this from your Admin Dashboard.</p>",
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

    csrf.init_app(app)

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

    @app.errorhandler(400)
    def base_error_handler(e):
        return render_template('400.html'), 400


def configure_logging(app):
    del app.logger.handlers[:]

    loggers = [app.logger, ]
    handlers = []

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(verbose_formatter())

    app_env = app.config.get('APP_ENV', 'production')
    env_local = app.config.get('APP_ENV_LOCAL', 'local')
    env_testing = app.config.get('APP_ENV_TESTING'. 'testing')
    env_dev = app.config.get('APP_ENV_DEVELOPMENT', 'development')
    env_prod = app.config.get('APP_ENV_PRODUCTION', 'production')

    if app_env in (env_local, env_testing, env_dev):
        console_handler.setLevel(logging.DEBUG)
        handlers.append(console_handler)
    elif app_env == env_prod:
        console_handler.setLevel(logging.INFO)
        handlers.append(console_handler)

        mail_server = app.config.get('MAIL_SERVER')
        mail_port = app.config.get('MAIL_PORT')
        from_email = app.config.get('DONT_REPLY_FROM_EMAIL')
        admins = app.config.get('ADMINS')
        if mail_server and mail_port and from_email and admins:
            mail_handler = SMTPHandler(
                (mail_server, mail_port),
                from_email,
                admins,
                '[Error] La aplicación falló',
                credentials=(
                  app.config.get('MAIL_USERNAME'),
                  app.config.get('MAIL_PASSWORD')
                ) if app.config.get('MAIL_USERNAME') else None
        )

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
