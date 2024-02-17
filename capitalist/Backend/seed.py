import datetime
# from deposit import Deposit
# from models import db  # Import your SQLAlchemy database instance
from models.user import User  # Import the User model
from app import app  # Import your Flask app instance
# Adjust import statements based on the actual directory structure
from Backend.models.deposit import Deposit
from Backend.models.user import User
from Backend.app import app

# Function to seed the database with dummy users
def seed_users():
    # Dummy user data
    users_data = [
        {'name': 'User 1', 'email': 'user1@example.com', 'number': '1234567890', 'password': 'password1'},
        {'name': 'User 2', 'email': 'user2@example.com', 'number': '9876543210', 'password': 'password2'},
        # Add more dummy user data as needed
    ]

    # Create User objects and add them to the database
    for data in users_data:
        user = User(**data)
        db.session.add(user)

    # Commit the changes to the database
    db.session.commit()

# Function to seed the database with dummy deposit history
def seed_deposits():
    # Dummy deposit data
    deposits_data = [
        {'user_id': 1, 'amount': 10000, 'timestamp': datetime.datetime.now()},
        {'user_id': 2, 'amount': 15000, 'timestamp': datetime.datetime.now()},
        # Add more dummy deposit data as needed
    ]

    # Add deposit records to the database
    for data in deposits_data:
        # Create deposit objects using the Deposit model and add them to the database
        deposit = Deposit(**data)
        db.session.add(deposit)

    # Commit the changes to the database
    db.session.commit()

if __name__ == '__main__':
    # Initialize the Flask app context
    with app.app_context():
        # Create the database tables
        db.create_all()

        # Seed the database with dummy users and deposit history
        seed_users()
        seed_deposits()

        print('Database seeded successfully!')
