import os
import joblib
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, flash 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'site.db')

app = Flask(__name__) 
app.config['SECRET_KEY'] = '1233444545555'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}" 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app) 
login_manager.login_view = 'login'

def init_db():
    """Ensure database tables exist at all times."""
    with app.app_context():
        db.create_all()

# --- Models ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False) 
    password = db.Column(db.String(150), nullable=False)
    gender = db.Column(db.String(20), nullable=True)
    age = db.Column(db.Integer, nullable=True)

@login_manager.user_loader 
def load_user(user_id):
    return db.session.get(User, int(user_id)) if hasattr(db.session, 'get') else User.query.get(int(user_id))

# --- Routes ---
@app.route('/') 
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/Register', methods=['GET', 'POST']) 
@app.route('/register', methods=['GET', 'POST'])
def register():
    init_db()
    if request.method == 'POST':
        username = request.form.get('username') 
        password = request.form.get('password')
        gender = request.form.get('gender')
        age = request.form.get('age')

        existing = User.query.filter_by(username=username).first() 
        if existing:
            flash('User already exists', 'error') 
            return redirect(url_for('register'))

        user = User(
            username=username, 
            password=password,
            gender=gender,
            age=int(age) if age and age.isdigit() else None
        ) 
        db.session.add(user)
        db.session.commit()
        flash('Registered successfully', 'success') 
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST']) 
@app.route('/Login', methods=['GET', 'POST'])
def login():
    init_db()
    if request.method == 'POST':
        username = request.form.get('username') 
        password = request.form.get('password')
        user = User.query.filter_by(username=username, password=password).first() 
        if user:
            login_user(user)
            return redirect(url_for('dashboard')) 
        flash('Invalid credentials', 'error')
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST']) 
@login_required
def dashboard(): 
    prediction_text = ""
    if request.method == 'POST': 
        try:
            open_price = float(request.form.get('Open', 0)) 
            high = float(request.form.get('High', 0))
            low = float(request.form.get('Low', 0))
            volume = float(request.form.get('Volume', 0))

            # Use the trained Linear Regression model if available
            model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
            if os.path.exists(model_path):
                import pandas as pd
                model = joblib.load(model_path)
                features_df = pd.DataFrame([[open_price, high, low, volume]], 
                                           columns=['Open', 'High', 'Low', 'Volume'])
                predicted_price = float(model.predict(features_df)[0])
            else:
                # Dummy formula fallback from lab manual
                predicted_price = (open_price + high + low) / 3.0

            prediction_text = f"Predicted Stock Price: ₹{predicted_price:.2f}"
        except Exception as e:
            print(f"Prediction calculation error: {e}")
            prediction_text = "Error in calculating prediction. Please verify inputs."

    return render_template('index.html', username=current_user.username, 
                           prediction_text=prediction_text)

@app.route('/logout') 
@login_required
def logout(): 
    logout_user()
    return redirect(url_for('login'))

with app.app_context(): 
    db.create_all()

if __name__ == '__main__': 
    app.run(debug=True, port=5000)
