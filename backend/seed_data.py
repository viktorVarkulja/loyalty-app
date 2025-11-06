#!/usr/bin/env python
"""
Seed script to populate the database with initial test users.
Run with: python seed_data.py
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User


def seed_database():
    """Populate database with initial test users."""

    print("Starting database seeding...")

    # Create test users
    print("\n1. Creating test users...")

    if not User.objects.filter(email='user@example.com').exists():
        user1 = User.objects.create_user(
            email='user@example.com',
            name='Test User',
            password='user123',
            points=0
        )
        print(f"   ✓ Created user: {user1.email}")
    else:
        user1 = User.objects.get(email='user@example.com')
        print(f"   → User already exists: {user1.email}")

    if not User.objects.filter(email='john@example.com').exists():
        user2 = User.objects.create_user(
            email='john@example.com',
            name='John Doe',
            password='john123',
            points=0
        )
        print(f"   ✓ Created user: {user2.email}")
    else:
        user2 = User.objects.get(email='john@example.com')
        print(f"   → User already exists: {user2.email}")

    print("\n" + "="*60)
    print("Database seeding completed successfully!")
    print("="*60)
    print(f"\nTotal users: {User.objects.count()}")
    print("\nTest credentials:")
    print("  Admin:")
    print("    Email: admin@example.com")
    print("    Password: admin123")
    print("  User 1:")
    print("    Email: user@example.com")
    print("    Password: user123")
    print("  User 2:")
    print("    Email: john@example.com")
    print("    Password: john123")
    print()


if __name__ == '__main__':
    seed_database()
