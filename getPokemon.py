from dotenv import load_dotenv
from pprint import pprint
import requests

load_dotenv()

def get_pokemon(pokemon="bulbasaur"):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
    poke_data = requests.get(url).json()

    return poke_data

if __name__ == "__main__":
    poke = input("please enter a city name: ")
    pokedata = get_pokemon(poke)
    pprint(pokedata)