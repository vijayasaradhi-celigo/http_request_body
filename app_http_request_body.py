import json
import os
import random

import openai
import pandas as pd
import requests
import streamlit as st
from dotenv import load_dotenv

from automapperlib import (chat_completion_with_function_execution,
                           createPromptWithGenerateAndSources, function_call,
                           functions)

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(layout="wide")
record_id = 1
dataset_filename = "dataset.json"


def load_dataset(filename):
    return json.loads(open(filename, "r").read())


def add_record(obj):
    return {"record": obj}


def get_flattened_keys(prefix, record):
    all_fields = []
    for key, value in record.items():
        print(type(key), type(value), key, value)
        if type(value) is dict:
            fields = get_flattened_keys(key, value)
            all_fields.extend(fields)
        else:
            if prefix == "":
                all_fields.append(key)
            else:
                all_fields.append("{}.{}".format(prefix, key))
    return all_fields


def merge_dicts(dict1, dict2):
    for key, value in dict2.items():
        if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
            merge_dicts(dict1[key], value)
        else:
            dict1[key] = value
    return dict1


def from_flattened(final_obj, flat_key_values_dict):
    obj = {}
    print("Entered from_flatted with {}\n\n".format(flat_key_values_dict))

    for i, (key, value) in enumerate(flat_key_values_dict.items()):
        print("i={} key={} value={}".format(i, key, value))
        if "." in key:
            field_names = key.split(".")
            print("Field names={}".format(field_names))
            obj = create_nested_dict(field_names, value)
            print("Temporary obj={}".format(obj))
        else:
            obj[key] = value

        print("Updating with obj", obj)
        print("Before update final obj={}".format(final_obj))
        final_obj = merge_dicts(final_obj, obj)
        print("After update final obj={}".format(final_obj))
        print("===========\n\n\n")
    print("Returning the final nested dict = {}".format(final_obj))
    return final_obj


def create_nested_dict(keys, value):
    """
    Create a nested dictionary based on a list of keys and a common value for all leaves.
    """
    result = current = {}
    for key in keys[:-1]:
        if current.get(key) is None:
            current[key] = {}
        current = current[key]
    current[keys[-1]] = value

    return result


def main():
    dataset = load_dataset(dataset_filename)
    record = dataset[record_id]
    export_record = record["export_record"]
    fields_to_import = record["import_fields"]
    print("Loaded {} records".format(len(dataset)))
    option = st.selectbox(
        "Import Connector and the method",
        ("Zoom: Create Meeting",),
        index=None,
        placeholder="Select the Connector and the method",
    )
    available_resouces = st.text_area(
        "Available Resources",
        json.dumps(add_record(export_record), indent=True),
        height=300,
    )
    c1, c2 = st.columns((1, 1))
    # fields_from_export = list(export_record.keys())
    fields_from_export = get_flattened_keys("", export_record)
    print("All fields={}".format(fields_from_export))
    ht = c1.text_area("Fields from Export", "\n".join(fields_from_export), height=300)
    ar = c2.text_area("Fields to Import", "\n".join(fields_to_import), height=300)

    txt_message = st.text_area(
        "Celigo AI",
        "Generate the handlebars template for creating the HTTP Request Body",
    )
    debug = st.checkbox("Debug", value=True)
    submit = st.button("Submit")
    if submit:
        messages = createPromptWithGenerateAndSources(
            fields_from_export, fields_to_import
        )
        response = chat_completion_with_function_execution(
            messages, functions, function_call
        )
        if debug:
            st.text_area("Response from LLM:", response)
        mappings = response["mappings"]
        final_mapping_obj = {}
        lines = []
        for field in mappings:
            dest_field = field["destination"]
            src_field = field["source"]
            line = "{} <==> {}".format(src_field, dest_field)
            lines.append(line)
            final_mapping_obj[src_field] = "{{ {} }}".format(dest_field)

        # st.text_area("Response", response, height=300)
        st.text_area("Mapping", "\n".join(lines), height=300)
        st.text_area(
            "Handlebar", json.dumps(final_mapping_obj, indent=True), height=300
        )
        nested_dict = from_flattened({}, final_mapping_obj)
        st.text_area(
            "Nested dictionary", json.dumps(nested_dict, indent=True), height=300
        )


if __name__ == "__main__":
    main()
