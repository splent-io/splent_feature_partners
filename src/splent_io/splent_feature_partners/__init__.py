from splent_framework.blueprints.base_blueprint import create_blueprint
from splent_framework.services.service_locator import register_service

from splent_io.splent_feature_partners.services import PartnersService

partners_bp = create_blueprint(__name__)


def init_feature(app):
    from splent_framework.assets.asset_registry import register_asset
    from splent_framework.settings.settings_schema import register_settings

    register_service(app, "PartnersService", PartnersService)
    register_asset(
        "css", "partners.assets", order=100, subfolder="css", filename="partners.css"
    )
    # Admin-configurable behaviour (framework renders the panel from this schema).
    register_settings(
        "partners",
        "Partners",
        [
            {
                "key": "title",
                "type": "text",
                "default": "Collaborating organisations",
                "label": "Section title",
            },
            {
                "key": "scope",
                "type": "select",
                "default": "home",
                "label": "Show on",
                "options": [("home", "Home page only"), ("all", "All pages")],
                "help": "Where the partners strip appears.",
            },
            {
                "key": "grayscale",
                "type": "bool",
                "default": "1",
                "label": "Greyscale logos",
                "help": "Show logos in grey, full colour on hover.",
            },
        ],
        icon="briefcase",
    )


def inject_context_vars(app):
    return {}
