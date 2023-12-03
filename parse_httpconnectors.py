import json

filename = "httpconnectors.json"

content = open(filename, "r").read()
json_objs = json.loads(content)
print(json_objs)
keys = json_objs[0].keys()
for key in keys:
    print(key)

name_to_id = {}

for obj in json_objs:
    connector_name = obj["name"]
    connector_id = obj["_id"]
    name_to_id[connector_name] = connector_id
print("Name to id={}".format(name_to_id))
fp = open("name_to_id.json", "w")
fp.write(json.dumps(name_to_id) + "\n")
fp.close()
print("Total connectors={}".format(len(name_to_id)))
url = "https://integrator.io/api/httpconnectors/{}?returnEverything=true"
for i, (key, value) in enumerate(name_to_id.items()):
    if i % 10 == 0:
        print("\n\n")
    print(url.format(value))
