# File created by Jacob Thomsen, 2 March 2022. Submission due before midnight 9 March 2022
# This program is for the Student Programmer Position coding task. Program requirements:

# 1.    Accept user input of a Pokemon type and return a list of Pokemon of the given type

# 2.    Allow the user to enter a name of a Pokemon. The given name must be from the information returned in step 1

# 3.    Return information for the entered Pokemon name including at least the games the Pokemon are in,
#           all the types of the Pokemon, the name of one of the Pokemon's moves,
#           and one other value of your choice related to the Pokemon.

import json
import requests
from sys import exit


# This function receives user input for a type and checks if type is found on type_list
# If found, it passes input to get_pokemon_of_type()
def type_selection():
    print("Enter a type from the list below:\n")
    for i, poke_type in enumerate(type_list):
        if (i + 1) % 4 == 0:
            print(poke_type + ",")
        elif i == (len(type_list) - 1):
            print(poke_type + ".\n")
        else:
            print(poke_type + ", ", end='')

    user_input_type = input("Type: ")
    user_input_low = user_input_type.lower()  # Convert input to all lowercase, this synthesizes input with lists/API
    print('\n')

    # Check if input matches element from type_list
    valid_input = False
    for poke_type in type_list:
        if user_input_low == (poke_type.lower()):
            valid_input = True
            break

    if valid_input:
        print("\n########################################\n")  # This provides a better command line experience for user
        print("Getting " + user_input_low.title() + " type Pokemon...")
        get_pokemon_of_type(user_input_low)
    else:
        print("\n########################################\n")
        print("\nSorry, I couldn't find any type titled \"" + user_input_low + "\", please try again.\n")
        type_selection()


# GET PokeAPI list of Pokemon with given type
def get_pokemon_of_type(given_type):

    # GET pokemon types from PokeAPI or throw error if issue connecting to PokeAPI
    try:
        response = requests.get("https://pokeapi.co/api/v2/type/" + given_type + "/")
        response_json_str = json.dumps(response.json(), sort_keys=True, indent=4)
        response_json_dict = json.loads(response_json_str)
        response.raise_for_status()
        print("Here are the pokemon with type " + given_type.title() + ":\n")
    except requests.exceptions.HTTPError as err:
        print("\nThere seems to be an issue connecting to PokeAPI.\nPlease restart the program and try again.\n")
        raise SystemExit(err)

    # Print list of all Pokemon of given_type
    for i, val in enumerate(response_json_dict['pokemon']):
        if (i + 1) % 5 == 0:
            print(response_json_dict['pokemon'][i]['pokemon']['name'] + ",")
        elif i == (len(response_json_dict['pokemon']) - 1):
            print(response_json_dict['pokemon'][i]['pokemon']['name'] + "\n")
        else:
            print(response_json_dict['pokemon'][i]['pokemon']['name'] + ", ", end='')

    # Get user input to either select pokemon, restart, or exit program
    print("Here they are!\n\nFrom here you can enter a Pokemon to learn more about them.")
    print("Or you enter 'restart' to pick a new Pokemon type or 'exit' to quit this program\n")
    valid_input = False
    input_low = ""
    while not valid_input:
        input_command = input("Input: ")
        input_low = input_command.lower()

        for i, pokemon in enumerate(response_json_dict['pokemon']):
            if input_low == response_json_dict['pokemon'][i]['pokemon']['name']:
                valid_input = True
                get_pokemon_of_name(input_low)

        if input_low == "restart" or input_low == "exit":
            break
        else:
            print("\nSorry, the input \"" + input_command + "\" doesn't match a Pokemon or either command.")
            print("Please try again.\n")

    if input_low == "restart":
        print("\n########################################\n")
        type_selection()
    elif input_low == "exit":
        print("\nThanks for using PokeAPI Search!\nExiting program now...\n")
        exit(0)


# GET information about pokemon from PokeAPI based on user-input Pokemon
def get_pokemon_of_name(given_name):
    pokemon = given_name.title()
    print("\n########################################\n")
    print ("Looking for " + pokemon + " in the Pokedex\n")

    # GET all data for one pokemon from PokeAPI, or throw error if issue connecting to PokeAPI
    try:
        response = requests.get("https://pokeapi.co/api/v2/pokemon/" + given_name + "/")
        response_json_str = json.dumps(response.json(), sort_keys=True, indent=4)
        response_json_dict = json.loads(response_json_str)
        response.raise_for_status()
        print("Found it, here's some info about " + pokemon + "...\n")
    except requests.exceptions.HTTPError as err:
        print("\nThere seems to be an issue connecting to PokeAPI.\nPlease restart the program and try again.\n")
        raise SystemExit(err)

    # Print pokemon Pokedex reference number
    print("- " + pokemon + " Pokedex reference number: " + str(response_json_dict['id']) + '\n\n')

    # Print game appearances of given pokemon
    print("- Found in these Pokemon game(s): \n\t", end='')
    if len(response_json_dict['game_indices']) == 0:
        print(pokemon + " does not appear in any main title Pokemon games.\n")

    for i, game in enumerate(response_json_dict['game_indices']):
        if (i + 1) % 6 == 0:
            print(response_json_dict['game_indices'][i]['version']['name'].title() + ',\n\t', end='')
        elif i == (len(response_json_dict['game_indices']) - 1):
            print(response_json_dict['game_indices'][i]['version']['name'].title() + "\n\n")
        else:
            print(response_json_dict['game_indices'][i]['version']['name'].title() + ", ", end='')

    # Print pokemon types
    print("- " + pokemon + " is a " + response_json_dict['types'][0]['type']['name'].title(), end='')
    if len(response_json_dict['types']) == 2:
        print("and " + response_json_dict['types'][1]['type']['name'].title(), end='')
    print(" type pokemon.\n\n")

    # Print pokemon's first move
    print("- One of " + pokemon + "'s moves is ", end='')
    print(response_json_dict['moves'][0]['move']['name'] + '\n')
    print("########################################\n")

    # Get user input to either restart or exit program
    print("If you would like to pick a new Pokemon type, enter 'restart'.\nOr enter 'exit' to quit this program.\n ")
    valid_input = False
    input_low = ""
    while not valid_input:
        input_command = input("Input: ")
        input_low = input_command.lower()
        if input_low == "restart" or input_low == "exit":
            break
        else:
            print("Command \"" + input_command + "\" not recognized. Please try again.")

    if input_low == "restart":
        print("\n########################################\n")
        type_selection()
    elif input_low == "exit":
        print("\nThanks for using PokeAPI Search!\nExiting program now...\n")
        exit(0)


# PokeAPI types are constant. This list does not need to be updated from an API GET
type_list = ["Normal", "Fighting", "Flying", "Poison", "Ground", "Bug", "Ghost", "Steel", "Fire",
             "Water", "Grass", "Electric", "Psychic", "Ice", "Dragon", "Dark", "Fairy"]

# INTRODUCTION
print("\nWelcome to PokeAPI Search!\n")
print("This program allows you to search for Pokemon based on type. "
      "From there, you can search for the information of a specific Pokemon.\n")
print("Let's begin!\n")

type_selection()
