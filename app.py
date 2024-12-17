from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Create the database
with app.app_context():
    db.create_all()  # Create the database tables if they don't exist

# Sample user data for demonstration
def create_sample_users():
    with app.app_context():
        if User.query.count() == 0:  # Create sample users only if the table is empty
            user1 = User(username='user1', password='pass1')
            user2 = User(username='user2', password='pass2')
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()

create_sample_users()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return jsonify(success=True), 200
    else:
        # Create a new user if the credentials are not found
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(success=True, message='New user created!'), 201

if __name__ == '__main__':
    app.run(debug=True)
