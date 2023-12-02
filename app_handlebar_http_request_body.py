import streamlit as st
import pandas as pd
import openai
import json
import requests
import random
from dotenv import load_dotenv


load_dotenv()
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(layout="wide")

available_resources = {
    "record": {
        "id": "1",
        "movie": "2001",
        "director": "Stanley Kubrick",
        "release_date": "1968",
        "num_oscars": "1",
        "imdb": "http://www.imdb.com/title/tt0062622/",
        "country": "USA",
    },
    "connection": {
        "name": "Google Sheets Vijay",
        "http": {"unencrypted": {}, "encrypted": "********"},
    },
    "import": {"name": "Update existing rows and append new rows"},
    "settings": {
        "integration": {},
        "flow": {},
        "flowGrouping": {},
        "connection": {},
        "import": {},
    },
}
record = available_resources["record"]


def main():
    c1, c2 = st.columns((1, 1))
    ht = c1.text_area("Handlebars Template", "", height=300)
    ar = c2.text_area(
        "Available Resouces", json.dumps(available_resources, indent=2), height=300
    )

    txt_message = st.text_area(
        "Celigo AI",
        "Generate the handlebars template for creating the HTTP Request Body",
    )
    debug = st.checkbox("Debug", value=True)
    submit = st.button("Submit")
    if submit:
        messages = create_messages(txt_message, ar)
        response = get_completion(messages)

        print("Printing response=================")
        print(response)
        content = json.dumps(response, indent=True)
        st.text_area("Response", response, height=300)


def create_messages(user_prompt, json_data):
    obj = json.loads(json_data)
    record_str = json.dumps(obj["record"])
    messages = []
    system_message_content = """You are an expert in creating mappings between source
    fields and destination fields. You are well versed with the celigo
    handlebars
    """
    messages.append({"role": "system", "content": system_message_content})
    messages.append({"role": "user", "content": user_prompt + "\n" + record_str})
    return messages


# This is the function suggested by the deeplearning.ai chatgpt prompt engineering course
def get_completion(messages, model="gpt-3.5-turbo-16k", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,  # this is the degree of randomness of the model's output
    )
    return response["choices"][0].message["content"]


def chat_completion_with_function_execution(
    messages, functions=[None], function_call="auto"
):
    """This function makes a ChatCompletion API call with the option of adding functions"""
    for i in range(3):
        response = get_completion(
            messages,
            model="gpt-3.5-turbo-16k",
            functions=functions,
            function_call="auto",
        )
        print("AFter get_completion")
        try:
            print(response)
            print(type(response))
            return response
        except Exception as e:
            print(f"Exception occurred: {e}")
            raise
        else:
            break


mappingSchema = {
    "type": "object",
    "description": "contains the values to create mappping",
    "properties": {
        "destination": {
            "type": "string",
            "description": "the value given by the user to map with the source",
        },
        #    "destinationDataType": {
        #      "type": "string",
        #      # "enum": ["string", "number", "bool", "stringArr", "numberArr", "boolArr"],
        #      "default": "string",
        #      "description": "the value which came from user and represents the data type of the destination",
        #    },
        "source": {
            "type": "string",
            "description": "the value to be selected from the sourcelist which is given to you",
        },
        #    "sourceDataType": {
        #      "type": "string",
        #      # "enum": ["string", "number", "bool", "stringArr", "numberArr", "boolArr"],
        #      "default": "string",
        #      "description": "the value which is selected from the sourcelist and represents the data type of the source",
        #    }
    },
    "required": [
        "destination",
        #    "destinationDataType",
        "source"
        #    "sourceDataType"
    ],
}

multipleMappingsSchema = {
    "type": "object",
    "properties": {
        # "count": {
        #   "type": "number",
        #   "description": "the number of mappings created under mappings array",
        # },
        "mappings": {
            "type": "array",
            "description": "the list of mappings to be created",
            "items": mappingSchema,
        }
    },
    "required": ["mappings"],
}

functions = [
    {
        "name": "create_mappings",
        "description": "Use this function and pass the required values to get the list of mappings between destination and source",
        "parameters": multipleMappingsSchema,
    }
]

function_call = {"name": "create_mappings"}
if __name__ == "__main__":
    main()
