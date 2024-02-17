from flask import Flask, request, jsonify
import datetime
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Dummy user database
users = []

# Dummy deposit history
deposits = []

# Dummy function to multiply deposited amount daily by two
def multiply_deposit(deposit):
    deposit['amount'] *= 2

# JWT Token Required Decorator
def token_required(f):
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = next(user for user in users if user['id'] == data['user_id'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

# Route for user registration
@app.route('/register', methods=['POST'])
def register():
    if request.content_type != 'application/json':
        return jsonify({'error': 'Unsupported Media Type'}), 415
    
    # Process the request body
    data = request.get_json()

    # Extracting user data from request
    name = data.get('name')
    email = data.get('email')
    number = data.get('number')
    password = data.get('password')

    # Perform validations
    if not name or not email or not number or not password:
        return jsonify({'message': 'Missing required fields!'}), 400

    # Check if user already exists
    if any(user['email'] == email or user['number'] == number for user in users):
        return jsonify({'message': 'User already exists!'}), 400

    # Create user dictionary and add to users list
    user_id = len(users) + 1
    user = {'id': user_id, 'name': name, 'email': email, 'number': number, 'password': password}
    users.append(user)

    # Generate JWT token
    token = jwt.encode({'user_id': user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)}, app.config['SECRET_KEY'])

    return jsonify({'message': 'User registered successfully!', 'token': token}), 201

# Route for user login
@app.route('/login', methods=['POST'])
def login():
    if request.content_type != 'application/json':
        return jsonify({'error': 'Unsupported Media Type'}), 415
    
    data = request.get_json()

    email = data.get('email')
    number = data.get('number')
    password = data.get('password')

    # Find user by email/number
    user = next((user for user in users if (user['email'] == email or user['number'] == number) and user['password'] == password), None)

    if not user:
        return jsonify({'message': 'Invalid email/number or password!'}), 401

    # Generate JWT token
    token = jwt.encode({'user_id': user['id'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)}, app.config['SECRET_KEY'])

    return jsonify({'message': 'Login successful!', 'token': token}), 200

# Route for deposit
@app.route('/deposit', methods=['POST'])
@token_required
def deposit(current_user):
    if request.content_type != 'application/json':
        return jsonify({'error': 'Unsupported Media Type'}), 415
    
    data = request.get_json()

    amount = data.get('amount')

    # Dummy minimum deposit check
    if amount < 6000:
        return jsonify({'message': 'Minimum deposit amount is 6000!'}), 400

    # Dummy logic to multiply deposited amount for 20 days
    for i in range(20):
        deposit = {'user_id': current_user['id'], 'amount': amount, 'timestamp': datetime.datetime.now()}
        deposits.append(deposit)
        multiply_deposit(deposit)

    return jsonify({'message': 'Deposit successful!'}), 201

# Route for withdrawal
@app.route('/withdraw', methods=['POST'], endpoint='withdraw_endpoint')
@token_required
def withdraw(current_user):
    if request.content_type != 'application/json':
        return jsonify({'error': 'Unsupported Media Type'}), 415
    
    # Your view function code here
    # Dummy logic for withdrawal after 20 days
    if datetime.datetime.now() >= deposits[0]['timestamp'] + datetime.timedelta(days=20):
        # Logic for withdrawal
        return jsonify({'message': 'Withdrawal successful!'}), 200
    else:
        return jsonify({'message': 'Cannot withdraw before 20 days!'}), 400

# Route for viewing account balance
@app.route('/balance', methods=['GET'], endpoint='balance_endpoint')  # Rename the endpoint to avoid conflict
@token_required
def balance(current_user):
    # Dummy logic to calculate account balance
    total_balance = sum(deposit['amount'] for deposit in deposits if deposit['user_id'] == current_user['id'])
    return jsonify({'balance': total_balance}), 200

if __name__ == '__main__':
    app.run(debug=True)
