# Shop Management System

A full-stack web application for managing a shop's inventory, sales, and user accounts.

## Features

- User authentication with email verification
- Two-factor authentication (simulated)
- Role-based access control (Admin/User)
- Product management with stock tracking
- Low stock alerts and visualization
- User management dashboard
- Sales tracking and analytics

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- npm (comes with Node.js)
- PostgreSQL (or SQLite for development)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install backend dependencies:
```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
pip install -r requirements.txt
```

3. Install frontend dependencies:
```bash
cd frontend
npm install
```

## Running the Application

The application consists of two parts that need to be run simultaneously in different terminal windows:

### Terminal 1 - Backend Server
```bash
cd backend
# Activate virtual environment if not already activated
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate

# Run the Django development server
python manage.py runserver
```
The backend server will run on http://localhost:8000

### Terminal 2 - Frontend Development Server
```bash
cd frontend
npm start
```
The frontend application will run on http://localhost:3000

## Important Notes

### Two-Factor Authentication
The 2FA system is simulated for demonstration purposes:
- When logging in, you'll be prompted for a 6-digit code
- The verification code will be displayed in the backend terminal
- No actual SMS or email is sent
- This is for testing purposes only

### User Roles
- Admin: Full access to all features including user management
- User: Access to shopping features and personal account management

## Development

### Backend
- Django REST Framework
- JWT Authentication
- PostgreSQL/SQLite Database
- RESTful API endpoints

### Frontend
- React.js
- React Router for navigation
- Chart.js for data visualization
- Axios for API communication
- Context API for state management

## Security Features
- JWT-based authentication
- Password hashing
- Role-based access control
- Email verification (simulated)
- Two-factor authentication (simulated)

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request 