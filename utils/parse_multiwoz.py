import os
import re
import json
import pandas as pd


def create_dialogue_file(dialogue_id, dialog, output_path):
    """Create a text file containing the dialog for a given dialogue ID"""

    # create the path to the output file
    output_file = os.path.join(output_path, f"{dialogue_id}_dialog.txt")
    # write the dialog to the file
    with open(output_file, 'w+') as f:
        f.write('\n'.join(dialog))


def extract_dialogue_info(dialogue, m_woz_2_1):
    """Extract various pieces of information from a MultiWoZ dialogue"""

    # extract the set of active intents in the dialogue
    active_intents = {frame['state']['active_intent'] for turn in dialogue['turns']
                      for frame in turn['frames'] if 'state' in frame}

    # extract the list of requested slots in the dialogue
    requested_slots = [state['requested_slots'] for turn in dialogue['turns']
                       for frame in turn['frames'] if 'state' in frame
                       for state in [frame['state']] if state['requested_slots']]

    # extract the dictionary of slot values in the dialogue
    slot_values = {slot: state['slot_values'][slot] for turn in dialogue['turns']
                   for frame in turn['frames'] if 'state' in frame
                   for state in [frame['state']]
                   for slot in state['slot_values']}

    # extract the summary of the dialogue goals
    summary = [re.sub(r'<(.*?)>', '', m)
               for message in m_woz_2_1.get(dialogue['dialogue_id'], {}).get('goal', {}).get('message', [])
               if isinstance(message, str) for m in [message]]

    # create a list of dialogue turns
    dialog = [f"{'User' if turn['speaker'] == 'USER' else 'Bot'}: {turn['utterance']}" for turn in dialogue['turns']]

    # return a dictionary containing various information about the dialogue
    return {
        'dialogue_id': os.path.splitext(dialogue['dialogue_id'])[0],
        'services': ' '.join(dialogue['services']),
        'active_intents': active_intents,
        'requested_slots': requested_slots,
        'slot_values': slot_values,
        'turns': len(dialogue['turns']),
        'dialog': dialog,
        'summary': summary,
    }


def parse_multiwoz(dialog_path, output_path, m_woz_old_path):
    """Parse a MultiWoZ dialog file and return a Pandas DataFrame"""

    # load the MultiWoZ_2.2 dialog file
    with open(dialog_path, 'r') as f:
        dialogues = json.load(f)

    # load the MultiWoZ 2.1 file
    with open(m_woz_old_path, 'r') as f:
        m_woz_2_1 = json.load(f)

    # Check if the output directory exists
    if not os.path.exists(output_path):
        # Create the directory if it doesn't exist
        os.makedirs(output_path)

    # extract the information from each dialogue and write it to a text file
    data = [extract_dialogue_info(dialogue, m_woz_2_1) for dialogue in dialogues]
    for dialogue_info in data:
        create_dialogue_file(dialogue_info['dialogue_id'], dialogue_info['dialog'], output_path)
    return pd.DataFrame(data)


if __name__ == "__main__":
    dir_path = "MultiWOZ_2.2/train"
    output_path = "data/dialogues"
    m_woz_old_path = "MultiWOZ_2.1/data.json"

    dfs = [parse_multiwoz(os.path.join(dir_path, filename), output_path, m_woz_old_path)
           for filename in os.listdir(dir_path) if filename.endswith(".json")]
    df = pd.concat(dfs, ignore_index=True)
    df.to_csv('data/multiwoz_dialogs.csv', index=False)
