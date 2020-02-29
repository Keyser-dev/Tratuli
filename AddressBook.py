# File Name: AddressBook.py
# Purpose: Handles data persistence with serialization and deserialzation of JSON encoded data.
# Author: Keyser

import json
import uuid

#=============================================== Functions =====================================================
# creates saved connection entry
def addEntry(e, conn):
    id = str(uuid.uuid4())
    conn[id] = []
    conn[id].append({
        'name': e[0],
        'address': e[1],
        'port': e[2],
        'user': e[3],
        'password': e[4],
        'note': e[5]
    })
    return conn

# encodes connections memory object to JSON file
def serialize(data):
    with open('saved\\connections.json', 'w') as outfile:
        json.dump(data, outfile, ensure_ascii=False)

# decodes JSON file to connections memory object
def deserialize():
    with open('saved\\connections.json', 'r') as json_file:
        data = json.load(json_file)
    return data
