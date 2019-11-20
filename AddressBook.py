import json

connections = {}
connections['entry'] = []

def addEntry(e):
    connections['entry'].append({
        'name': e[0],
        'address': e[1],
        'port': e[2],
        'user': e[3],
        'password': e[4],
        'note': e[5]
    })
    serialize(connections)

def serialize(data):
    print(data)
    with open('connections.json', 'w') as outfile:
        json.dump(data, outfile, ensure_ascii=False)

def deserialize():
    with open('connections.json') as json_file:
        data = json.load(json_file)
    return data
