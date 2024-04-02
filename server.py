from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_cors import CORS
from getPokemon import get_pokemon, get_pokemon_names
from waitress import serve
import mysql.connector
import os
import bcrypt


app = Flask(__name__)
CORS(app)

app.secret_key = 'password'


db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'passwd': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")
    
@app.route('/register-user', methods=['POST'])
def registerUser():
    username = request.form['username']
    password = request.form['password'].encode('utf-8')

    # Hash the password
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())

    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    try:
        # Insert the new user into the database
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, hashed)
        )
        conn.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('index'))
    except mysql.connector.Error as e:
        # This will catch errors such as "Duplicate entry" and others
        flash(str(e), 'danger')
        return redirect(url_for('register'))
    finally:
        cursor.close()
        conn.close()

@app.route('/register')
def register():
    return render_template('register.html')

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
        statnames = statnames
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