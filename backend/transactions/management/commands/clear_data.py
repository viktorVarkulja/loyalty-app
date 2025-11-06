from django.core.management.base import BaseCommand
from django.db import transaction as db_transaction
from django.contrib.auth import get_user_model
from transactions.models import Transaction, TransactionItem
from products.models import Product, Store
from reviews.models import ReviewRequest

User = get_user_model()


class Command(BaseCommand):
    help = 'Clear all data from database except users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm that you want to delete all data',
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(
                self.style.WARNING(
                    'This will delete ALL data except users!\n'
                    'User points will be reset to 0.\n'
                    'To confirm, run: python manage.py clear_data --confirm'
                )
            )
            return

        self.stdout.write('Starting to clear data...')

        with db_transaction.atomic():
            # Delete in order to respect foreign key constraints
            # 1. Delete transaction items first (they reference transactions)
            item_count = TransactionItem.objects.count()
            TransactionItem.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f'Deleted {item_count} transaction items'))

            # 2. Delete transactions (they reference stores)
            transaction_count = Transaction.objects.count()
            Transaction.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f'Deleted {transaction_count} transactions'))

            # 3. Delete review requests
            review_count = ReviewRequest.objects.count()
            ReviewRequest.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f'Deleted {review_count} review requests'))

            # 4. Delete products
            product_count = Product.objects.count()
            Product.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f'Deleted {product_count} products'))

            # 5. Delete stores
            store_count = Store.objects.count()
            Store.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f'Deleted {store_count} stores'))

            # 6. Reset all user points to 0
            user_count = User.objects.all().update(points=0)
            self.stdout.write(self.style.SUCCESS(f'Reset points to 0 for {user_count} users'))

        self.stdout.write(
            self.style.SUCCESS(
                '\nSuccessfully cleared all data except users!\n'
                'Users and their accounts remain intact with 0 points.'
            )
        )
