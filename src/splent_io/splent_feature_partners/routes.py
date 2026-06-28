from flask import (
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required

from splent_io.splent_feature_partners import partners_bp
from splent_framework.services.service_locator import service_proxy

partners_service = service_proxy("PartnersService")


# =====================================================================
# PUBLIC
# =====================================================================
@partners_bp.route("/partners", methods=["GET"])
def index():
    return render_template("partners/index.html")


# =====================================================================
# ADMIN — domain-specific management (the "plugin" screen)
# =====================================================================
def _images():
    """Image-only media items offered in the picker."""
    return [m for m in service_proxy("MediaService").list_recent() if m.is_image]


def _form_to_data(form):
    media_id = (form.get("media_id") or "").strip()
    return {
        "media_id": int(media_id) if media_id else None,
        "name": (form.get("name") or "").strip(),
        "link": (form.get("link") or "").strip(),
        "order": int(form.get("order") or 0),
        "active": bool(form.get("active")),
    }


@partners_bp.route("/admin/partners", methods=["GET"])
@login_required
def admin_index():
    return render_template(
        "partners/admin/list.html",
        partners=partners_service.all_partners(),
    )


@partners_bp.route("/admin/partners/new", methods=["GET", "POST"])
@login_required
def admin_new():
    if request.method == "POST":
        data = _form_to_data(request.form)
        if not data["media_id"]:
            flash("A logo is required.", "danger")
            return redirect(url_for("partners.admin_new"))
        partner = partners_service.create(**data)
        flash(f"Added {partner.name or 'partner'}.", "success")
        return redirect(url_for("partners.admin_index"))
    return render_template("partners/admin/form.html", partner=None, media=_images())


@partners_bp.route("/admin/partners/<int:id>/edit", methods=["GET", "POST"])
@login_required
def admin_edit(id):
    partner = partners_service.get(id)
    if partner is None:
        from flask import abort

        abort(404)
    if request.method == "POST":
        data = _form_to_data(request.form)
        if not data["media_id"]:
            flash("A logo is required.", "danger")
            return redirect(url_for("partners.admin_edit", id=id))
        partners_service.update(partner, **data)
        flash(f"Updated {partner.name or 'partner'}.", "success")
        return redirect(url_for("partners.admin_index"))
    return render_template("partners/admin/form.html", partner=partner, media=_images())


@partners_bp.route("/admin/partners/<int:id>/delete", methods=["POST"])
@login_required
def admin_delete(id):
    partner = partners_service.get(id)
    if partner is None:
        from flask import abort

        abort(404)
    name = partner.name or "partner"
    partners_service.delete(partner)
    flash(f"Removed {name}.", "success")
    return redirect(url_for("partners.admin_index"))
