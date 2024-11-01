import json


def laptop_preference(input_str):
    """
    Suggest a laptop based on the new hire's role, or return their previous choice if they already exist.

    Parameters:
    input_str (str): A JSON string representing a dictionary with the following keys:
                     - "new_hire_name" (str): Name of the new hire.
                     - "role" (str): Role of the new hire (e.g., "Engineer", "Marketing", "Sales").

                     Example: '{"new_hire_name": "Jordan", "role": "Engineer"}'

    Returns:
    str: A formatted message suggesting the best laptop based on the role or showing the previous choice if available.

    Raises:
    Exception: If an error occurs during processing (e.g., missing data).
    ValueError: If the input format is invalid.
    """
    # Hardcoded previous laptop choices
    previous_choices = {
        "Jordan": "MacBook Pro",
        "Alex": "Dell XPS"
    }

    # Parse the input JSON string
    try:
        # Replace single quotes with double quotes
        input_str_clean = input_str.replace("'", "\"")
        # Remove any extraneous characters such as trailing quotes
        input_str_clean = input_str_clean.strip().strip("\"")
        input_dict = json.loads(input_str_clean)
        new_hire_name = input_dict["new_hire_name"]
        role = input_dict["role"]
    except (json.JSONDecodeError, KeyError) as e:
        return f"Error: {str(e)}. Invalid input format. Please provide a valid JSON string."

    # Check if the user already has a laptop preference
    if new_hire_name in previous_choices:
        return f"{new_hire_name} already has a laptop preference: {previous_choices[new_hire_name]}."

    # Suggest a laptop based on the role
    if role.lower() in ["engineer", "developer", "engineering"]:
        suggested_laptop = "MacBook Pro"
    else:
        suggested_laptop = "Dell XPS (Windows)"

    return f"Based on your role as a {role}, we suggest a {suggested_laptop} for {new_hire_name}."
