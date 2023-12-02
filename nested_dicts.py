def merge_dicts(dict1, dict2):
    for key, value in dict2.items():
        if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
            merge_dicts(dict1[key], value)
        else:
            dict1[key] = value
    return dict1


def create_nested_dicts(lines):
    result = []

    for line in lines:
        field_names_list = line.split(".")
        current_dict = {}

        temp_dict = current_dict
        for field in field_names_list:
            temp_dict = temp_dict.setdefault(field, {})

        # Merge the current_dict with the existing result
        merge_dicts(result, current_dict)

    return result


# Example usage:
lines = [
    "first_name.last_name",
    "address.city.state.country",
    "company.name.department",
]

nested_dicts = create_nested_dicts(lines)

for idx, nested_dict in enumerate(nested_dicts, start=1):
    print(f"Nested Dictionary {idx}:")
    print(nested_dict)
    print()
