"""Integration tests for the SplentFeaturePartnersSeeder.

The seeder is the record of the old-site homepage partner logo strip migrated
from WordPress, so these tests pin down its shape rather than sample data.
"""

import os

import pytest

from splent_framework.db import db

from splent_io.splent_feature_partners import seeders
from splent_io.splent_feature_partners.models import Partner
from splent_io.splent_feature_partners.seeders import (
    PARTNERS,
    SplentFeaturePartnersSeeder,
)
from splent_io.splent_feature_partners.services import PartnersService


@pytest.fixture
def seeded(test_client):
    with test_client.application.app_context():
        SplentFeaturePartnersSeeder().run()
        yield


def test_the_seeder_data_holds_the_whole_strip():
    assert len(PARTNERS) == 5


def test_every_partner_logo_is_bundled():
    seed_dir = os.path.join(os.path.dirname(seeders.__file__), "seed_media")
    for p in PARTNERS:
        assert os.path.isfile(os.path.join(seed_dir, p["logo"])), p["name"]


def test_seeding_creates_every_partner(seeded):
    assert db.session.query(Partner).count() == len(PARTNERS)


def test_partners_keep_the_export_display_order(seeded):
    partners = Partner.query.order_by(Partner.order.asc()).all()
    assert [p.name for p in partners] == [p["name"] for p in PARTNERS]


def test_every_partner_carries_a_logo_and_is_active(seeded):
    for partner in Partner.query.all():
        assert partner.media_id is not None
        assert partner.logo_url
        assert partner.active


def test_the_export_had_no_logo_links(seeded):
    assert all(p.link == "" for p in Partner.query.all())


def test_seeded_partners_feed_the_public_strip(seeded):
    partners = PartnersService().active_partners()
    assert [p.name for p in partners] == [p["name"] for p in PARTNERS]


def test_reseeding_does_not_duplicate_media_items(seeded):
    first = sorted(p.media_id for p in Partner.query.all())
    SplentFeaturePartnersSeeder().run()
    partners = Partner.query.order_by(Partner.id.asc()).all()
    assert sorted(p.media_id for p in partners[len(PARTNERS) :]) == first
