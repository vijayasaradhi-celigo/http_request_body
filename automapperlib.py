import json
import os

import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def main():
    messages = createPromptWithGenerateAndSources(copy_dest_fields, copy_source_fields)
    response = chat_completion_with_function_execution(
        messages, functions, function_call
    )
    print("Printing response=================")
    print(response)
    generated_mappings = response["mappings"]


def createPromptWithGenerateAndSources(destination_fields, source_fields):
    print("Source List={}".format(source_fields))
    print("Destination List={}".format(source_fields))
    messages = []
    system_message_content = """You are an expert in creating mappings between source
    fields and destination fields. You are well versed with the celigo
    integration platform. You are task is to arrive at the best possible
    mappings between the source and the destination fields. You will be
    provided with a list of source fields and a list of destination fields. For
    each source, you need to come up with the best possible destination based
    on the similarity of the source and destination fields. 
    """
    messages.append({"role": "system", "content": system_message_content})
    messages.append(
        {
            "role": "user",
            "content": """Each mapping is a one to one
                     relation between the source and destination fields.
                     The mapping should be based on the similarity between the
                     source field and the most similar destination field.
    """.strip(),
        }
    )
    messages.append(
        {
            "role": "user",
            "content": """
       Please follow these rules to determine the best mappings:-
       - Consider source name and source data type into consideration.
       - Use destination only once when mapping between source and destination.
       - Use source only once when mapping between source and destination.
       - Use only the source fields given to you.
       - Every destination field should be mapped to a source field.
       - Do not use the same source field twice.
       - Don't assume or suggest source fields which are not given to you.
       - Don't assume or suggest destination fields which are not given to you.
       - Use the exact source field name given to you.
       - Use the exact destination field name given to you.
       - Do not modify the source or the destination field names.
       """,
        }
    )
    messages.append(
        {
            "role": "user",
            "content": """
     List of destination fields: {}
     """.format(
                " ".join(destination_fields)
            ),
        }
    )
    messages.append(
        {
            "role": "user",
            "content": """
         Use only the following source when you try to map with destination.
         This object is a list of objects which contains two values source and the sourceDataType.
       """.strip(),
        }
    )
    messages.append(
        {
            "role": "user",
            "content": """
    List of source fields: {}
     """.format(
                " ".join(source_fields)
            ),
        }
    )
    return messages


# This is the function suggested by the deeplearning.ai chatgpt prompt engineering course
def get_completion(
    messages,
    model="gpt-3.5-turbo-16k",
    functions=[None],
    temperature=0,
    function_call="auto",
):
    # messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        functions=functions,
        function_call="auto",
        temperature=temperature,  # this is the degree of randomness of the model's output
    )
    return json.loads(response["choices"][0]["message"]["function_call"]["arguments"])


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
        print("After get_completion")
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
        "source": {
            "type": "string",
            "description": "the value to be selected from the sourcelist which is given to you",
        },
    },
    "required": ["destination", "source"],
}

multipleMappingsSchema = {
    "type": "object",
    "properties": {
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
