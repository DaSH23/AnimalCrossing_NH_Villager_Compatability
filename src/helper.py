import sys
import os.path
import json

ROOT_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../")

def load_json(filepath: str):
    with open(os.path.join(ROOT_PATH, filepath)) as json_file:
        json_data = json.load(json_file)
    return json_data

villagers = load_json("data/acnh.json")
SIZE = len(villagers)
# print (villagers)
score_dict = { '♥': 5, '♦': 3, '♣': 2, '×': 1 }

def score_to_int(score_symbol: str):
	return score_dict[score_symbol]

def name_to_index(name: str):
    for i in range(len(villagers)):
        if villagers[i]['Name'] == name:
            return i
        else:
            continue
    print ("Name not found in data! Return -1.")
    return -1

def index_to_name(index: int):
    return villagers[index]['Name']

def check_index(index: int):
    return index != -1 and index <= 391

def issublist(l1: list, l2: list):
    return set(l1) <= set(l2)
