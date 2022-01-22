from .models import SearchIndex


PRIMARY_DB = 'default'
SPHINX_DB = 'sphinx'


class DBRouter(object):

    def db_for_read(self, model, **hints):
        """ reading SomeModel from otherdb """
        if model == SearchIndex:
            return SPHINX_DB
        return PRIMARY_DB

    def db_for_write(self, model, **hints):
        """ writing SomeModel to otherdb """
        return PRIMARY_DB
