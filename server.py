from flask import Flask, render_template, request
from getPokemon import get_pokemon, get_pokemon_names
from waitress import serve

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/search')
def search_mon():
    pokemon_name = request.args.get('search')
    if not pokemon_name:
        return "No Pokemon name provided."

    poke_data = get_pokemon(pokemon_name)
    if not poke_data:
        return "Pokemon not found."

    return render_template(
        "pokemon.html",
        title = poke_data["species"]["name"],
        ability = poke_data["abilities"][0]['ability']['name'],
        sprite = poke_data["sprites"]["front_default"]
    )

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)