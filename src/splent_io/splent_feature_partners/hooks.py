"""Template hooks for splent_feature_partners.

* ``home.section`` — renders the public partners strip on the homepage (or on
  every public page when the admin sets scope="all").
* ``layout.authenticated_sidebar`` — admin sidebar link to the partners manager.

The strip's CSS is NOT injected here: it is declared through the asset registry
(in __init__.init_feature via register_asset) so the shell loads it in a
deduplicated, deterministic order. The markup is config-driven (title / scope /
grayscale) via the admin-editable settings read by get_config("partners").
"""

from flask import render_template, request, url_for
from markupsafe import Markup

from splent_framework.hooks.template_hooks import register_template_hook
from splent_framework.services.service_locator import service_proxy
from splent_framework.settings.settings_schema import get_config


def partners_section():
    """Render the partners strip into the home.section slot.

    Scope-aware: by default (scope="home") it renders only on the homepage;
    "all" renders it on every public page. Returns "" when there are no active
    partners so the slot collapses cleanly rather than showing an empty heading.
    """
    cfg = get_config("partners")
    if cfg.get("scope", "home") == "home" and request.endpoint != "public.index":
        return ""
    try:
        partners = service_proxy("PartnersService").active_partners()
    except Exception:
        return ""
    if not partners:
        return ""
    return Markup(render_template("partners/strip.html", partners=partners, cfg=cfg))


def partners_admin_link():
    """Sidebar entry for the partners manager (the WP-plugin pattern)."""
    active = (
        "active"
        if request.endpoint and request.endpoint.startswith("partners.admin")
        else ""
    )
    return (
        f'<li class="sidebar-item {active}">'
        f'<a class="sidebar-link" href="{url_for("partners.admin_index")}">'
        '<i class="align-middle" data-feather="briefcase"></i> '
        '<span class="align-middle">Partners</span>'
        "</a>"
        "</li>"
    )


register_template_hook("home.section", partners_section, order=30)
register_template_hook("layout.authenticated_sidebar", partners_admin_link)
