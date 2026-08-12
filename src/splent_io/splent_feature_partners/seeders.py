import os

from splent_framework.seeders.BaseSeeder import BaseSeeder

from splent_io.splent_feature_media.services import MediaService
from splent_io.splent_feature_partners.models import Partner


def _seed_image(filename, title=""):
    """Import a bundled seed logo into the media library and return the item.

    Idempotent: MediaService.import_from_file dedupes on source_key, so
    re-running the seeder reuses the existing MediaItem instead of duplicating
    the file.
    """
    path = os.path.join(os.path.dirname(__file__), "seed_media", filename)
    return MediaService().import_from_file(
        path, title=title, source_key="seed://partners/" + filename
    )


# The old-site homepage logo strip ("The Diverso Lab is associated and works
# with several organizations"), in its display order. The export carried no
# links on the logos, so "link" stays empty. "logo" names a file bundled in
# seed_media/.
PARTNERS = [
    {"name": "Universidad de Málaga", "logo": "universidad-de-malaga.jpg"},
    {
        "name": "Ministerio de Ciencia, Innovación y Universidades",
        "logo": "ministerio-de-ciencia-innovacion-y-universidades.jpg",
    },
    {"name": "TASOVA", "logo": "tasova.png"},
    {"name": "IDEA Research Group", "logo": "idea-research-group.png"},
    {"name": "Universidad de Sevilla", "logo": "universidad-de-sevilla.jpg"},
]


class SplentFeaturePartnersSeeder(BaseSeeder):
    def run(self):
        data = []
        for order, p in enumerate(PARTNERS, start=1):
            media = _seed_image(p["logo"], title=p["name"])
            data.append(
                Partner(
                    media_id=media.id,
                    name=p["name"],
                    link=p.get("link", ""),
                    order=order,
                    active=True,
                )
            )

        self.seed(data)
