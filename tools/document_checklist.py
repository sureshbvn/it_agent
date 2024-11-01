import json

def documentation_checklist(input_str):
    """
    Provide a checklist of required documentation for preboarding.

    Parameters:
    input_str (str): A JSON string with the key:
                     - "new_hire_name" (str): Name of the new hire.
                     Example: '{"new_hire_name": "Jordan"}'

    Returns:
    str: A formatted checklist of required documents and their submission status.

    Raises:
    Exception: If an error occurs during processing (e.g., missing data).
    """
    # Hardcoded document checklist data.
    # In a real-world scenario, this data would be fetched from a database or an external service.
    document_data = {
        "Sharath": {"ID Proof": "Submitted", "Work Authorization": "Pending", "Bank Details": "Pending"},
        "Rohit": {"ID Proof": "Submitted", "Work Authorization": "Submitted", "Bank Details": "Submitted"},
    }

    # Parse the input JSON string
    try:
        input_dict = json.loads(input_str.replace("'", "\""))
        new_hire_name = input_dict["new_hire_name"]
    except (json.JSONDecodeError, KeyError) as e:
        return f"Error: {str(e)}. Invalid input format. Please provide a valid JSON string."

    # Check for the new hire's document submission status
    info = document_data.get(new_hire_name)
    if info:
        message = f"Hello {new_hire_name}, here is your preboarding document checklist:\n"
        for doc, status in info.items():
            message += f"- {doc}: {status}\n"
        return message
    else:
        return f"No document checklist found for {new_hire_name}. Please check with HR for details."
