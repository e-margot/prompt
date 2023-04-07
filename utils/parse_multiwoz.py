import os
import json
import pandas as pd


def create_dialogue_file(dialogue_id, dialog, output_path):
    """Create a text file containing the dialog for a given dialogue ID"""
    output_file = os.path.join(output_path, f"{dialogue_id}_dialog.txt")
    with open(output_file, 'w+') as f:
        f.write('\n'.join(dialog))


def extract_dialogue_info(dialogue, m_woz_2_1):
    """Extract various pieces of information from a MultiWoZ dialogue"""
    turns = len(dialogue['turns'])
    services = " ".join(dialogue['services'])
    active_intents = set()
    requested_slots = []
    summary = []
    slot_values = {}
    for turn in dialogue['turns']:
        for frame in turn['frames']:
            if 'state' in frame:
                if frame['state']['active_intent'] != 'NONE':
                    active_intents.add(frame['state']['active_intent'])
                    slot_values.update(frame['state']['slot_values'])
                    if frame['state']['requested_slots']:
                        requested_slots.append(frame['state']['requested_slots'])

    for dialogue_id in m_woz_2_1:
        if dialogue['dialogue_id'] == dialogue_id:
            message = m_woz_2_1[dialogue_id]['goal']['message']
            if not type(message) == list:
                message = [message]
            for i in range(len(message)):
                message[i] = re.sub(r'\<(.*?)\>', '', message[i])
            summary.add(message)

    dialog = []
    for turn in dialogue['turns']:
        speaker = 'User' if turn['speaker'] == 'USER' else 'Bot'
        dialog.append(f"{speaker}: {turn['utterance']}")
    return {
        'dialogue_id': os.path.splitext(dialogue['dialogue_id'])[0],
        'services': services,
        'active_intents': active_intents,
        'requested_slots': requested_slots,
        'slot_values': slot_values,
        'turns': turns,
        'dialog': dialog,
        'summary': summary,
    }


def parse_multiwoz(dialog_path, output_path, m_woz_old_path):
    """Parse a MultiWoZ dialog file and return a Pandas DataFrame"""
    with open(dialog_path, 'r') as f:
        dialogues = json.load(f)

    with open(m_woz_old_path, 'r') as f:
        m_woz_2_1 = json.load(f)

    # Check if the output directory exists
    if not os.path.exists(output_path):
        # Create the directory if it doesn't exist
        os.makedirs(output_path)

    data = [extract_dialogue_info(dialogue, m_woz_2_1) for dialogue in dialogues]
    for dialogue_info in data:
        create_dialogue_file(dialogue_info['dialogue_id'], dialogue_info['dialog'], output_path)
    return pd.DataFrame(data)


if __name__ == "__main__":
    dir_path = "MultiWOZ_2.2/train"
    output_path = "data/dialogues"
    mWOZ_old_path = "MultiWOZ_2.1/data.json"

    dfs = []
    for filename in os.listdir(dir_path):
        if filename.endswith(".json"):
            input_path = os.path.join(dir_path, filename)
            dfs.append(parse_multiwoz(input_path, output_path, mWOZ_old_path))

    df = pd.concat(dfs, ignore_index=True)
    df.to_csv('data/multiwoz_dialogs.csv', index=False)
