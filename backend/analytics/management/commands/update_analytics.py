"""
Django management command to update analytics data.
Run this periodically (e.g., via cron job) to keep analytics fresh.

Usage:
    python manage.py update_analytics
    python manage.py update_analytics --type store
    python manage.py update_analytics --type product
"""

from django.core.management.base import BaseCommand
from analytics.services import AnalyticsService


class Command(BaseCommand):
    help = 'Update analytics data (store, product, rankings, activities)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--type',
            type=str,
            choices=['all', 'store', 'product', 'rankings', 'activities'],
            default='all',
            help='Type of analytics to update'
        )

    def handle(self, *args, **options):
        update_type = options['type']

        self.stdout.write(self.style.SUCCESS(f'\nStarting analytics update: {update_type}\n'))

        try:
            if update_type in ['all', 'store']:
                self.stdout.write('Updating store analytics...')
                AnalyticsService.update_store_analytics()
                self.stdout.write(self.style.SUCCESS(' Store analytics updated\n'))

            if update_type in ['all', 'product']:
                self.stdout.write('Updating product analytics...')
                AnalyticsService.update_product_analytics()
                self.stdout.write(self.style.SUCCESS(' Product analytics updated\n'))

            if update_type in ['all', 'rankings']:
                self.stdout.write('Updating store-product rankings...')
                AnalyticsService.update_store_product_rankings()
                self.stdout.write(self.style.SUCCESS(' Store-product rankings updated\n'))

            if update_type in ['all', 'activities']:
                self.stdout.write('Updating user-store activities...')
                AnalyticsService.update_user_store_activities()
                self.stdout.write(self.style.SUCCESS(' User-store activities updated\n'))

            self.stdout.write(self.style.SUCCESS(f'\n Analytics update complete: {update_type}\n'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\nL Error updating analytics: {str(e)}\n'))
            raise
