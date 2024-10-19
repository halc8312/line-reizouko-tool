# tests/test_app.py

import unittest
from app import app
from models.database import init_db, get_db_connection

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Initialize the database for testing
        init_db()
        self.clear_test_data()

    def tearDown(self):
        # Clear test data after each test
        self.clear_test_data()

    def clear_test_data(self):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM items;")
        cursor.execute("DELETE FROM users;")
        connection.commit()
        cursor.close()
        connection.close()

    def test_hello_endpoint(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), "Hello, LINE Refrigerator Management Tool!")

    def test_register_user(self):
        response = self.app.post('/users/register', json={
            "user_id": "test_user",
            "username": "Test User"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("User registered successfully.", response.data.decode('utf-8'))

    def test_add_item(self):
        # First, register the user
        self.app.post('/users/register', json={
            "user_id": "test_user",
            "username": "Test User"
        })
        # Add an item for the registered user
        response = self.app.post('/fridge/add_item', json={
            "name": "Milk",
            "expiration_date": "2024-12-31",
            "quantity": 2,
            "user_id": "test_user"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("Item added successfully.", response.data.decode('utf-8'))

    def test_add_item_without_user(self):
        # Attempt to add an item without registering the user
        response = self.app.post('/fridge/add_item', json={
            "name": "Milk",
            "expiration_date": "2024-12-31",
            "quantity": 2,
            "user_id": "non_existent_user"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("User does not exist.", response.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()
