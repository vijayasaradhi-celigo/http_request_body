import json
import os
import sys

SOURCE_DIR = "../metadataCreation/assistantMetadata"


def get_all_files_in_dir(directory):
    return os.listdir(directory)


def main1():
    files = get_all_files_in_dir(SOURCE_DIR)
    print("#Total files={}".format(len(files)))
    for file in files:
        parse_metadata(file)


def main():
    parse_metadata("loopreturns.json")


def parse_metadata(filename):
    full_path = os.path.join(SOURCE_DIR, filename)
    fp = open(full_path, "r")
    content = fp.read()
    obj = json.loads(content)

    print(obj)
    print(obj.keys())
    connection = obj["connection"]
    print("Connection")
    print(connection)
    print(connection.keys())
    sys.exit()


if __name__ == "__main__":
    main()
