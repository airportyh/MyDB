import unittest
import requests

class TestDatabases(unittest.TestCase):

    def test_get_dbs(self):
        response = requests.get('http://127.0.0.1:5000/databases')
        self.assertEqual(response.status_code, 200)
        dbs = response.json()
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertTrue(len(dbs) > 0)
        self.assertEqual(type(dbs), list)
    
    def test_create_and_delete(self):
        response = requests.get('http://127.0.0.1:5000/databases')
        dbs = response.json()
        self.assertFalse('a_test_db' in dbs)
        response = requests.post('http://127.0.0.1:5000/databases', data={'name': 'a_test_db'})
        self.assertEqual(response.status_code, 200)
        response = requests.get('http://127.0.0.1:5000/databases')
        dbs = response.json()
        self.assertTrue('a_test_db' in dbs)
        response = requests.delete('http://127.0.0.1:5000/databases/a_test_db')
        self.assertEqual(response.status_code, 200)
        response = requests.get('http://127.0.0.1:5000/databases')
        dbs = response.json()
        self.assertFalse('a_test_db' in dbs)

if __name__ == '__main__':
    unittest.main()