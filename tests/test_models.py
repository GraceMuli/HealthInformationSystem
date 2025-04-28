import unittest
from app import create_app, db
from app.models import Client, Program

class ModelsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
        self.app_context.pop()
        
    def test_client_creation(self):
        client = Client(name='John Doe', age=30,gender='Male')
        db.session.add(client)
        db.session.commit()

        retrieved_client = Client.query.first()
        self.assertIsNotNone(retrieved_client)
        self.assertEqual(retrieved_client.name, 'John Doe')
        self.assertEqual(retrieved_client.age, 30)
        self.assertEqual(retrieved_client.gender, 'Male')

    def test_program_creation(self):
        program = Program(name='Diabetes')
        db.session.add(program)
        db.session.commit()

        retrieved_program = Program.query.first()
        self.assertIsNotNone(retrieved_program)
        self.assertEqual(retrieved_program.name, 'Diabetes')

    def test_program_name_uniqueness(self):
        program1 = Program(name='Hypertension')
        program2 = Program(name='Hypertension')
        db.session.add(program1)
        db.session.commit()
        with self.assertRaises(Exception):
            db.session.add(program2)
            db.session.commit()

    def test_enrollment(self):
        client = Client(name='Jane Doe', age=25, gender='Female')
        program = Program(name='Asthma')
        db.session.add_all([client, program])
        db.session.commit()

        client.programs.append(program)
        db.session.commit()

        enrolled_client = Client.query.first()
        self.assertIn(program, enrolled_client.programs)
        self.assertIn(client, program.clients)

    def test_client_without_name_fails(self):
        client = Client(name=None, age=40, gender='Male')
        db.session.add(client)

        with self.assertRaises(Exception):
            db.session.commit()

    def test_program_without_name_fails(self):
        program = Program(name=None)
        db.session.add(program)

        with self.assertRaises(Exception):
            db.session.commit()