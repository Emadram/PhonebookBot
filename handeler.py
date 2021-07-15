import json
def readfile():
    with open('data.txt') as file_data: 
        new_data = json.load(file_data)
        return new_data