def create_nested_dict(keys, value):
    """
    Create a nested dictionary based on a list of keys and a common value for all leaves.
    """
    result = current = {}
    
    for key in keys[:-1]:
        current[key] = {}
        current = current[key]
    
    current[keys[-1]] = value
    
    return result

# Example usage:
nested_keys = ['first', 'second', 'third']
nested_value = 42

nested_dict = create_nested_dict(nested_keys, nested_value)

print(nested_dict)
