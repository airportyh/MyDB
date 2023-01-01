import unittest
import requests

class TestDatabases(unittest.TestCase):

    def test_list_dbs(self):
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
        response = requests.put('http://127.0.0.1:5000/databases/a_test_db')
        self.assertEqual(response.status_code, 200)
        response = requests.get('http://127.0.0.1:5000/databases')
        dbs = response.json()
        self.assertTrue('a_test_db' in dbs)
        response = requests.delete('http://127.0.0.1:5000/databases/a_test_db')
        self.assertEqual(response.status_code, 200)
        response = requests.get('http://127.0.0.1:5000/databases')
        dbs = response.json()
        self.assertFalse('a_test_db' in dbs)

class TestTables(unittest.TestCase):
    
    def setUp(self):
        response = requests.put('http://127.0.0.1:5000/databases/b_test_db')
        self.assertEqual(response.status_code, 200)
        
    def tearDown(self):
        response = requests.delete('http://127.0.0.1:5000/databases/b_test_db')
        self.assertEqual(response.status_code, 200)
    
    def test_list_tables(self):
        response = requests.get('http://127.0.0.1:5000/databases/b_test_db/tables')
        self.assertEqual(response.json(), [])
    
    def test_create_table(self):
        response = requests.put('http://127.0.0.1:5000/databases/b_test_db/tables/persons')
        self.assertEqual(response.status_code, 200)
        response = requests.get('http://127.0.0.1:5000/databases/b_test_db/tables')
        self.assertEqual(response.json(), ['persons'])
    
    def test_list_columns(self):
        response = requests.put('http://127.0.0.1:5000/databases/b_test_db/tables/persons')
        self.assertEqual(response.status_code, 200)
        response = requests.get('http://127.0.0.1:5000/databases/b_test_db/tables/persons/columns')
        self.assertEqual(response.json(), [{'name': 'id', 'type': 'integer'}])
    
    def test_create_column(self):
        response = requests.put('http://127.0.0.1:5000/databases/b_test_db/tables/persons')
        self.assertEqual(response.status_code, 200)
        response = requests.put('http://127.0.0.1:5000/databases/b_test_db/tables/persons/columns/name', json={
            'type': 'varchar'
        })
        self.assertEqual(response.status_code, 200)
        response = requests.get('http://127.0.0.1:5000/databases/b_test_db/tables/persons/columns')
        self.assertEqual(response.json(), [
            {'name': 'id', 'type': 'integer'},
            {'name': 'name', 'type': 'character varying'},
        ])
    
    def test_delete_column(self):
        response = requests.put('http://127.0.0.1:5000/databases/b_test_db/tables/persons')
        self.assertEqual(response.status_code, 200)
        response = requests.put('http://127.0.0.1:5000/databases/b_test_db/tables/persons/columns/name', json={
            'type': 'varchar'
        })
        self.assertEqual(response.status_code, 200)
        response = requests.delete('http://127.0.0.1:5000/databases/b_test_db/tables/persons/columns/name')
        self.assertEqual(response.status_code, 200)
        response = requests.get('http://127.0.0.1:5000/databases/b_test_db/tables/persons/columns')
        self.assertEqual(response.json(), [{'name': 'id', 'type': 'integer'}])
    
    def test_error_when_creating(self):
        response = requests.put('http://127.0.0.1:5000/databases/b_test_db/tables/persons')
        self.assertEqual(response.status_code, 200)
        response = requests.put('http://127.0.0.1:5000/databases/b_test_db/tables/persons')
        self.assertEqual(response.status_code, 500)
    
    def test_list_rows(self):
        response = requests.put('http://127.0.0.1:5000/databases/b_test_db/tables/persons')
        self.assertEqual(response.status_code, 200)
        response = requests.get('http://127.0.0.1:5000/databases/b_test_db/tables/persons/rows')
        self.assertEqual(response.json(), [])
        
    def test_create_row(self):
        response = requests.put('http://127.0.0.1:5000/databases/b_test_db/tables/persons')
        self.assertEqual(response.status_code, 200)
        response = requests.put('http://127.0.0.1:5000/databases/b_test_db/tables/persons/columns/name', json={
            'type': 'varchar'
        })
        self.assertEqual(response.status_code, 200)
        response = requests.put('http://127.0.0.1:5000/databases/b_test_db/tables/persons/columns/age', json={
            'type': 'integer'
        })
        self.assertEqual(response.status_code, 200)
        response = requests.post('http://127.0.0.1:5000/databases/b_test_db/tables/persons/rows', json={
            'columns': ['name', 'age'],
            'values': ['Jerry', 54]
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), { "id": 1 })
        response = requests.get('http://127.0.0.1:5000/databases/b_test_db/tables/persons/rows')
        self.assertEqual(response.json(), [
            {'age': 54, 'id': 1, 'name': 'Jerry'}
        ])
    
    def test_delete_row(self):
        response = requests.put('http://127.0.0.1:5000/databases/b_test_db/tables/persons')
        self.assertEqual(response.status_code, 200)
        response = requests.put('http://127.0.0.1:5000/databases/b_test_db/tables/persons/columns/name', json={
            'type': 'varchar'
        })
        self.assertEqual(response.status_code, 200)
        response = requests.put('http://127.0.0.1:5000/databases/b_test_db/tables/persons/columns/age', json={
            'type': 'integer'
        })
        self.assertEqual(response.status_code, 200)
        response = requests.post('http://127.0.0.1:5000/databases/b_test_db/tables/persons/rows', json={
            'columns': ['name', 'age'],
            'values': ['Jerry', 54]
        })
        self.assertEqual(response.status_code, 200)
        id = response.json()["id"]
        response = requests.delete('http://127.0.0.1:5000/databases/b_test_db/tables/persons/rows/%s' % id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), { "deleted": True })
        
        response = requests.delete('http://127.0.0.1:5000/databases/b_test_db/tables/persons/rows/%s' % id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), { "deleted": False })
    
    def test_update_row(self):
        response = requests.put('http://127.0.0.1:5000/databases/b_test_db/tables/persons')
        self.assertEqual(response.status_code, 200)
        response = requests.put('http://127.0.0.1:5000/databases/b_test_db/tables/persons/columns/name', json={
            'type': 'varchar'
        })
        self.assertEqual(response.status_code, 200)
        response = requests.put('http://127.0.0.1:5000/databases/b_test_db/tables/persons/columns/age', json={
            'type': 'integer'
        })
        self.assertEqual(response.status_code, 200)
        response = requests.post('http://127.0.0.1:5000/databases/b_test_db/tables/persons/rows', json={
            'columns': ['name', 'age'],
            'values': ['Jerry', 54]
        })
        self.assertEqual(response.status_code, 200)
        id = response.json()["id"]
        response = requests.put('http://127.0.0.1:5000/databases/b_test_db/tables/persons/rows/%s' % id, json={
            'columns': ['name', 'age'],
            'values': ['Jerome', 55]
        })
        self.assertEqual(response.status_code, 200)
        response = requests.get('http://127.0.0.1:5000/databases/b_test_db/tables/persons/rows')
        self.assertEqual(response.json(), [
            {'age': 55, 'id': 1, 'name': 'Jerome'}
        ])

if __name__ == '__main__':
    unittest.main()