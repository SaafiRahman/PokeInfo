from flask import Flask, render_template, request, jsonify, flash, redirect, session, url_for
from flask_cors import CORS
from getPokemon import get_pokemon, get_pokemon_names
from waitress import serve
import mysql.connector
import os
import bcrypt


app = Flask(__name__)
CORS(app)

app.secret_key = os.urandom(16)

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'passwd': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

@app.route('/')
@app.route('/index')
def index():
    username = session.get('username')
    return render_template("index.html", username = username)
    
@app.route('/register-user', methods=['POST'])
def registerUser():
    username = request.form['username']
    password = request.form['password'].encode('utf-8')

    # Hash the password
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())

    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('''SELECT username
                    FROM users WHERE username = %s''', (username,))
    founduser = cursor.fetchone()

    if not founduser:
        try:
            # Insert the new user into the database
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
                (username, hashed)
            )
            conn.commit()
            session['username'] = username
            return redirect(url_for('index'))
        except mysql.connector.Error as e:
            # This will catch errors such as "Duplicate entry" and others
            flash(str(e), 'danger')
            return redirect(url_for('register'))
        finally:
            cursor.close()
            conn.close()
    else:
        flash('Username already exists. Please choose a different one.', 'warning')
        return redirect(url_for('register')) 

@app.route('/login-user', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password'].encode('utf-8')

    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    try:
        # Query the database for the user
        cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        # Check if user was found
        if user is None:
            flash('Username does not exist.', 'warning')
            return redirect(url_for('login'))

        # Retrieve the stored hashed password
        stored_password_hash = user[0]
        if isinstance(stored_password_hash, str):
            stored_password_hash = stored_password_hash.encode('utf-8')

        # Use bcrypt to compare submitted password with the stored hashed password
        if bcrypt.checkpw(password, stored_password_hash):
            flash('Login successful!', 'success')
            session['username'] = username
            # Redirect to a new page (e.g., dashboard) upon successful login
            return redirect(url_for('index'))
        else:
            flash('Password is incorrect.', 'warning')
            return redirect(url_for('login'))
    except mysql.connector.Error as err:
        flash(f'Database error: {err}', 'danger')
        return redirect(url_for('login'))
    finally:
        cursor.close()
        conn.close()


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/search')
def search_mon():
    pokemon_name = request.args.get('search').lower()
    if not pokemon_name:
        return "No Pokemon name provided."

    poke_data = get_pokemon(pokemon_name)
    if not poke_data:
        return "Pokemon not found."

    abilities = [ability['ability']['name'] for ability in poke_data["abilities"]]
    types = [type['type']['name'] for type in poke_data['types']]
    basestats = []
    statnames = []
    for stat in poke_data['stats']:
        basestats.append(stat['base_stat'])
        statnames.append(stat['stat']['name'])
    
    return render_template(
        "pokemon.html",
        title = poke_data["species"]["name"],
        abilities = abilities,
        types = types,
        sprite = poke_data["sprites"]["front_default"],
        basestats = basestats,
        statnames = statnames,
        username = session.get('username')
    )

@app.route('/suggestions')
def get_suggestions():
    keyword = request.args.get('keyword', '').lower()
    if not keyword:
        return jsonify([])  # No keyword provided

    suggestions = get_pokemon_names("pokemon.csv")
    # Filter or process suggestions as needed based on 'keyword'.
    filtered_suggestions = [s for s in suggestions if s.lower().startswith(keyword)]

    return jsonify(filtered_suggestions)

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)