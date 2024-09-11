import csv
import getpass

# Database file
DATABASE_FILE = 'database.csv'

# Helper function to load specific data types from the database
def load_data(data_type):
    data = []
    with open(DATABASE_FILE, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Type'] == data_type:
                data.append(row)
    return data

# Helper function to save specific data types to the database
def save_data(data_type, data, fieldnames):
    all_data = []
    try:
        with open(DATABASE_FILE, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            all_data = list(reader)
    except FileNotFoundError:
        pass

    # Remove existing entries of the same data type
    all_data = [row for row in all_data if row['Type'] != data_type]
    
    # Add the new data with a 'Type' field
    for row in data:
        row['Type'] = data_type
    all_data.extend(data)

    with open(DATABASE_FILE, 'w', newline='') as csvfile:
        fieldnames_with_type = fieldnames + ['Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames_with_type)
        writer.writeheader()
        writer.writerows(all_data)

# User Sign-up and Login
def signup():
    username = input("Choose a username: ")
    password = getpass.getpass("Choose a password: ")
    users = load_data('user')
    
    for user in users:
        if user['Username'] == username:
            print("Username already exists. Please choose a different one.")
            return
    
    users.append({'Username': username, 'Password': password})
    save_data('user', users, ['Username', 'Password'])
    print(f"User {username} signed up successfully.")

def user_login():
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    
    users = load_data('user')
    for user in users:
        if user['Username'] == username and user['Password'] == password:
            print(f"Welcome {username}!")
            user_menu(username)
            return
    print("Invalid credentials.")

def admin_login():
    username = input("Enter admin username: ")
    password = getpass.getpass("Enter admin password: ")
    
    # Simple hardcoded admin credentials
    if username == 'admin' and password == 'admin':
        print(f"Welcome Admin!")
        admin_menu()
    else:
        print("Invalid credentials.")

# Flight Management (Admin)
def add_flight():
    flight_number = input("Enter flight number: ")
    origin = input("Enter flight origin: ")
    destination = input("Enter flight destination: ")
    date = input("Enter flight date (YYYY-MM-DD): ")
    time = input("Enter flight time (HH:MM): ")
    
    flights = load_data('flight')
    flights.append({
        'Flight Number': flight_number,
        'Origin': origin,
        'Destination': destination,
        'Date': date,
        'Time': time,
        'Seats Available': '60'  # Default seat count
    })
    save_data('flight', flights, ['Flight Number', 'Origin', 'Destination', 'Date', 'Time', 'Seats Available'])
    print(f"Flight {flight_number} added successfully.")

def remove_flight():
    flight_number = input("Enter the flight number to remove: ")
    flights = load_data('flight')
    flights = [flight for flight in flights if flight['Flight Number'] != flight_number]
    save_data('flight', flights, ['Flight Number', 'Origin', 'Destination', 'Date', 'Time', 'Seats Available'])
    print(f"Flight {flight_number} removed successfully.")

def view_bookings():
    flight_number = input("Enter flight number to view bookings: ")
    bookings = load_data('booking')
    
    print(f"\nBookings for Flight {flight_number}:")
    for booking in bookings:
        if booking['Flight Number'] == flight_number:
            print(f"User: {booking['Username']} | Seats Booked: {booking['Seats']}")

# User Actions
def search_flights():
    date = input("Enter flight date (YYYY-MM-DD): ")
    time = input("Enter flight time (HH:MM): ")
    
    flights = load_data('flight')
    matching_flights = [flight for flight in flights if flight['Date'] == date and flight['Time'] == time]
    
    if matching_flights:
        print("\nMatching Flights:")
        for flight in matching_flights:
            print(f"Flight {flight['Flight Number']} from {flight['Origin']} to {flight['Destination']} at {flight['Time']} with {flight['Seats Available']} seats available.")
    else:
        print("No matching flights found.")

def book_flight(username):
    search_flights()
    flight_number = input("Enter flight number to book: ")
    seats = int(input("Enter number of seats to book: "))
    
    flights = load_data('flight')
    for flight in flights:
        if flight['Flight Number'] == flight_number:
            available_seats = int(flight['Seats Available'])
            if available_seats >= seats:
                flight['Seats Available'] = str(available_seats - seats)
                save_data('flight', flights, ['Flight Number', 'Origin', 'Destination', 'Date', 'Time', 'Seats Available'])
                
                # Save booking
                bookings = load_data('booking')
                bookings.append({'Username': username, 'Flight Number': flight_number, 'Seats': str(seats)})
                save_data('booking', bookings, ['Username', 'Flight Number', 'Seats'])
                
                print(f"Successfully booked {seats} seats on Flight {flight_number}.")
            else:
                print(f"Only {available_seats} seats available.")
            return

def my_bookings(username):
    bookings = load_data('booking')
    print(f"\n{username}'s Bookings:")
    for booking in bookings:
        if booking['Username'] == username:
            print(f"Flight: {booking['Flight Number']} | Seats: {booking['Seats']}")

# Menus
def user_menu(username):
    while True:
        print("\nUser Menu:")
        print("1. Search Flights")
        print("2. Book Flight")
        print("3. My Bookings")
        print("4. Logout")
        choice = input("Choose an option: ")
        
        if choice == '1':
            search_flights()
        elif choice == '2':
            book_flight(username)
        elif choice == '3':
            my_bookings(username)
        elif choice == '4':
            print("Logging out...")
            break
        else:
            print("Invalid option. Try again.")

def admin_menu():
    while True:
        print("\nAdmin Menu:")
        print("1. Add Flight")
        print("2. Remove Flight")
        print("3. View Bookings by Flight Number")
        print("4. Logout")
        choice = input("Choose an option: ")
        
        if choice == '1':
            add_flight()
        elif choice == '2':
            remove_flight()
        elif choice == '3':
            view_bookings()
        elif choice == '4':
            print("Logging out...")
            break
        else:
            print("Invalid option. Try again.")

# Main System
def main():
    # Initialize the database CSV if not present
    try:
        with open(DATABASE_FILE, 'r') as file:
            pass
    except FileNotFoundError:
        with open(DATABASE_FILE, 'w', newline='') as csvfile:
            fieldnames = ['Type', 'Username', 'Password', 'Flight Number', 'Origin', 'Destination', 'Date', 'Time', 'Seats', 'Seats Available']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    while True:
        print("\nWelcome to the Flight Booking System!")
        print("1. Sign Up")
        print("2. User Login")
        print("3. Admin Login")
        print("4. Exit")
        choice = input("Choose an option: ")
        
        if choice == '1':
            signup()
        elif choice == '2':
            user_login()
        elif choice == '3':
            admin_login()
        elif choice == '4':
            print("Exiting system.")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == '__main__':
    main()
