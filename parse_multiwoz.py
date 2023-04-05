import os
import json
import pandas as pd


def parse_multiwoz(dialog_path, output_path):
    """
    Parses a MultiWoZ dialog files and returns the domain, slot, intent, number of turns, and the dialog itself
    as a Pandas DataFrame.
    """

    # Check if the output directory exists
    if not os.path.exists(output_path):
        # Create the directory if it doesn't exist
        os.makedirs(output_path)

    # Create an empty list to store the dataframes
    dfs = []

    # Load the dialogue data from a file
    with open(dialog_path, 'r') as f:
        dialogue_data = json.load(f)

    for file_iter in range(len(dialogue_data)):
        # The id of dialogue
        dialogue_id = os.path.splitext(dialogue_data[file_iter]['dialogue_id'])[0]

        # The number of turns in the dialogue
        turns = len(dialogue_data[file_iter]['turns'])

        # The services in the dialogue
        services = dialogue_data[file_iter]['services']

        # The active intents and slot values in the dialogue
        active_intents = set()
        requested_slots = []
        slot_values = {}
        for turn in dialogue_data[file_iter]['turns']:
            for frame in turn["frames"]:
                if "state" in frame:
                    if frame['state']['active_intent'] != 'NONE':
                        active_intents.add(frame['state']['active_intent'])
                        slot_values.update(frame['state']['slot_values'])
                        if frame['state']['requested_slots']:
                            requested_slots.append(frame['state']['requested_slots'])
        # The user and system utterances in the dialogue
        dialog = []
        for utter_iter in range(turns):
            if dialogue_data[file_iter]['turns'][utter_iter]['speaker'] == 'USER':
                dialog.append(f"User: {dialogue_data[file_iter]['turns'][utter_iter]['utterance']}")
            else:
                dialog.append(f"Bot: {dialogue_data[file_iter]['turns'][utter_iter]['utterance']}")

        # Write the dialog to a file with a dialogue identifier
        output = os.path.join(output_path, f"{dialogue_id}_dialog.txt")
        with open(output, 'w+') as f:
            f.write('\n'.join(dialog))

        # Create DataFrame
        df = pd.DataFrame({
            'dialogue_id': dialogue_id,
            'services': [services],
            'active_intents': [active_intents],
            'requested_slots': [requested_slots],
            'slot_values': [slot_values],
            'turns': [turns],
        })

        dfs.append(df)

    return pd.concat(dfs)
