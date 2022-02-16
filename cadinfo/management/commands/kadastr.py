import logging
from argparse import ArgumentParser

from django.core.management.base import BaseCommand

from cadinfo.changesets import create_changeset
from cadinfo.management.commands.db_updates import update
from cadinfo.models import Update


class Command(BaseCommand):
    help = 'Create random users'

    def add_arguments(self, parser: ArgumentParser):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(levelname)-8s %(processName)s %(threadName)s %(message)s')

        subparsers = parser.add_subparsers(dest='action', required=True)

        update = subparsers.add_parser('update', help='Updates list of parcels from official api')

        parser.add_argument('--limit', help='Limit exetution to N parcels being updated; For debugging.')

        create_change = subparsers.add_parser('change', help='Creates diff information between changes')
        create_change.add_argument('-r', '--revision', required=True)
        create_change.add_argument('-p', '--previous', required=True)

    def handle(self, action, limit, *args, **kwargs):
        import logging
        logging.basicConfig(level=logging.INFO)

        if action == 'update':
            update.update_database()
        if action == 'change':
            create_changeset(
                revision=Update.objects.get(id=kwargs['revision']),
                previous=Update.objects.get(id=kwargs['previous']),
            )
