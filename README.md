# Django Ecommerce Website

A complete, modern ecommerce website built with Django, HTML, CSS, and JavaScript. This application provides a full-featured online shopping experience with user authentication, product catalog, shopping cart, and order management.

## 🚀 Features

### Core Features
- **Modern, Responsive Design**: Beautiful UI built with Bootstrap 5 and custom CSS
- **User Authentication**: Registration, login, logout, and profile management
- **Product Catalog**: Browse products with search, filtering, and sorting
- **Shopping Cart**: Add/remove items, update quantities (both AJAX and form-based)
- **Category System**: Organize products by categories
- **Product Reviews**: User ratings and reviews for products
- **Order Management**: Track orders and order history
- **Admin Interface**: Complete Django admin for managing all data

### Technical Features
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **AJAX Functionality**: Dynamic cart operations without page reloads
- **Session Management**: Cart persistence for anonymous users
- **Image Handling**: Product and category images with Pillow
- **Search**: Full-text search across products and categories
- **Pagination**: Efficient pagination for product listings
- **Security**: CSRF protection, user authentication, and secure sessions

## 🛠️ Technology Stack

- **Backend**: Django 5.2.4
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Bootstrap 5.3.0, Font Awesome 6.4.0
- **Database**: SQLite (development) - easily configurable for PostgreSQL/MySQL
- **Image Processing**: Pillow
- **Additional Libraries**: django-crispy-forms, crispy-bootstrap5

## 📋 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation Steps

1. **Clone or Download the Project**
   ```bash
   # If you have the project files, navigate to the project directory
   cd ecommerce-site
   ```

2. **Install Dependencies**
   ```bash
   pip install --break-system-packages -r requirements.txt
   ```

3. **Run Database Migrations**
   ```bash
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```

4. **Create Superuser Account**
   ```bash
   python3 manage.py createsuperuser
   # Follow the prompts to create admin account
   ```

5. **Start Development Server**
   ```bash
   python3 manage.py runserver 0.0.0.0:8000
   ```

6. **Access the Application**
   - Website: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin

## 🏗️ Project Structure

```
ecommerce_site/
├── ecommerce_site/          # Main project settings
│   ├── settings.py          # Django settings
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py             # WSGI configuration
├── core/                   # Core app (home page)
│   ├── views.py            # Home page view
│   └── urls.py             # Core URLs
├── products/               # Products management
│   ├── models.py           # Product, Category, Review models
│   ├── views.py            # Product listing and detail views
│   ├── urls.py             # Product URLs
│   └── admin.py            # Admin configuration
├── cart/                   # Shopping cart functionality
│   ├── models.py           # Cart and CartItem models
│   ├── views.py            # Cart operations (AJAX + forms)
│   ├── context_processors.py # Cart context for templates
│   └── urls.py             # Cart URLs
├── accounts/               # User management
│   ├── models.py           # UserProfile, Address models
│   ├── views.py            # Auth views, profile management
│   └── urls.py             # Account URLs
├── orders/                 # Order management
│   ├── models.py           # Order, OrderItem models
│   ├── views.py            # Order listing and details
│   └── urls.py             # Order URLs
├── templates/              # HTML templates
│   ├── base.html           # Base template
│   ├── core/               # Core app templates
│   ├── products/           # Product templates
│   ├── cart/               # Cart templates
│   └── accounts/           # Account templates
├── static/                 # Static files
│   ├── css/style.css       # Custom CSS
│   └── js/main.js          # Custom JavaScript
├── media/                  # User uploaded files
└── requirements.txt        # Python dependencies
```

## 📖 Usage Guide

### Admin Panel Features
1. **Access Admin**: Navigate to `/admin` and login with superuser credentials
2. **Add Categories**: Create product categories with names and descriptions
3. **Add Products**: Create products with images, descriptions, and pricing
4. **Manage Users**: View and manage user accounts and profiles
5. **View Orders**: Monitor orders and update order statuses

### User Features
1. **Browse Products**: View all products or filter by category
2. **Search**: Use the search bar to find specific products
3. **Product Details**: Click on any product to view detailed information
4. **Add to Cart**: Add products to cart (works for both logged-in and anonymous users)
5. **Manage Cart**: Update quantities or remove items from cart
6. **User Account**: Register, login, and manage profile information
7. **Order History**: View past orders and order details (logged-in users)

### Key URLs
- **Home**: `/` - Homepage with featured products
- **Products**: `/products/` - Product listing with search and filters
- **Product Detail**: `/products/product/<slug>/` - Individual product pages
- **Cart**: `/cart/` - Shopping cart
- **Login**: `/accounts/login/` - User login
- **Register**: `/accounts/register/` - User registration
- **Profile**: `/accounts/profile/` - User profile management
- **Orders**: `/orders/` - Order history
- **Admin**: `/admin/` - Django admin interface

## 🎨 Customization

### Styling
- **Custom CSS**: Edit `static/css/style.css` for styling changes
- **Color Scheme**: Modify CSS variables in `:root` section
- **Layout**: Update Bootstrap classes in templates

### Adding Features
- **Payment Integration**: Add payment processing in checkout views
- **Email Notifications**: Configure email settings for order confirmations
- **Inventory Management**: Extend product models for advanced stock tracking
- **Wishlist**: Add wishlist functionality for users
- **Reviews**: Extend review system with more features

### Configuration
- **Database**: Update `DATABASES` in settings.py for production databases
- **Media Files**: Configure `MEDIA_ROOT` and `MEDIA_URL` for file uploads
- **Static Files**: Set up static file serving for production
- **Email**: Configure email backend for user notifications

## 🚀 Deployment

### Production Considerations
1. **Debug Mode**: Set `DEBUG = False` in production
2. **Secret Key**: Use environment variables for secret key
3. **Database**: Configure PostgreSQL or MySQL for production
4. **Static Files**: Set up static file serving (Nginx, Whitenoise)
5. **Media Files**: Configure media file storage (local or cloud)
6. **Security**: Update `ALLOWED_HOSTS` and security settings

### Environment Variables
Create a `.env` file for sensitive settings:
```
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=your-database-url
ALLOWED_HOSTS=your-domain.com
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

If you encounter any issues or have questions:

1. Check the Django documentation: https://docs.djangoproject.com/
2. Review the project structure and code comments
3. Ensure all dependencies are installed correctly
4. Verify database migrations have been applied

## 🔧 Development

### Adding Sample Data
To add sample categories and products for testing:

1. Access the admin panel at `/admin`
2. Login with your superuser account
3. Add categories in the "Categories" section
4. Add products in the "Products" section
5. Upload images for better visual appeal

### Testing Features
1. **Cart Functionality**: Add items, update quantities, remove items
2. **User Registration**: Create test user accounts
3. **Search**: Test search functionality with product names
4. **Responsive Design**: Test on different screen sizes
5. **Order Flow**: Complete the purchase flow (when payment is implemented)

---

**Created with ❤️ using Django, Bootstrap, and modern web technologies.** 
