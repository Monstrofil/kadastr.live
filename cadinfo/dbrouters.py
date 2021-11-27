from .models import Landuse, Koatuu, SearchIndex

LANDUSE_MODELS = (
    Landuse,
    Koatuu
)

LANDUSE_DB = 'cadastre'
PRIMARY_DB = 'primary'
SPHINX_DB = 'sphinx'


class DBRouter(object):

    def db_for_read(self, model, **hints):
        """ reading SomeModel from otherdb """
        if model in LANDUSE_MODELS:
            return LANDUSE_DB
        elif model == SearchIndex:
            return SPHINX_DB
        return PRIMARY_DB

    def db_for_write(self, model, **hints):
        """ writing SomeModel to otherdb """
        if model in LANDUSE_MODELS:
            return LANDUSE_DB
        return PRIMARY_DB
