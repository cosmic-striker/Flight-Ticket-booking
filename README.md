# Flight Ticket Booking System

A simple web-based flight ticket booking application built with Flask and Python. This application allows users to sign up, log in, view available flights, and book tickets. Administrators can manage flights through a dedicated dashboard.

## Features

- **User Registration and Login**: Users can create accounts and log in securely.
- **Flight Booking**: Users can view available flights and book tickets.
- **Admin Dashboard**: Administrators can add, view, and manage flight information.
- **Session Management**: Secure user sessions with role-based access.
- **Data Storage**: Uses CSV files for storing user, flight, and booking data.

## Technologies Used

- **Backend**: Python with Flask framework
- **Frontend**: HTML templates with CSS styling
- **Data Storage**: CSV files
- **Session Management**: Flask sessions

## Installation

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd Flight-Ticket-booking
   ```

2. **Install dependencies**:
   ```
   pip install flask
   ```

3. **Run the application**:
   ```
   python app.py
   ```

4. **Access the application**:
   Open your web browser and go to `http://localhost:5000`

## Usage

- **Home Page**: Navigate to the home page to get started.
- **Sign Up**: Create a new user account.
- **Log In**: Log in with your credentials.
- **Booking**: View available flights and book tickets.
- **Admin Dashboard**: Log in as an admin to manage flights.

## Project Structure

```
Flight-Ticket-booking/
├── app.py                 # Main Flask application
├── test.py                # Test file
├── data/
│   ├── users.csv          # User data
│   ├── flights.csv        # Flight data
│   ├── bookings.csv       # Booking data
│   └── database.csv       # Additional database file
├── static/
│   ├── input.css          # Input CSS styles
│   └── output.css         # Output CSS styles
├── templates/
│   ├── home.html          # Home page template
│   ├── login.html         # Login page template
│   ├── signup.html        # Signup page template
│   ├── booking.html       # Booking page template
│   ├── admin.html         # Admin dashboard template
│   └── admin_login.html   # Admin login template
└── README.md              # This file
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.