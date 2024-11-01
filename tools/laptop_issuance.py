import json
import re

def laptop_issuance(input_str):
    """
    Check laptop issuance status and provide a tracking code if available.

    Parameters:
    input_str (str): A JSON string representing a dictionary with the following key:
                     - "new_hire_name" (str): Name of the new hire to check laptop status.
                     Example: '{"new_hire_name": "Jordan"}'

    Returns:
    str: A formatted message about the issuance status and tracking code (if available).

    Raises:
    Exception: If there is an error in processing (e.g., missing data).
    ValueError: If the input format is invalid or the new hire's record is not found.
    """
    # Hardcoded laptop status data.
    # In a real-world scenario, this data would be fetched from a database or an external service.
    laptop_status_data = {
        "Sharath": {"status": "Shipped", "tracking_code": "FEDEX12345"},
        "Abhinav": {"status": "Shipped", "tracking_code": "FEDEX1222"},
        "Rohit": {"status": "In Progress", "tracking_code": None}
    }

    # Parse the input JSON string
    try:
        # Replace single quotes with double quotes
        input_str_clean = input_str.replace("'", "\"")
        # Remove any extraneous characters such as trailing quotes
        input_str_clean = input_str_clean.strip().strip("\"")
        input_dict = json.loads(input_str_clean)
        new_hire_name = input_dict["new_hire_name"]
    except (json.JSONDecodeError, KeyError) as e:
        return f"Error: {str(e)}. Invalid input format. Please provide a valid JSON string."

    # Check for the new hire's laptop issuance status
    info = laptop_status_data.get(new_hire_name)
    if info:
        if info["status"] == "Shipped" and info["tracking_code"]:
            return (f"Hello {new_hire_name}, your laptop has been shipped! "
                    f"Tracking code: {info['tracking_code']} (FedEx).")
        elif info["status"] == "In Progress":
            return f"Hi {new_hire_name}, your laptop issuance is currently in progress. We’ll notify you once it ships!"
        else:
            return f"Hello {new_hire_name}, we’re preparing your laptop for shipment."
    else:
        return f"No laptop issuance record found for {new_hire_name}. Please check with IT support."
