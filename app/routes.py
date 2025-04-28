from flask import Blueprint, render_template, request, redirect, url_for, jsonify, abort
from . import db
from .models import Client, Program
from .utils import format_name
from .forms import ClientForm

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/create-program', methods=['GET', 'POST'])
def create_program():
    if request.method == 'POST':
        name = request.form['name']
        program = Program(name=name)
        db.session.add(program)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('create_program.html')

@main.route('/register-client', methods=['GET', 'POST'])
def register_client():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']

        client = Client(name=name, age=age, gender=gender)
        db.session.add(client)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('register_client.html')

@main.route('/enroll-client', methods=['GET', 'POST'])
def enroll_client():
    clients = Client.query.all()
    programs = Program.query.all()

    if request.method == 'POST':
        client_id = int(request.form['client'])
        selected_programs = request.form.getlist('programs')
        client = db.session.get(Client, client_id)
        for pid in selected_programs:
            program = db.session.get(Program, int(pid))
            if program not in client.programs:
                client.programs.append(program)
        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template('enroll_client.html', clients=clients, programs=programs)

@main.route('/search-client', methods=['GET', 'POST'])
def search_client():
    query = request.args.get('q') or request.form.get('q')
    if query:
        clients = Client.query.filter(Client.name.ilike(f"%{query}%")).all()
    else:
        clients = Client.query.all()
    return render_template('search_client.html', clients=clients)

@main.route('/client/<int:client_id>')
def client_profile(client_id):
    client = db.session.get(Client, client_id)
    if client is None:
        abort(404)
    return render_template('client_profile.html', client=client)

@main.route('/api/client/<int:client_id>')
def api_client_profile(client_id):
    client = db.session.get(Client, client_id)
    if client is None:
        abort(404)
    return jsonify({
        'id': client.id,
        'name': client.name,
        'age': client.age,
        'gender': client.gender,
        'programs': [program.name for program in client.programs]
    })