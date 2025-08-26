# HumbleBridge - Donation Platform Backend

A FastAPI backend for a donation platform where people can donate items and volunteers can pick them up and deliver them to the needy.

## Features

- **User Management**: Support for Donors, Volunteers, and Admins
- **Donation System**: Create, assign, and track donations
- **HumbleCoin Rewards**: Earn coins for successful donations
- **JWT Authentication**: Secure user authentication
- **RESTful API**: Clean, documented endpoints
- **PostgreSQL Database**: Production-ready database with Alembic migrations

## Quick Start

### Option 1: Docker Database (Recommended)

**Prerequisites**: Docker and Docker Compose installed

1. **Start database service**:
   ```bash
   python docker-manage.py setup
   ```

2. **Run migrations locally**:
   ```bash
   python manage_db.py migrate
   ```

3. **Start the API locally**:
   ```bash
   uvicorn main:app --reload
   ```

4. **Access the API**:
   - API Documentation: http://localhost:8000/docs
   - Alternative Docs: http://localhost:8000/redoc

### Option 2: Local Development

**Prerequisites**: Python 3.8+ and PostgreSQL installed and running

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up PostgreSQL database**:
   ```bash
   # Create database and user (see POSTGRESQL_SETUP.md for details)
   createdb -U postgres -h localhost humble_dev
   psql -U postgres -h localhost -c "CREATE USER addy_rw WITH PASSWORD 'pwd';"
   psql -U postgres -h localhost -c "GRANT ALL PRIVILEGES ON DATABASE humble_dev TO addy_rw;"
   ```

3. **Run database migrations**:
   ```bash
   python manage_db.py setup
   ```

4. **Start the application**:
   ```bash
   uvicorn main:app --reload
   ```

5. **Access the API**:
   - API Documentation: http://localhost:8000/docs
   - Alternative Docs: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /register` - Create a new user account
- `POST /login` - Authenticate and get JWT token

### Donations
- `POST /donate` - Create a new donation (Donor only)
- `GET /donations` - List all donations (Volunteer/Admin)
- `POST /donations/{id}/assign` - Assign donation to volunteer
- `POST /donations/{id}/deliver` - Mark donation as delivered
- `GET /my-donations` - View user's own donations

### User Profile
- `GET /profile` - Get user profile and coin count

## User Roles

- **Donor**: Can create donations and earn HumbleCoins
- **Volunteer**: Can view and pick up donations for delivery
- **Admin**: Full access to all features

## HumbleCoin System

- Donors earn 10 HumbleCoins when their donation is marked as delivered
- Coins can be tracked in the user profile

## Database Schema

- **Users**: id, email, password_hash, role, created_at
- **Donations**: id, item_name, category, description, pickup_address, image_url, status, donor_id, volunteer_id, created_at
- **HumbleCoins**: id, user_id, coins, created_at, updated_at

## Development

The project follows a modular structure:
- `models/` - SQLAlchemy database models
- `schemas/` - Pydantic request/response schemas
- `routes/` - API route handlers
- `core/` - Configuration and utilities
- `auth/` - Authentication utilities

### Database Management

- **Setup database**: `python manage_db.py setup`
- **Create migration**: `python manage_db.py create-migration "Description"`
- **Run migrations**: `python manage_db.py migrate`
- **View history**: `python manage_db.py history`
- **Reset database**: `python manage_db.py reset`

### Development Tools

#### Docker Database Commands
- **Start database**: `python docker-manage.py setup`
- **Stop database**: `docker-compose down`
- **View logs**: `docker-compose logs -f`
- **Database status**: `docker-compose ps`
- **Connect to database**: `docker-compose exec db psql -U addy_rw -d humble_dev`

#### Local Development
- **Start server**: `./start.sh` or `python -m uvicorn main:app --reload`
- **Test API**: `python test_api.py`
- **Reset database**: `python manage_db.py reset` 