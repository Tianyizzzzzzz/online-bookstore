# Online Bookstore - Django E-commerce Platform

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/django-4.2+-green.svg)
![PostgreSQL](https://img.shields.io/badge/postgresql-13+-blue.svg)
![AWS](https://img.shields.io/badge/aws-compatible-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

A full-featured online bookstore e-commerce platform built with Django, featuring user authentication, shopping cart, order management, and digital book delivery via email.

## 🚀 Features

### Core Features
- **User Authentication**: Registration, login, logout, password reset
- **Book Catalog**: Browse books with search, filtering, and pagination
- **Shopping Cart**: Add/remove items, update quantities
- **Order Management**: Complete checkout process with order tracking
- **Digital Delivery**: Automatic email delivery of eBooks as PDF attachments
- **Admin Panel**: Full administrative interface for managing books and orders

### Technical Features
- **Responsive Design**: Mobile-friendly interface using Bootstrap 5
- **Database**: PostgreSQL for production, SQLite for development
- **Email System**: SMTP email delivery for order confirmations
- **Security**: CSRF protection, secure authentication, input validation
- **Cloud Ready**: AWS S3 integration for static files and media storage
- **Deployment**: Production-ready with Nginx, Gunicorn, and SSL support

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js (for frontend dependencies)
- PostgreSQL (for production)
- Git

## 🛠️ Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/online-bookstore.git
cd online-bookstore
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite for development)
DB_NAME=db.sqlite3

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py init_data  # Creates sample data
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```

Visit `http://localhost:8000` to see the application.

## 📁 Project Structure

```
online_bookstore/
├── manage.py
├── requirements.txt
├── .env.example
├── README.md
├── online_bookstore/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── store/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── context_processors.py
│   ├── management/
│   │   └── commands/
│   │       └── init_data.py
│   ├── templates/
│   │   └── store/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── book_list.html
│   │       ├── book_detail.html
│   │       ├── cart.html
│   │       ├── checkout.html
│   │       ├── order_confirmation.html
│   │       ├── login.html
│   │       └── register.html
│   └── static/
│       └── store/
│           └── css/
│               └── style.css
├── media/
│   └── books/
├── deployment_scripts/
│   └── deploy.sh
└── staticfiles/
```

## 🔧 Configuration

### Database Configuration
For production with PostgreSQL:
```env
ENVIRONMENT=production
DB_NAME=bookstore_db
DB_USER=bookstore_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### Email Configuration
For Gmail SMTP:
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### AWS S3 Configuration (Optional)
```env
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_S3_REGION_NAME=us-east-1
AWS_STORAGE_BUCKET_NAME=your-bucket-name
```

## 📚 Usage

### Admin Panel
1. Access admin panel at `/admin/`
2. Use superuser credentials to log in
3. Manage books, orders, and users

### Customer Flow
1. Browse books at `/books/`
2. Register for an account at `/register/`
3. Add books to cart
4. Complete checkout process
5. Receive order confirmation email with eBook attachments

### Sample Data
The application includes sample data for testing:
- **Books**: 12 programming books with various categories
- **Users**: 
  - Admin: `admin` / `admin123`
  - Demo: `demo` / `demo123`
  - Customer: `customer` / `customer123`

## 🚀 Deployment

### AWS EC2 Deployment
1. **Prepare the deployment script**:
   ```bash
   chmod +x deployment_scripts/deploy.sh
   ```

2. **Update configuration in deploy.sh**:
   - Set your domain name
   - Configure email settings
   - Update GitHub repository URL

3. **Run deployment**:
   ```bash
   ./deployment_scripts/deploy.sh
   ```

### Manual Deployment Steps
1. **Set up server** (Ubuntu 20.04+)
2. **Install dependencies**: Python, PostgreSQL, Nginx
3. **Clone repository** and install Python packages
4. **Configure database** and run migrations
5. **Set up Gunicorn** for WSGI server
6. **Configure Nginx** as reverse proxy
7. **Set up SSL** with Let's Encrypt
8. **Configure firewall** and security

### Environment Variables for Production
```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
ENVIRONMENT=production
```

## 🔐 Security Features

- **CSRF Protection**: All forms protected against CSRF attacks
- **SQL Injection Prevention**: Django ORM prevents SQL injection
- **XSS Protection**: Template auto-escaping enabled
- **Secure Authentication**: Password hashing with Django's built-in system
- **HTTPS Support**: SSL/TLS encryption for production
- **Input Validation**: Form validation on client and server side
- **Rate Limiting**: Fail2ban configuration for brute force protection

## 📧 Email System

The application automatically sends order confirmation emails containing:
- Order details and receipt
- PDF attachments of purchased eBooks
- Customer information
- Download instructions

Email templates are located in `store/templates/store/email/`.

## 🛡️ Testing

### Running Tests
```bash
python manage.py test
```

### Test Coverage
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

### Sample Test Data
Use the management command to create test data:
```bash
python manage.py init_data --clear
```

## 📊 Database Models

### Core Models
- **Book**: Product catalog with title, author, price, stock
- **User**: Django's built-in user model
- **UserProfile**: Extended user information
- **CartItem**: Shopping cart items
- **Order**: Customer orders with shipping info
- **OrderItem**: Individual items within orders

### Model Relationships
- User → UserProfile (One-to-One)
- User → CartItem (One-to-Many)
- User → Order (One-to-Many)
- Order → OrderItem (One-to-Many)
- Book → CartItem (One-to-Many)
- Book → OrderItem (One-to-Many)

## 🎨 Frontend

### Technologies Used
- **Bootstrap 5**: Responsive CSS framework
- **Font Awesome**: Icons and UI elements
- **Custom CSS**: Enhanced styling and animations
- **JavaScript**: Interactive functionality

### Key Features
- Responsive design for mobile/tablet/desktop
- Shopping cart badge with item count
- Search functionality with autocomplete
- Form validation and user feedback
- Loading states and transitions

## 🔄 API Endpoints

### Main URLs
- `/` - Home page
- `/books/` - Book catalog
- `/books/<id>/` - Book detail
- `/cart/` - Shopping cart
- `/checkout/` - Checkout process
- `/register/` - User registration
- `/login/` - User login
- `/admin/` - Admin panel

### AJAX Endpoints
- `/search/` - Book search autocomplete
- `/add-to-cart/<id>/` - Add item to cart
- `/remove-from-cart/<id>/` - Remove from cart

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add comments for complex logic
- Include tests for new features
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## 🆘 Support

### Common Issues
1. **Database Connection**: Check PostgreSQL service and credentials
2. **Email Not Sending**: Verify SMTP settings and app passwords
3. **Static Files**: Run `python manage.py collectstatic`
4. **Permissions**: Check file permissions for media uploads

### Getting Help
- Check the [Issues](https://github.com/your-username/online-bookstore/issues) page
- Review Django documentation
- Contact: support@yourdomain.com

## 📈 Future Enhancements

### Planned Features
- [ ] Product reviews and ratings
- [ ] Wishlist functionality
- [ ] Advanced search filters
- [ ] Payment gateway integration
- [ ] Inventory management
- [ ] Multi-language support
- [ ] Mobile app API
- [ ] Analytics dashboard

### Technical Improvements
- [ ] Redis caching
- [ ] Celery for background tasks
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Monitoring and logging
- [ ] Performance optimization

## 🏆 Project Goals

This project was created as part of an internship at EMRTS to demonstrate:
- Full-stack web development skills
- Django framework proficiency
- Database design and management
- Cloud deployment capabilities
- Security best practices
- Professional code organization

---

**Built with ❤️ for EMRTS Internship Project**

For questions or support, please contact the development team. 
