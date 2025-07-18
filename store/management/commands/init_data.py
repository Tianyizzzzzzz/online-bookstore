"""
Django management command to initialize the bookstore with sample data.

This command creates sample books, users, and other data to help with
development and testing of the online bookstore application.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from store.models import Book, UserProfile
import os


class Command(BaseCommand):
    """
    Management command to initialize the bookstore with sample data.

    This command creates sample books, a test user, and other necessary
    data to get the bookstore up and running for development.
    """

    help = 'Initialize the bookstore with sample data'

    def add_arguments(self, parser):
        """Add command line arguments"""
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before adding new data',
        )

        parser.add_argument(
            '--books-only',
            action='store_true',
            help='Only create sample books',
        )

        parser.add_argument(
            '--users-only',
            action='store_true',
            help='Only create sample users',
        )

    def handle(self, *args, **options):
        """Handle the command execution"""

        self.stdout.write(
            self.style.SUCCESS('Starting bookstore initialization...')
        )

        # Clear existing data if requested
        if options['clear']:
            self.clear_data()

        # Create sample data based on options
        if options['books_only']:
            self.create_sample_books()
        elif options['users_only']:
            self.create_sample_users()
        else:
            self.create_sample_users()
            self.create_sample_books()

        self.stdout.write(
            self.style.SUCCESS('Successfully initialized bookstore!')
        )

    def clear_data(self):
        """Clear existing data from the database"""
        self.stdout.write('Clearing existing data...')

        # Clear books
        Book.objects.all().delete()

        # Clear users except superusers
        User.objects.filter(is_superuser=False).delete()

        self.stdout.write(
            self.style.WARNING('Existing data cleared!')
        )

    def create_sample_users(self):
        """Create sample users for testing"""
        self.stdout.write('Creating sample users...')

        # Create a demo user
        if not User.objects.filter(username='demo').exists():
            demo_user = User.objects.create_user(
                username='demo',
                email='demo@example.com',
                password='demo123',
                first_name='Demo',
                last_name='User'
            )

            # Create profile
            UserProfile.objects.create(
                user=demo_user,
                phone_number='123-456-7890',
                default_shipping_address='123 Demo Street',
                default_shipping_city='Demo City',
                default_shipping_state='Demo State',
                default_shipping_zip='12345'
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Created demo user: {demo_user.username}'
                )
            )

        # Create a test customer
        if not User.objects.filter(username='customer').exists():
            customer = User.objects.create_user(
                username='customer',
                email='customer@example.com',
                password='customer123',
                first_name='John',
                last_name='Doe'
            )

            # Create profile
            UserProfile.objects.create(
                user=customer,
                phone_number='987-654-3210',
                default_shipping_address='456 Customer Lane',
                default_shipping_city='Customer City',
                default_shipping_state='Customer State',
                default_shipping_zip='54321'
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Created customer user: {customer.username}'
                )
            )

    def create_sample_books(self):
        """Create sample books for the bookstore"""
        self.stdout.write('Creating sample books...')

        # Sample book data
        books_data = [
            {
                'title': 'Python Programming for Beginners',
                'author': 'John Smith',
                'isbn': '9781234567890',
                'description': 'A comprehensive guide to learning Python programming from scratch. This book covers all the fundamentals of Python including data types, control structures, functions, and object-oriented programming.',
                'price': Decimal('29.99'),
                'stock_quantity': 50,
                'is_featured': True,
            },
            {
                'title': 'Django Web Development',
                'author': 'Jane Doe',
                'isbn': '9781234567891',
                'description': 'Learn how to build powerful web applications using Django framework. This book covers everything from basic setup to advanced features like authentication and deployment.',
                'price': Decimal('39.99'),
                'stock_quantity': 30,
                'is_featured': True,
            },
            {
                'title': 'JavaScript: The Complete Guide',
                'author': 'Mike Johnson',
                'isbn': '9781234567892',
                'description': 'Master JavaScript programming with this comprehensive guide. Learn modern JavaScript features, DOM manipulation, and asynchronous programming.',
                'price': Decimal('34.99'),
                'stock_quantity': 25,
                'is_featured': False,
            },
            {
                'title': 'Database Design Fundamentals',
                'author': 'Sarah Wilson',
                'isbn': '9781234567893',
                'description': 'Understand the principles of database design and normalization. This book covers SQL, database modeling, and best practices for database development.',
                'price': Decimal('44.99'),
                'stock_quantity': 20,
                'is_featured': True,
            },
            {
                'title': 'HTML and CSS Mastery',
                'author': 'David Brown',
                'isbn': '9781234567894',
                'description': 'Learn to create beautiful and responsive web pages using HTML and CSS. Includes modern CSS techniques and responsive design principles.',
                'price': Decimal('24.99'),
                'stock_quantity': 35,
                'is_featured': False,
            },
            {
                'title': 'React.js Development',
                'author': 'Emily Davis',
                'isbn': '9781234567895',
                'description': 'Build modern user interfaces with React.js. This book covers components, state management, hooks, and advanced React patterns.',
                'price': Decimal('42.99'),
                'stock_quantity': 15,
                'is_featured': True,
            },
            {
                'title': 'Machine Learning with Python',
                'author': 'Robert Taylor',
                'isbn': '9781234567896',
                'description': 'Dive into machine learning using Python libraries like scikit-learn and TensorFlow. Learn algorithms, data preprocessing, and model evaluation.',
                'price': Decimal('54.99'),
                'stock_quantity': 12,
                'is_featured': False,
            },
            {
                'title': 'Data Structures and Algorithms',
                'author': 'Lisa Anderson',
                'isbn': '9781234567897',
                'description': 'Master fundamental data structures and algorithms. Essential reading for programming interviews and efficient software development.',
                'price': Decimal('49.99'),
                'stock_quantity': 18,
                'is_featured': True,
            },
            {
                'title': 'Git Version Control',
                'author': 'Mark Thompson',
                'isbn': '9781234567898',
                'description': 'Learn Git version control system from basics to advanced techniques. Perfect for developers working in teams and managing code repositories.',
                'price': Decimal('19.99'),
                'stock_quantity': 40,
                'is_featured': False,
            },
            {
                'title': 'Web Security Essentials',
                'author': 'Karen Martinez',
                'isbn': '9781234567899',
                'description': 'Understand web security vulnerabilities and how to prevent them. Covers HTTPS, authentication, XSS, CSRF, and other security best practices.',
                'price': Decimal('37.99'),
                'stock_quantity': 22,
                'is_featured': True,
            },
            {
                'title': 'Docker and Containerization',
                'author': 'Alex Rodriguez',
                'isbn': '9781234567800',
                'description': 'Learn Docker containerization technology for modern application deployment. Includes Docker Compose, orchestration, and best practices.',
                'price': Decimal('32.99'),
                'stock_quantity': 28,
                'is_featured': False,
            },
            {
                'title': 'API Design and Development',
                'author': 'Chris Lee',
                'isbn': '9781234567801',
                'description': 'Design and build robust REST APIs. Learn about API documentation, authentication, versioning, and testing strategies.',
                'price': Decimal('41.99'),
                'stock_quantity': 16,
                'is_featured': True,
            },
        ]

        # Create books
        created_count = 0
        for book_data in books_data:
            book, created = Book.objects.get_or_create(
                isbn=book_data['isbn'],
                defaults=book_data
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created book: {book.title}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'Book already exists: {book.title}'
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Created {created_count} new books!'
            )
        )

        # Display summary
        total_books = Book.objects.count()
        featured_books = Book.objects.filter(is_featured=True).count()

        self.stdout.write(
            self.style.SUCCESS(
                f'Total books in database: {total_books}'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'Featured books: {featured_books}'
            )
        )

    def create_superuser_if_needed(self):
        """Create a superuser if none exists"""
        if not User.objects.filter(is_superuser=True).exists():
            self.stdout.write('Creating superuser...')
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            self.stdout.write(
                self.style.SUCCESS('Superuser created: admin/admin123')
            )