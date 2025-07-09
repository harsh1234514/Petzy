from django.core.management.base import BaseCommand
from products.models import Category, Product
from decimal import Decimal


class Command(BaseCommand):
    help = 'Create sample data for the ecommerce site'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample data...'))

        # Create categories
        categories_data = [
            {
                'name': 'Electronics',
                'slug': 'electronics',
                'description': 'Latest electronics and gadgets'
            },
            {
                'name': 'Clothing',
                'slug': 'clothing',
                'description': 'Fashion and clothing items'
            },
            {
                'name': 'Books',
                'slug': 'books',
                'description': 'Books and literature'
            },
            {
                'name': 'Home & Garden',
                'slug': 'home-garden',
                'description': 'Home decoration and garden items'
            },
            {
                'name': 'Sports',
                'slug': 'sports',
                'description': 'Sports and fitness equipment'
            }
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            categories[cat_data['slug']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create products
        products_data = [
            {
                'name': 'Smartphone X1',
                'slug': 'smartphone-x1',
                'description': 'Latest smartphone with advanced features and high-quality camera.',
                'price': Decimal('699.99'),
                'category': 'electronics',
                'stock': 50,
                'featured': True
            },
            {
                'name': 'Wireless Headphones',
                'slug': 'wireless-headphones',
                'description': 'Premium wireless headphones with noise cancellation.',
                'price': Decimal('199.99'),
                'category': 'electronics',
                'stock': 30,
                'featured': True
            },
            {
                'name': 'Laptop Pro',
                'slug': 'laptop-pro',
                'description': 'High-performance laptop for professionals and gamers.',
                'price': Decimal('1299.99'),
                'category': 'electronics',
                'stock': 15,
                'featured': False
            },
            {
                'name': 'Cotton T-Shirt',
                'slug': 'cotton-t-shirt',
                'description': 'Comfortable 100% cotton t-shirt in various colors.',
                'price': Decimal('29.99'),
                'category': 'clothing',
                'stock': 100,
                'featured': True
            },
            {
                'name': 'Denim Jeans',
                'slug': 'denim-jeans',
                'description': 'Classic denim jeans with modern fit.',
                'price': Decimal('79.99'),
                'category': 'clothing',
                'stock': 75,
                'featured': False
            },
            {
                'name': 'Winter Jacket',
                'slug': 'winter-jacket',
                'description': 'Warm and stylish winter jacket for cold weather.',
                'price': Decimal('149.99'),
                'category': 'clothing',
                'stock': 25,
                'featured': True
            },
            {
                'name': 'Python Programming Book',
                'slug': 'python-programming-book',
                'description': 'Comprehensive guide to Python programming for beginners.',
                'price': Decimal('49.99'),
                'category': 'books',
                'stock': 40,
                'featured': False
            },
            {
                'name': 'Web Development Guide',
                'slug': 'web-development-guide',
                'description': 'Complete guide to modern web development.',
                'price': Decimal('59.99'),
                'category': 'books',
                'stock': 35,
                'featured': True
            },
            {
                'name': 'Coffee Table',
                'slug': 'coffee-table',
                'description': 'Modern wooden coffee table for living room.',
                'price': Decimal('299.99'),
                'category': 'home-garden',
                'stock': 10,
                'featured': False
            },
            {
                'name': 'Garden Plant Set',
                'slug': 'garden-plant-set',
                'description': 'Set of beautiful plants for your garden.',
                'price': Decimal('89.99'),
                'category': 'home-garden',
                'stock': 20,
                'featured': True
            },
            {
                'name': 'Yoga Mat',
                'slug': 'yoga-mat',
                'description': 'Premium yoga mat for exercise and meditation.',
                'price': Decimal('39.99'),
                'category': 'sports',
                'stock': 60,
                'featured': False
            },
            {
                'name': 'Running Shoes',
                'slug': 'running-shoes',
                'description': 'Comfortable running shoes for daily exercise.',
                'price': Decimal('119.99'),
                'category': 'sports',
                'stock': 45,
                'featured': True
            }
        ]

        for prod_data in products_data:
            category = categories[prod_data.pop('category')]
            product, created = Product.objects.get_or_create(
                slug=prod_data['slug'],
                defaults={**prod_data, 'category': category}
            )
            if created:
                self.stdout.write(f'Created product: {product.name}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created sample data! '
                f'Categories: {len(categories_data)}, '
                f'Products: {len(products_data)}'
            )
        )