from splent_framework.db import db


class Partner(db.Model):
    """A collaborating organisation shown in the homepage partners strip.

    The logo comes from the media library (``media_id`` -> MediaItem); the
    feature only REFERENCES it, so logos are uploaded/managed in /admin/media.
    ON DELETE SET NULL keeps the partner if its logo is removed; the strip
    then shows the name as a wordmark until a new logo is picked.
    """

    __tablename__ = "partner"

    id = db.Column(db.Integer, primary_key=True)
    media_id = db.Column(
        db.Integer,
        db.ForeignKey("media_item.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    name = db.Column(db.String(255), default="")
    link = db.Column(db.String(512), default="")
    order = db.Column(db.Integer, default=0, index=True)
    active = db.Column(db.Boolean, default=True, index=True)

    media = db.relationship("MediaItem", lazy="joined")

    @property
    def logo_url(self):
        return self.media.url if self.media else ""

    def __repr__(self):
        return f"Partner<{self.id}>"
