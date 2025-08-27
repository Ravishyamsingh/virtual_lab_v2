# Cryptography Virtual Lab - Production-Ready Platform

A comprehensive, secure, and scalable web-based educational platform for teaching cryptographic algorithms through interactive simulations and hands-on exercises.

## 🚀 Features

### 🔐 Advanced Security & Authentication
- **Role-Based Access Control (RBAC)** - Separate interfaces for faculty and students
- **Enhanced Input Validation** - Comprehensive sanitization and validation
- **Session Security** - Secure session management with timeout
- **Audit Logging** - Complete audit trail for all user actions
- **Error Handling** - Robust error handling with user-friendly error pages
- **Security Headers** - OWASP-compliant security headers

### 👥 User Management
- **Faculty Portal** - Administrative dashboard with real-time statistics
- **Student Portal** - Learning-focused interface with progress tracking
- **Dual Login System** - Separate login flows for different user types
- **Session Management** - Secure session handling with role validation

### 📊 Real-Time Dashboard
- **Live Statistics** - Real-time student count, progress tracking
- **Activity Monitoring** - Recent user activities and system events
- **Resource Management** - Dynamic lab module information
- **Quick Actions** - Administrative shortcuts for common tasks

### 🧪 Educational Modules
- **8 Cryptographic Algorithms** - Comprehensive coverage of key concepts
- **Interactive Simulations** - Hands-on learning experiences
- **Progressive Learning** - Structured educational pathways
- **Assignment System** - Practice exercises and assessments

## 🏗️ Architecture

### Application Structure
```
cryptography-virtual-lab/
├── app.py                      # Main application with factory pattern
├── config.py                   # Environment-specific configurations
├── dashboard_stats.py          # Real-time statistics and data
├── auth.py                     # Authentication and authorization
├── requirements.txt            # Python dependencies
├── utils/
│   ├── validators.py           # Input validation and sanitization
│   └── error_handlers.py       # Comprehensive error handling
├── routes/                     # Algorithm-specific routes
│   ├── mono_alphabetic.py      # Mono-alphabetic cipher
│   ├── shift_cipher.py         # Caesar/Shift cipher
│   ├── aes_algorithm.py        # AES encryption
│   ├── des_algorithm.py        # DES encryption
│   ├── hash_function.py        # Cryptographic hashing
│   ├── message_auth.py         # Message authentication
│   ├── dsa_algorithm.py        # Digital signatures
│   ├── one_time_pad.py         # One-time pad cipher
│   └── ciphers/
│       └── mono_alphabetic_cipher.py  # Cipher implementation
├── templates/
│   ├── base.html               # Base template with navigation
│   ├── index.html              # Student dashboard
│   ├── login_selection.html    # Login type selection
│   ├── login.html              # Student login
│   ├── faculty_login.html      # Faculty login
│   ├── faculty_dashboard.html  # Faculty dashboard
│   ├── errors/                 # Error page templates
│   └── pages/                  # Algorithm-specific pages
├── static/
│   ├── css/                    # Stylesheets
│   └── js/                     # JavaScript files
├── data/
│   └── users.json              # User database (JSON-based)
└── logs/                       # Application logs
```

### Key Components

#### 1. Application Factory (`app.py`)
- **Factory Pattern** - Configurable app creation
- **Blueprint Registration** - Modular route organization
- **Error Handler Integration** - Centralized error management
- **Configuration Loading** - Environment-specific settings

#### 2. Configuration Management (`config.py`)
- **Environment Configs** - Development, Testing, Production
- **Security Settings** - CSRF, session security, headers
- **Feature Flags** - Enable/disable functionality
- **Logging Configuration** - Structured logging setup

#### 3. Authentication System (`auth.py`)
- **Role-Based Decorators** - `@faculty_required`, `@student_required`
- **Session Validation** - Secure session management
- **User Lookup** - Efficient user data retrieval
- **Credential Verification** - Secure password checking

#### 4. Validation Framework (`utils/validators.py`)
- **Input Sanitization** - XSS and injection prevention
- **Data Validation** - Username, email, password validation
- **Security Validation** - File upload and URL validation
- **Form Decorators** - Automated validation for routes

#### 5. Error Handling (`utils/error_handlers.py`)
- **Centralized Logging** - Structured error logging
- **User-Friendly Pages** - Custom error templates
- **Security Logging** - Separate security event logs
- **Error Recovery** - Graceful error handling

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Quick Start
```bash
# Clone the repository
git clone <repository-url>
cd cryptography-virtual-lab

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables (optional)
export FLASK_ENV=development
export SECRET_KEY=your-secret-key-here

# Run the application
python app.py
```

### Environment Configuration
Create a `.env` file for environment-specific settings:
```env
FLASK_ENV=development
SECRET_KEY=your-super-secret-key-change-in-production
SESSION_TIMEOUT_HOURS=1
LOG_LEVEL=INFO
ENABLE_REGISTRATION=False
ENABLE_API=False
```

## 👤 User Accounts

### Faculty Accounts
- **admin** / **admin123** - Administrator
- **ravishyam121** / **shyam810** - Faculty Member
- **faculty1** / **faculty123** - Dr. John Smith

### Student Accounts
- **user1** / **password123** - Student One
- **user2** / **password456** - Student Two
- **student1** / **student123** - Alice Johnson

## 🔒 Security Features

### Authentication Security
- **Input Validation** - All inputs validated and sanitized
- **Session Security** - Secure session cookies with timeout
- **Role Validation** - Strict role-based access control
- **Audit Logging** - Complete authentication audit trail

### Application Security
- **CSRF Protection** - Cross-site request forgery prevention
- **XSS Prevention** - Input sanitization and output encoding
- **Security Headers** - OWASP-recommended HTTP headers
- **Error Handling** - No sensitive information in error messages

### Data Security
- **Input Sanitization** - Prevent injection attacks
- **Session Management** - Secure session handling
- **Logging Security** - No sensitive data in logs
- **File Upload Security** - Secure file handling (when enabled)

## 📊 Monitoring & Logging

### Log Files
- **`logs/app.log`** - General application logs
- **`logs/error.log`** - Error and exception logs
- **`logs/security.log`** - Security events and violations
- **`logs/auth.log`** - Authentication and authorization events

### Monitoring Features
- **Real-time Statistics** - Live user and system metrics
- **Activity Tracking** - User action monitoring
- **Error Tracking** - Comprehensive error logging
- **Performance Metrics** - System performance monitoring

## 🧪 Available Lab Modules

### Classical Ciphers
1. **Mono Alphabetic Cipher** - Substitution cipher with frequency analysis
2. **Shift Cipher (Caesar)** - Classical shift cipher with cryptanalysis
3. **One Time Pad** - Theoretically unbreakable encryption

### Modern Cryptography
4. **AES Algorithm** - Advanced Encryption Standard
5. **DES Algorithm** - Data Encryption Standard
6. **Hash Functions** - Cryptographic hashing and integrity
7. **Message Authentication** - MACs, HMACs, and digital signatures
8. **DSA Algorithm** - Digital Signature Algorithm

### Educational Structure
Each module includes:
- **Aim** - Learning objectives
- **Theory** - Conceptual explanations
- **Procedure** - Step-by-step instructions
- **Simulation** - Interactive tools
- **Assignment** - Practice exercises
- **References** - Additional resources

## 🚀 Production Deployment

### Environment Setup
```bash
# Set production environment
export FLASK_ENV=production
export SECRET_KEY=your-production-secret-key
export SESSION_COOKIE_SECURE=True
export DATABASE_URL=your-database-url

# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
```

### Security Checklist
- [ ] Change default secret key
- [ ] Enable HTTPS in production
- [ ] Set secure session cookies
- [ ] Configure proper logging
- [ ] Set up database backups
- [ ] Enable rate limiting
- [ ] Configure security headers
- [ ] Set up monitoring

## 🔧 Configuration Options

### Security Configuration
```python
# Session Security
SESSION_COOKIE_SECURE = True      # HTTPS only
SESSION_COOKIE_HTTPONLY = True    # No JavaScript access
SESSION_COOKIE_SAMESITE = 'Lax'   # CSRF protection
PERMANENT_SESSION_LIFETIME = 3600  # 1 hour timeout

# CSRF Protection
WTF_CSRF_ENABLED = True
WTF_CSRF_TIME_LIMIT = 3600

# Security Headers
SECURITY_HEADERS = {
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'X-XSS-Protection': '1; mode=block',
    'Strict-Transport-Security': 'max-age=31536000'
}
```

### Feature Flags
```python
# Authentication Features
ENABLE_REGISTRATION = False
ENABLE_PASSWORD_RESET = False
ENABLE_TWO_FACTOR_AUTH = False

# Lab Features
ENABLE_FILE_UPLOAD = True
ENABLE_PROGRESS_TRACKING = True
ENABLE_ASSIGNMENTS = True

# Administrative Features
ENABLE_USER_MANAGEMENT = True
ENABLE_SYSTEM_MONITORING = True
ENABLE_AUDIT_LOGS = True
```

## 📈 Performance & Scalability

### Current Capabilities
- **Concurrent Users** - Supports multiple simultaneous users
- **Session Management** - Efficient session handling
- **Real-time Updates** - Live dashboard statistics
- **Responsive Design** - Mobile and desktop compatible

### Scalability Features
- **Application Factory** - Easy horizontal scaling
- **Modular Architecture** - Component-based design
- **Configuration Management** - Environment-specific settings
- **Database Ready** - Prepared for database migration

## 🤝 Contributing

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt

# Run in development mode
export FLASK_ENV=development
python app.py

# Run tests
pytest

# Code formatting
black .
flake8 .
```

### Code Quality
- **Type Hints** - Python type annotations
- **Documentation** - Comprehensive docstrings
- **Error Handling** - Robust exception handling
- **Testing** - Unit and integration tests
- **Security** - Security-first development

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- **Email** - support@cryptolab.edu
- **Documentation** - See inline code documentation
- **Issues** - Check application logs for troubleshooting

## 🔄 Version History

### v1.0.0 (Current)
- ✅ Role-based authentication system
- ✅ Faculty and student portals
- ✅ Real-time dashboard statistics
- ✅ Comprehensive error handling
- ✅ Security hardening
- ✅ Audit logging system
- ✅ 8 cryptographic lab modules
- ✅ Production-ready configuration

### Planned Features
- 🔄 Database integration (SQLAlchemy)
- 🔄 REST API endpoints
- 🔄 Advanced user management
- 🔄 Progress tracking system
- 🔄 Assignment submission system
- 🔄 Email notifications
- 🔄 Advanced analytics
- 🔄 Mobile application

---

**Built with ❤️ for cryptography education**