from dotenv import load_dotenv
from pprint import pprint
import requests
import csv

load_dotenv()

def get_pokemon(pokemon="bulbasaur"):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
    poke_data = requests.get(url).json()

    return poke_data

def get_pokemon_names():
    pokemon_names = []
    with open('pokemon.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            pokemon_names.append(row['Name'])
    return pokemon_names

if __name__ == "__main__":
    poke = input("please enter a city name: ")
    pokedata = get_pokemon(poke)
    pprint(pokedata)