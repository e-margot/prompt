import os
import json


def parse_schema(input_path, output_path):

    with open(input_path, 'r') as f:
        schema_file = json.load(f)

    # Check if the output directory exists
    if not os.path.exists(output_path):
        # Create the directory if it doesn't exist
        os.makedirs(output_path)

    # Get service description
    services = {}
    for i in range(len(schema_file)):
        service_name = schema_file[i]['service_name']
        service_descripton = schema_file[i]['description']
        services.update({service_name: service_descripton})

    # Save file
    services_output = os.path.join(output_path, f"services_description.json")
    with open(services_output, 'w') as f1:
        json.dump(services, f1)

    # Get slots description
    slots = {}
    for i in range(len(schema_file)):
        for j in range(len(schema_file[i]['slots'])):
            slot_name = schema_file[i]['slots'][j]['name']
            slot_description = schema_file[i]['slots'][j]['description']
            slots.update({slot_name: slot_description})

    slots_output = os.path.join(output_path, f"slots_description.json")
    with open(slots_output, 'w') as f2:
        json.dump(slots, f2)

    # Get intent description
    intents = {}
    for i in range(len(schema_file)):
        for j in range(len(schema_file[i]['intents'])):
            intent_name = schema_file[i]['intents'][j]['name']
            intent_description = schema_file[i]['intents'][j]['description']
            intents.update({intent_name: intent_description})

    intents_output = os.path.join(output_path, f"intents_description.json")
    with open(intents_output, 'w') as f3:
        json.dump(intents, f3)


if __name__ == "__main__":
    parse_schema("MultiWOZ_2.2/schema.json", "data/descriptions")
