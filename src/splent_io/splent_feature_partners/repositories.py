from splent_io.splent_feature_partners.models import Partner
from splent_framework.repositories.BaseRepository import BaseRepository


class PartnersRepository(BaseRepository):
    def __init__(self):
        super().__init__(Partner)
