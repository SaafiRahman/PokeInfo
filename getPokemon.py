from dotenv import load_dotenv
from pprint import pprint
from flask import jsonify
import requests
import csv
import os

load_dotenv()

def get_pokemon(pokemon="bulbasaur"):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
    poke_data = requests.get(url).json()

    return poke_data

def get_pokemon_names(file_path):
    try:
        pokemon_array = []
        
        # Open the CSV file for reading
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            # Create a CSV reader object
            csvreader = csv.reader(csvfile)
            # Loop through each row in the CSV
            for row in csvreader:
                # Each row is a list, add the first element (Pokémon name) to our array
                if row:  # Ensure the row is not empty
                    pokemon_array.append(row[0])
        
        return pokemon_array
    
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

if __name__ == "__main__":
    poke = input("please enter a city name: ")
    pokedata = get_pokemon(poke)
    pprint(pokedata)