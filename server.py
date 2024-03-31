from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from getPokemon import get_pokemon, get_pokemon_names
from waitress import serve


app = Flask(__name__)
CORS(app)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")
    


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
    stats = [stat['base_stat'] for stat in poke_data['stats']]
    
    return render_template(
        "pokemon.html",
        title = poke_data["species"]["name"],
        abilities = abilities,
        types = types,
        sprite = poke_data["sprites"]["front_default"],
        stats = stats
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