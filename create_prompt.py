import random
import pandas as pd


# Load the data from a CSV file into a DataFrame
path = "data/multiwoz_dialogs.csv"
data = pd.read_csv(path)

# Select a random row from the DataFrame
row_idx = random.randint(0, len(data) - 1)
row = data.iloc[row_idx]

# Extract the relevant information from the row
dialog_id = row["dialogue_id"]
slots = row["slot_values"]
intents = row["active_intents"]
num_turns = row["turns"]
domains = row["service"]

# Constant text
start_texts = [f"Generate a dialogue in the MultiWOZ dataset for the following scenario: \n",
               f"Generate a dialogue for the following scenario: \n"
               ]
end_texts = [f"""Start the dialogue with a greeting from the user and ends with a goodbye from the bot. 
Make sure the dialogue is coherent and follows the conventions of natural conversation. 
Make sure the system gets the address, phone number or reference number if it possible""",
             ]

# Load the text of the dialog from the corresponding file
with open(f"{dialog_id}_dialog.txt", "r") as f:
    dialog_text = f.read()


def create_prompt(trial):

    # The code trial.suggest_categorical("param", param, [True] * len(param)) suggests a categorical value for a
    # hyperparameter named "param". The possible values for "param" are chosen from the list param and each value is
    # associated with a boolean value True.

    # Essentially, this code suggests a set of boolean values for a hyperparameter. The length of the set of suggested
    # values is the same as the length of param. The suggested boolean value of True for each element in the set implies
    # that the corresponding value in param should be included in the model evaluation.
    with_intent = trial.suggest_catigorical("with_intent", [False, True])
    with_slot = trial.suggest_catigorical("with_slot", [False, True])
    with_example = trial.suggest_catigorical("with_example", [False, True])
    chosen_slots = trial.suggest_categorical("slots", slots, [True] * len(slots))
    chosen_intents = trial.suggest_categorical("intents", intents, [True] * len(intents))
    start_text = trial.suggest_categorical("start_text", start_texts)
    end_text = trial.suggest_categorical("end_text", end_texts)
    n_turns = trial.suggest_catigorical("num_turns", [False, True])
    # domain = trial.suggest_categorical("domain", domains)

    # Use the sampled parameters to construct the prompt
    prompt = f"{start_text}. This is the {domains} bot. "
    if with_slot:
        prompt += f"Included slots: "
        for slot in slots:
            if chosen_slots[slots.index(slot)]:
                prompt += f"{slot}\n"
    if with_intent:
        prompt += f"Included intent: "
        for intent in intents:
            if chosen_intents[intents.index(intent)]:
                prompt += f"{intent}\n"

    prompt += f"With turns: {num_turns}"

    if with_example:
        prompt += f"Example: {dialog_text[0]}"
    prompt += end_text

    return prompt

