from flask import request, jsonify, Blueprint, current_app
from models import db, user, deposit
import datetime
import jwt

routes_app = Blueprint('routes_app', __name__)

def token_required(f):
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = user.query.get(data["user_id"])
        except:
            return jsonify({"message": "Token is invalid!"}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@routes_app.route("/sign-up", methods=["POST"])
def register():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    number = data.get("number")
    password = data.get("password")

    if not name or not email or not number or not password:
        return jsonify({"message": "Missing required fields!"}), 400

    if (
        user.query.filter_by(email=email).first()
        or user.query.filter_by(number=number).first()
    ):
        return jsonify({"message": "User already exists!"}), 400

    new_user = user(name=name, email=email, number=number, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201

@routes_app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    number = data.get("number")
    password = data.get("password")

    user = user.query.filter((user.email == email) | (user.number == number)).first()

    if not user or not user.check_password(password):
        return jsonify({"message": "Invalid email/number or password!"}), 401

    token = jwt.encode(
        {
            "user_id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
        },
        current_app.config["SECRET_KEY"],
    )

    return jsonify({"message": "Login successful!", "token": token}), 200

@routes_app.route("/deposit", methods=["POST"])
@token_required
def deposit(current_user):
    data = request.get_json()

    amount = data.get("amount")

    if amount < 6000:
        return jsonify({"message": "Minimum deposit amount is 6000!"}), 400

    for i in range(20):
        deposit = deposit(
            user_id=current_user.id, amount=amount, timestamp=datetime.datetime.now()
        )
        db.session.add(deposit)
        db.session.commit()
        multiply_deposit(deposit)

    return jsonify({"message": "Deposit successful!"}), 201

@routes_app.route("/withdraw", methods=["POST"])
@token_required
def withdraw(current_user):
    if datetime.datetime.now() >= current_user.deposits[
        0
    ].timestamp + datetime.timedelta(days=20):
        return jsonify({"message": "Withdrawal successful!"}), 200
    else:
        return jsonify({"message": "Cannot withdraw before 20 days!"}), 400

@routes_app.route("/balance", methods=["GET"])
@token_required
def balance(current_user):
    total_balance = sum(deposit.amount for deposit in current_user.deposits)
    return jsonify({"balance": total_balance}), 200
