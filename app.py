from flask import Flask, render_template, request, redirect, url_for, session, flash
import csv

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# CSV file paths
USER_CSV = 'data/users.csv'
FLIGHT_CSV = 'data/flights.csv'
BOOKINGS_CSV = 'data/bookings.csv'


# Helper Functions
def read_csv(file_path):
    with open(file_path, 'r') as file:
        return list(csv.DictReader(file))

def write_csv(file_path, data, fieldnames):
    with open(file_path, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(data)

def save_flight_data(flight_data):
    fieldnames = ['flight_id', 'origin', 'destination', 'date', 'time', 'seats']
    write_csv(FLIGHT_CSV, flight_data, fieldnames)

def save_user_data(user_data):
    fieldnames = ['username', 'password', 'role']
    write_csv(USER_CSV, user_data, fieldnames)

def save_booking_data(booking_data):
    fieldnames = ['username', 'flight_id', 'date', 'time']
    write_csv(BOOKINGS_CSV, booking_data, fieldnames)


# Routes

# Home Page
@app.route('/')
def home():
    return render_template('home.html')

# User Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_data = {'username': username, 'password': password, 'role': 'user'}
        save_user_data(user_data)
        flash('User registered successfully!')
        return redirect(url_for('login'))
    return render_template('signup.html')

# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = read_csv(USER_CSV)
        for user in users:
            if user['username'] == username and user['password'] == password:
                session['username'] = username
                session['role'] = user['role']
                if user['role'] == 'admin':
                    return redirect(url_for('admin_dashboard'))
                else:
                    return redirect(url_for('booking'))
        flash('Invalid credentials, please try again!')
    return render_template('login.html')

# Admin Login
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    return redirect(url_for('login'))

# User Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    flash('You have been logged out!')
    return redirect(url_for('login'))

# User Booking Page
@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if 'username' in session and session['role'] == 'user':
        flights = read_csv(FLIGHT_CSV)
        if request.method == 'POST':
            flight_id = request.form['flight_id']
            for flight in flights:
                if flight['flight_id'] == flight_id and int(flight['seats']) > 0:
                    flight['seats'] = str(int(flight['seats']) - 1)
                    save_flight_data(flight)
                    booking_data = {
                        'username': session['username'],
                        'flight_id': flight_id,
                        'date': flight['date'],
                        'time': flight['time']
                    }
                    save_booking_data(booking_data)
                    flash('Booking successful!')
                    return redirect(url_for('my_bookings'))
            flash('Flight not available or full.')
        return render_template('booking.html', flights=flights)
    flash('Please log in first!')
    return redirect(url_for('login'))

# User My Bookings
@app.route('/my_bookings')
def my_bookings():
    if 'username' in session and session['role'] == 'user':
        bookings = read_csv(BOOKINGS_CSV)
        user_bookings = [booking for booking in bookings if booking['username'] == session['username']]
        return render_template('my_bookings.html', bookings=user_bookings)
    flash('Please log in first!')
    return redirect(url_for('login'))

# Admin Dashboard
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'username' in session and session['role'] == 'admin':
        flights = read_csv(FLIGHT_CSV)
        return render_template('admin.html', flights=flights)
    flash('Admin login required!')
    return redirect(url_for('admin_login'))

# Add Flight
@app.route('/add_flight', methods=['POST'])
def add_flight():
    if 'username' in session and session['role'] == 'admin':
        flight_data = {
            'flight_id': request.form['flight_id'],
            'origin': request.form['origin'],
            'destination': request.form['destination'],
            'date': request.form['date'],
            'time': request.form['time'],
            'seats': '60'  # Default seat count is 60
        }
        save_flight_data(flight_data)
        flash('Flight added successfully!')
        return redirect(url_for('admin_dashboard'))
    flash('Admin login required!')
    return redirect(url_for('admin_login'))

# Remove Flight
@app.route('/remove_flight/<flight_id>')
def remove_flight(flight_id):
    if 'username' in session and session['role'] == 'admin':
        flights = read_csv(FLIGHT_CSV)
        updated_flights = [flight for flight in flights if flight['flight_id'] != flight_id]
        with open(FLIGHT_CSV, 'w', newline='') as file:
            fieldnames = ['flight_id', 'origin', 'destination', 'date', 'time', 'seats']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_flights)
        flash('Flight removed successfully!')
        return redirect(url_for('admin_dashboard'))
    flash('Admin login required!')
    return redirect(url_for('admin_login'))

# View All Bookings (Admin)
@app.route('/view_bookings/<flight_id>')
def view_bookings(flight_id):
    if 'username' in session and session['role'] == 'admin':
        bookings = read_csv(BOOKINGS_CSV)
        flight_bookings = [booking for booking in bookings if booking['flight_id'] == flight_id]
        return render_template('view_bookings.html', bookings=flight_bookings)
    flash('Admin login required!')
    return redirect(url_for('admin_login'))


if __name__ == '__main__':
    app.run(debug=True)
