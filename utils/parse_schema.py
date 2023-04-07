import os
import json


def parse_schema(input_path: str, output_path: str) -> None:
    """
    Parses the schema JSON file and extracts descriptions for services, slots, and intents,
    and saves them to separate JSON files in the specified output directory.

    Args:
        input_path (str): The path to the input schema JSON file.
        output_path (str): The path to the output directory where the extracted descriptions will be saved.

    Returns:
        None
    """
    with open(input_path, 'r') as f:
        schema_file = json.load(f)

    # Check if the output directory exists and create it if it doesn't
    os.makedirs(output_path, exist_ok=True)

    # Extract service descriptions
    services = {service['service_name']: service['description'] for service in schema_file}

    # Extract slot descriptions
    slots = {slot['name']: slot['description'] for service in schema_file for slot in service['slots']}

    # Extract intent descriptions
    intents = {intent['name']: intent['description'] for service in schema_file for intent in service['intents']}

    # Save descriptions to file
    with open(os.path.join(output_path, "services_description.json"), 'w') as f:
        json.dump(services, f)
    with open(os.path.join(output_path, "slots_description.json"), 'w') as f:
        json.dump(slots, f)
    with open(os.path.join(output_path, "intents_description.json"), 'w') as f:
        json.dump(intents, f)


if __name__ == "__main__":
    parse_schema("../MultiWOZ_2.2/schema.json", "data/descriptions")
