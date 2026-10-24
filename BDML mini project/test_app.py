import os
import unittest
from app import app, db, User

class StockPredictionTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()

        with app.app_context():
            db.create_all()
            User.query.filter_by(username='student1').delete()
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            User.query.filter_by(username='student1').delete()
            db.session.commit()
            db.session.remove()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Stock Price Prediction", response.data)
        print("[OK] Home page route tested successfully.")

    def test_registration_and_login(self):
        # Register user
        reg_response = self.client.post('/Register', data={
            'username': 'student1',
            'gender': 'Male',
            'age': '21',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(reg_response.status_code, 200)
        self.assertIn(b"Registered successfully", reg_response.data)
        print("[OK] Registration tested successfully.")

        # Login user
        login_response = self.client.post('/login', data={
            'username': 'student1',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(login_response.status_code, 200)
        self.assertIn(b"Stock Price Predictor", login_response.data)
        self.assertIn(b"Welcome, student1!", login_response.data)
        print("[OK] Login and redirect to dashboard tested successfully.")

        # Predict stock price
        predict_response = self.client.post('/dashboard', data={
            'Open': '1510.50',
            'High': '1535.00',
            'Low': '1498.20',
            'Volume': '1200000'
        }, follow_redirects=True)
        self.assertEqual(predict_response.status_code, 200)
        self.assertIn(b"Predicted Stock Price:", predict_response.data)
        print("[OK] Prediction tested successfully.")

        # Logout
        logout_response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(logout_response.status_code, 200)
        self.assertIn(b"Login", logout_response.data)
        print("[OK] Logout tested successfully.")

if __name__ == '__main__':
    unittest.main()
