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


def from_flattened(flat_key_values_dict):
    obj = {}
    final_obj = {}
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
    connector_uids = [obj["uid"] for obj in dataset]
    option = st.selectbox(
        "Select Connector and the method",
        connector_uids,
        placeholder="Select the Connector and the method",
    )
    record_id = connector_uids.index(option)
    # st.write("Record id={}".format(record_id))
    record = dataset[record_id]
    connector_uri = record["connector_uri"]
    export_record = record["export_record"]
    fields_to_import = record["import_fields"]
    st.text(connector_uri)
    available_resouces = st.text_area(
        "Available Resources",
        json.dumps(add_record(export_record), indent=4),
        height=300,
    )
    print("Loaded {} records".format(len(dataset)))
    c1, c2 = st.columns((1, 1))
    # fields_from_export = list(export_record.keys())
    fields_from_export = get_flattened_keys("", export_record)
    print("All fields={}".format(fields_from_export))
    ta_fields_from_export = c1.text_area(
        "Fields from Export", "\n".join(fields_from_export), height=300
    )
    ta_fields_to_import = c2.text_area(
        "Fields to Import", "\n".join(fields_to_import), height=300
    )

    #    txt_message = st.text_area(
    #        "Celigo AI",
    #        "Generate the handlebars template for creating the HTTP Request Body",
    #    )
    debug = st.checkbox("Debug", value=False)
    submit = st.button("Submit")
    if submit:
        fields_from_export = ta_fields_from_export.split("\n")
        fields_to_import = ta_fields_to_import.split("\n")
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
            final_mapping_obj[src_field] = "{{{{ record.{} }}}}".format(dest_field)

        if debug:
            st.text_area("Response", response, height=300)
        if debug:
            st.text_area("Mapping", "\n".join(lines), height=300)
        if debug:
            st.text_area(
                "Flat Handlebar", json.dumps(final_mapping_obj, indent=4), height=300
            )
        nested_dict = from_flattened(final_mapping_obj)
        st.text_area("Handlebar", json.dumps(nested_dict, indent=4), height=300)


if __name__ == "__main__":
    main()
