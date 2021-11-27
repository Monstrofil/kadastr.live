import logging
from argparse import ArgumentParser

from django.core.management.base import BaseCommand

from cadinfo.management.commands.db_updates import update


class Command(BaseCommand):
    help = 'Create random users'

    def add_arguments(self, parser: ArgumentParser):
        logging.basicConfig(level=logging.INFO)

        subparsers = parser.add_subparsers(dest='action', required=True)

        update = subparsers.add_parser('update', help='Updates list of parcels from official api')

        parser.add_argument('--limit', help='Limit exetution to N parcels being updated; For debugging.')

    def handle(self, action, limit, *args, **kwargs):
        if action == 'update':
            update.update_database()
