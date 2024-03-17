from flask import Flask, render_template, request
from getPokemon import get_pokemon
from waitress import serve

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/search')
def search_mon():
    pokemon = request.args.get('search')
    poke_data = get_pokemon(pokemon)

    return render_template(
        "pokemon.html",
        title = poke_data["species"]["name"],
        ability = poke_data["abilities"][0]['ability']['name'],
        sprite = poke_data["sprites"]["front_default"]
    )

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)