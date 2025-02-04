# order-service/test_app.py
import unittest
import requests
import json

class TestOrderService(unittest.TestCase):
    BASE_URL = 'http://localhost:5000'

    def test_list_orders(self):
        response = requests.get(f'{self.BASE_URL}/orders')
        self.assertEqual(response.status_code, 200)
    
    def test_create_order_invalid_product(self):
        # Attempt to create an order with a non-existent product id.
        response = requests.post(f'{self.BASE_URL}/orders',
                                 headers={'Content-Type': 'application/json'},
                                 data=json.dumps({'product_id': 9999, 'quantity': 1}))
        self.assertEqual(response.status_code, 404)
    
    # add more tests (after seeding the DB with known data).

if __name__ == '__main__':
    unittest.main()