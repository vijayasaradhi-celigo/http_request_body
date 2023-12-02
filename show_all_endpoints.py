import json
import os

name_to_id_file = "name_to_id.json"
CONNECTOR_DIR = "../httpconnectors"

with open(name_to_id_file, "r") as fp:
    name_to_id = json.loads(fp.read())

# print(name_to_id)
for connector_name, connector_id in name_to_id.items():
    connector_filename = "{}.json".format(connector_id)

    full_path = os.path.join(CONNECTOR_DIR, connector_filename)
    print("Full path={}".format(full_path))

    fp = open(full_path, "r")
    content = fp.read()
    connector_obj = json.loads(content)

    # print(connector_obj)
    keys = connector_obj.keys()

    httpconnectorendpoints = connector_obj["httpConnectorEndpoints"]
    if len(httpconnectorendpoints) == 0:
        print("No HTTP Connector Endpoints found")
    for endpoint in httpconnectorendpoints:
        name = endpoint["name"]
        method = endpoint["method"]
        relativeURI = endpoint["relativeURI"]
        query_params = endpoint.get("queryParameters")
        if query_params is None:
            params = "None"
        else:
            params = [i["name"] for i in query_params]
        resource_fields = endpoint.get("resourceFields")
        if resource_fields is None:
            fields = None
            fields_len = 0
        else:
            fields = resource_fields[0]["fields"]
            fields_len = len(fields)
        print(
            connector_name,
            name,
            method,
            relativeURI,
            "fields=",
            fields,
            "#fields=",
            fields_len,
        )
