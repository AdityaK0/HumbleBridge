# HumbleBridge - Project Overview

## 🏗️ Architecture

HumbleBridge is a FastAPI-based donation platform backend with the following architecture:

### Project Structure
```
humblebridge/
├── core/                    # Core configuration and database
│   ├── __init__.py
│   ├── config.py           # Settings and environment variables
│   └── database.py         # SQLAlchemy setup and session management
├── models/                  # SQLAlchemy database models
│   ├── __init__.py
│   ├── user.py             # User model with roles
│   ├── donation.py         # Donation model with status tracking
│   └── humble_coin.py      # HumbleCoin tracking model
├── schemas/                 # Pydantic request/response schemas
│   ├── __init__.py
│   ├── user.py             # User-related schemas
│   └── donation.py         # Donation-related schemas
├── routes/                  # API route handlers
│   ├── __init__.py
│   ├── auth.py             # Authentication endpoints
│   ├── donations.py        # Donation management endpoints
│   └── profile.py          # User profile endpoints
├── auth/                    # Authentication utilities
│   ├── __init__.py
│   └── jwt.py              # JWT token management
├── main.py                  # FastAPI application entry point
├── requirements.txt         # Python dependencies
├── README.md               # Project documentation
├── API_DOCUMENTATION.md    # Detailed API documentation
├── test_api.py             # API testing script
├── start.sh                # Startup script
└── reset_db.py             # Database reset script
```

## 🔧 Technology Stack

- **Framework**: FastAPI 0.104.1
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT tokens with python-jose
- **Password Hashing**: bcrypt with passlib
- **Validation**: Pydantic 2.5.0
- **Server**: Uvicorn with ASGI
- **Documentation**: Auto-generated Swagger/OpenAPI

## 🎯 Key Features

### 1. User Management
- **Role-based authentication**: Donor, Volunteer, Admin
- **JWT-based authentication**: Secure token-based auth
- **Password hashing**: bcrypt for secure password storage

### 2. Donation System
- **Donation creation**: Donors can create donations
- **Status tracking**: pending → assigned → delivered
- **Category system**: clothes, books, electronics, furniture, food, other
- **Assignment system**: Volunteers can pick up donations

### 3. HumbleCoin Rewards
- **Automatic rewards**: 10 coins per delivered donation
- **Balance tracking**: Integrated with user profiles
- **Future-ready**: Extensible for additional features

### 4. API Features
- **RESTful design**: Clean, predictable endpoints
- **Input validation**: Pydantic schemas for all requests
- **Error handling**: Comprehensive error responses
- **Documentation**: Auto-generated Swagger docs

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip package manager

### Quick Start
1. **Clone and navigate to project**:
   ```bash
   cd humblebridge
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the server**:
   ```bash
   ./start.sh
   # or manually:
   python -m uvicorn main:app --reload
   ```

4. **Access the API**:
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Alternative Docs: http://localhost:8000/redoc

### Development Tools

- **Reset database**: `python reset_db.py`
- **Test API**: `python test_api.py`
- **Start server**: `./start.sh`

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    password_hash VARCHAR NOT NULL,
    role VARCHAR NOT NULL DEFAULT 'donor',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Donations Table
```sql
CREATE TABLE donations (
    id INTEGER PRIMARY KEY,
    item_name VARCHAR NOT NULL,
    category VARCHAR NOT NULL,
    description TEXT,
    pickup_address VARCHAR NOT NULL,
    image_url VARCHAR,
    status VARCHAR NOT NULL DEFAULT 'pending',
    donor_id INTEGER NOT NULL,
    volunteer_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (donor_id) REFERENCES users(id),
    FOREIGN KEY (volunteer_id) REFERENCES users(id)
);
```

### HumbleCoins Table
```sql
CREATE TABLE humble_coins (
    id INTEGER PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL,
    coins INTEGER NOT NULL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## 🔐 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: bcrypt for password security
- **Role-based Access Control**: Different permissions per user role
- **Input Validation**: Pydantic schemas prevent invalid data
- **SQL Injection Protection**: SQLAlchemy ORM with parameterized queries

## 🧪 Testing

The project includes a test script (`test_api.py`) that demonstrates:
- User registration
- Authentication
- Donation creation
- Profile access
- Complete workflow testing

## 📈 Scalability Considerations

### Current Implementation
- SQLite for development and small-scale deployment
- Single-server architecture
- File-based database

### Production Considerations
- **Database**: PostgreSQL or MySQL for production
- **Caching**: Redis for session management
- **Load Balancing**: Multiple server instances
- **File Storage**: Cloud storage for images
- **Monitoring**: Application performance monitoring
- **Security**: HTTPS, rate limiting, input sanitization

## 🔄 API Workflow

### Typical Donation Flow
1. **Donor registers** → Creates account
2. **Donor creates donation** → Item available for pickup
3. **Volunteer views donations** → Sees pending items
4. **Volunteer assigns donation** → Takes responsibility
5. **Volunteer delivers donation** → Marks as delivered
6. **Donor earns coins** → 10 HumbleCoins awarded

## 🛠️ Development Guidelines

### Code Organization
- **Separation of concerns**: Models, schemas, routes separated
- **Dependency injection**: FastAPI's dependency system
- **Type hints**: Full type annotation support
- **Error handling**: Consistent error responses

### Adding New Features
1. **Create model** in `models/` directory
2. **Create schemas** in `schemas/` directory
3. **Create routes** in `routes/` directory
4. **Update imports** in `__init__.py` files
5. **Add to main.py** if needed

### Database Migrations
For production, consider using Alembic for database migrations.

## 🎨 Future Enhancements

### Planned Features
- **Image upload**: Cloud storage integration
- **Notifications**: Email/SMS notifications
- **Maps integration**: Location-based features
- **Analytics**: Donation statistics and reporting
- **Mobile app**: React Native frontend
- **Admin panel**: Web-based administration interface

### Technical Improvements
- **Async operations**: Background task processing
- **WebSocket support**: Real-time updates
- **Microservices**: Service decomposition
- **Containerization**: Docker deployment
- **CI/CD**: Automated testing and deployment

## 📝 License

This project is created for educational and demonstration purposes.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

**HumbleBridge** - Connecting generosity with need through technology. 