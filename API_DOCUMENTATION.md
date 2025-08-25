# EasyRent API Documentation

## Table of Contents
1. [Authentication and Users](#1-authentication-and-users-apiv1users)
2. [Listings](#2-listings-apiv1listings)
3. [Bookings](#3-bookings-apiv1bookings)
4. [API Documentation](#4-api-documentation)

## 1. Authentication and Users (`/api/v1/users/`)

### User Management
- **`POST /api/v1/users/`** - Register a new user
  - **Access:** Anonymous users
  - **Request Body:** New user data
  - **Response:** Registered user data

- **`GET /api/v1/users/`** - List all users
  - **Access:** Administrators only
  - **Response:** List of users

- **`GET /api/v1/users/{id}/`** - Get user details
  - **Access:** Authenticated users (own data) or administrators
  - **Response:** User details

- **`PUT/PATCH /api/v1/users/{id}/`** - Update user information
  - **Access:** Account owner or administrator
  - **Request Body:** Updated data
  - **Response:** Updated user data

- **`DELETE /api/v1/users/{id}/`** - Delete user
  - **Access:** Account owner or administrator

### Authentication
- **`POST /api/v1/users/login/`** - Login
  - **Access:** All users
  - **Request Body:** Username and password
  - **Response:** JWT access and refresh tokens

- **`POST /api/v1/users/logout/`** - Logout
  - **Access:** Authenticated users
  - **Action:** Invalidates the token

### Profile
- **`GET /api/v1/users/my`** - Current user information
  - **Access:** Authenticated users
  - **Response:** Current user's data

- **`POST /api/v1/users/change-password/`** - Change password
  - **Access:** Authenticated users
  - **Request Body:** Current and new password

## 2. Listings (`/api/v1/listings/`)

### Basic Operations
- **`GET /api/v1/listings/`** - List all listings
  - **Access:** All users
  - **Filters:**
    - `min_price`, `max_price` - price range
    - `min_rooms`, `max_rooms` - number of rooms
    - `location` - location search
    - `housing_type` - type of housing
  - **Sorting:** By price (`price`) and creation date (`created_at`)
  - **Response:** List of active listings

- **`POST /api/v1/listings/`** - Create a new listing
  - **Access:** Authenticated landlords
  - **Request Body:** Listing data
  - **Response:** Created listing

- **`GET /api/v1/listings/{id}/`** - Get listing details
  - **Access:** All users
  - **Response:** Listing details with reviews

- **`PUT/PATCH /api/v1/listings/{id}/`** - Update listing
  - **Access:** Listing owner or administrator
  - **Request Body:** Updated data
  - **Response:** Updated listing

- **`DELETE /api/v1/listings/{id}/`** - Delete listing
  - **Access:** Listing owner or administrator

### Additional Actions
- **`GET /api/v1/listings/my_listings/`** - My listings
  - **Access:** Authenticated landlords
  - **Response:** Current user's listings

- **`POST /api/v1/listings/{id}/add_review/`** - Add review
  - **Access:** Authenticated tenants
  - **Request Body:** Review text and rating
  - **Response:** Created review

## 3. Bookings (`/api/v1/bookings/`)

- **`GET /api/v1/bookings/`** - List bookings
  - **Access:** Authenticated users
  - **Response:**
    - Tenants: their bookings
    - Landlords: bookings for their listings
    - Administrators: all bookings

- **`POST /api/v1/bookings/`** - Create booking
  - **Access:** Authenticated tenants
  - **Request Body:** Listing ID, booking dates
  - **Response:** Created booking

- **`GET /api/v1/bookings/{id}/`** - Get booking details
  - **Access:**
    - Tenant (own booking)
    - Landlord (booking for their listing)
    - Administrator

- **`PUT/PATCH /api/v1/bookings/{id}/`** - Update booking
  - **Access:**
    - Tenant (own booking)
    - Administrator
  - **Restrictions:** Can only be updated within certain timeframes

- **`DELETE /api/v1/bookings/{id}/`** - Cancel booking
  - **Access:**
    - Tenant (own booking)
    - Administrator
  - **Restrictions:** Can only be cancelled before a certain date

## 4. API Documentation

- **`GET /api/schema/`** - Get OpenAPI schema
- **`GET /api/schema/swagger/`** - Swagger UI documentation

## General Notes

1. **Authentication:** Required for all endpoints except:
   - User registration
   - Login
   - Viewing listings
   - Viewing listing details

2. **User Roles:**
   - **Tenants** - can book listings and leave reviews
   - **Landlords** - can create and manage listings
   - **Administrators** - full access to all features

3. **Restrictions:**
   - Bookings can only be cancelled before a certain date
   - Only landlords can create listings
   - Only tenants who have booked a listing can leave reviews for it
