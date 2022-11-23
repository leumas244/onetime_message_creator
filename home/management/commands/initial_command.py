from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'here your help information'

    def handle(self, *args, **options):
        print('######## START  ########')

        print('######## FINISHING  ########')
