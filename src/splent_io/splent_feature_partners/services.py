from splent_io.splent_feature_partners.models import Partner
from splent_io.splent_feature_partners.repositories import PartnersRepository
from splent_framework.db import db
from splent_framework.services.BaseService import BaseService


class PartnersService(BaseService):
    """Collaborating organisations shown on the homepage, each with a logo."""

    def __init__(self):
        super().__init__(PartnersRepository())

    def active_partners(self):
        """Active partners that still have a logo, in display order."""
        partners = (
            Partner.query.filter_by(active=True)
            .order_by(Partner.order.asc(), Partner.id.asc())
            .all()
        )
        return [p for p in partners if p.media is not None]

    def all_partners(self):
        return Partner.query.order_by(Partner.order.asc(), Partner.id.asc()).all()

    def get(self, partner_id):
        return Partner.query.get(partner_id)

    def create(self, **data):
        partner = Partner(**data)
        db.session.add(partner)
        db.session.commit()
        return partner

    def update(self, partner, **data):
        for key, value in data.items():
            setattr(partner, key, value)
        db.session.commit()
        return partner

    def delete(self, partner):
        db.session.delete(partner)
        db.session.commit()
