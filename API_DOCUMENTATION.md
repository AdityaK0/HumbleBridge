# HumbleBridge API Documentation

## Overview

HumbleBridge is a donation platform API that connects donors with volunteers to deliver items to those in need. The API supports user authentication, donation management, and a HumbleCoin reward system.

## Base URL
```
http://localhost:8000
```

## Authentication

All protected endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### 1. Authentication

#### Register User
```http
POST /register
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "role": "donor"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "role": "donor",
  "created_at": "2024-01-01T00:00:00",
  "coins": 0
}
```

#### Login
```http
POST /login
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 2. User Profile

#### Get Profile
```http
GET /profile
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "role": "donor",
  "created_at": "2024-01-01T00:00:00",
  "coins": 10
}
```

### 3. Donations

#### Create Donation (Donor only)
```http
POST /donate
```

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "item_name": "Winter Jacket",
  "category": "clothes",
  "description": "Warm winter jacket in good condition",
  "pickup_address": "123 Main St, City, State",
  "image_url": "https://example.com/jacket.jpg"
}
```

**Response:**
```json
{
  "id": 1,
  "item_name": "Winter Jacket",
  "category": "clothes",
  "description": "Warm winter jacket in good condition",
  "pickup_address": "123 Main St, City, State",
  "image_url": "https://example.com/jacket.jpg",
  "status": "pending",
  "donor_id": 1,
  "volunteer_id": null,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

#### List Donations (Volunteer/Admin only)
```http
GET /donations
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
[
  {
    "id": 1,
    "item_name": "Winter Jacket",
    "category": "clothes",
    "description": "Warm winter jacket in good condition",
    "pickup_address": "123 Main St, City, State",
    "image_url": "https://example.com/jacket.jpg",
    "status": "pending",
    "donor_id": 1,
    "volunteer_id": null,
    "created_at": "2024-01-01T00:00:00"
  }
]
```

#### Get My Donations
```http
GET /my-donations
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
[
  {
    "id": 1,
    "item_name": "Winter Jacket",
    "category": "clothes",
    "description": "Warm winter jacket in good condition",
    "pickup_address": "123 Main St, City, State",
    "image_url": "https://example.com/jacket.jpg",
    "status": "pending",
    "donor_id": 1,
    "volunteer_id": null,
    "created_at": "2024-01-01T00:00:00"
  }
]
```

#### Assign Donation (Volunteer/Admin only)
```http
POST /donations/{donation_id}/assign
```

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "volunteer_id": 2
}
```

**Response:**
```json
{
  "id": 1,
  "item_name": "Winter Jacket",
  "category": "clothes",
  "description": "Warm winter jacket in good condition",
  "pickup_address": "123 Main St, City, State",
  "image_url": "https://example.com/jacket.jpg",
  "status": "assigned",
  "donor_id": 1,
  "volunteer_id": 2,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

#### Deliver Donation (Volunteer/Admin only)
```http
POST /donations/{donation_id}/deliver
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "item_name": "Winter Jacket",
  "category": "clothes",
  "description": "Warm winter jacket in good condition",
  "pickup_address": "123 Main St, City, State",
  "image_url": "https://example.com/jacket.jpg",
  "status": "delivered",
  "donor_id": 1,
  "volunteer_id": 2,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

## Data Models

### User Roles
- `donor`: Can create donations and earn HumbleCoins
- `volunteer`: Can view and pick up donations for delivery
- `admin`: Full access to all features

### Donation Categories
- `clothes`: Clothing items
- `books`: Books and educational materials
- `electronics`: Electronic devices
- `furniture`: Furniture items
- `food`: Food items
- `other`: Other miscellaneous items

### Donation Status
- `pending`: Available for assignment
- `assigned`: Assigned to a volunteer
- `delivered`: Successfully delivered
- `cancelled`: Cancelled donation

## HumbleCoin System

- Donors earn 10 HumbleCoins when their donation is marked as delivered
- Coins are tracked in the user profile
- Coins can be used for future features (not implemented in this version)

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Email already registered"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Only donors can create donations"
}
```

### 404 Not Found
```json
{
  "detail": "Donation not found"
}
```

## Example Usage

### Complete Workflow

1. **Register a donor:**
```bash
curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "donor@example.com",
    "password": "password123",
    "role": "donor"
  }'
```

2. **Register a volunteer:**
```bash
curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "volunteer@example.com",
    "password": "password123",
    "role": "volunteer"
  }'
```

3. **Login as donor:**
```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "donor@example.com",
    "password": "password123"
  }'
```

4. **Create a donation:**
```bash
curl -X POST "http://localhost:8000/donate" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "item_name": "Winter Jacket",
    "category": "clothes",
    "description": "Warm winter jacket in good condition",
    "pickup_address": "123 Main St, City, State"
  }'
```

5. **Login as volunteer and view donations:**
```bash
curl -X GET "http://localhost:8000/donations" \
  -H "Authorization: Bearer <volunteer_token>"
```

6. **Assign donation to volunteer:**
```bash
curl -X POST "http://localhost:8000/donations/1/assign" \
  -H "Authorization: Bearer <volunteer_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "volunteer_id": 2
  }'
```

7. **Mark donation as delivered:**
```bash
curl -X POST "http://localhost:8000/donations/1/deliver" \
  -H "Authorization: Bearer <volunteer_token>"
```

8. **Check donor's HumbleCoins:**
```bash
curl -X GET "http://localhost:8000/profile" \
  -H "Authorization: Bearer <donor_token>"
```

## Interactive Documentation

Visit the following URLs for interactive API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc 