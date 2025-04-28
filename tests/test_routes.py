import unittest
from flask import Flask
from app import create_app, db
from app.models import Client, Program

class RoutesTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
        self.app_context.pop()

    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the Health Information System', response.data)

    def test_create_program(self):
        response = self.client.post('/create-program', data={'name': 'Malaria'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        program = Program.query.filter_by(name='Malaria').first()
        self.assertIsNotNone(program)

    def test_register_client(self):
        response = self.client.post('/register-client', data={'name': 'John Doe', 'age': 30, 'gender': 'Male'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        client = Client.query.filter_by(name='John Doe').first()
        self.assertIsNotNone(client)

    def test_enroll_client(self):
        # First, create a client and a program
        client = Client(name='Jane Doe', age=25, gender='Female')
        program = Program(name='Diabetes')
        db.session.add_all([client, program])
        db.session.commit()
        # Enroll the client in the program
        response = self.client.post('/enroll-client', data={'client': client.id, 'programs': [program.id]}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(program, client.programs)

    def test_search_client(self):
        # First, create a client
        client = Client(name='Alice Smith', age=99, gender='Female')
        db.session.add(client)
        db.session.commit()
        # Search for the client
        response = self.client.get('/search-client', query_string={'q': 'Alice'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Alice Smith', response.data)

    def test_search_client_no_results(self):
        response = self.client.get('/search-client', query_string={'q': 'Nonexistent'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No clients found', response.data)

    def test_client_profile(self):
        # First, create a client
        client = Client(name='Bob Brown', age=40, gender='Female')
        db.session.add(client)
        db.session.commit()

        response = self.client.get(f'/client/{client.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bob Brown', response.data)

    def test_api_client_profile(self):
        # First, create a client
        client = Client(name='Charlie Black', age=35, gender="Male")
        db.session.add(client)
        program1 = Program(name='Malaria')
        client.programs.append(program1)
        db.session.commit()

        response = self.client.get(f'/api/client/{client.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['name'], 'Charlie Black')
        self.assertEqual(data['age'], 35)
        self.assertEqual(data['gender'], 'Male')
        self.assertIn('Malaria', data['programs'])