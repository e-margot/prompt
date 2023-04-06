import json
import optuna
import pandas as pd


# Load data from CSV file into a DataFrame
def load_data(path: str) -> pd.DataFrame:
    """Load data from CSV file into a Pandas DataFrame.
    Args:
        path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Pandas DataFrame containing the data from the CSV file.
    """
    return pd.read_csv(path)


# Select a random row from the DataFrame
def select_random_row(data: pd.DataFrame) -> pd.Series:
    """Select a random row from the DataFrame.

    Args:
        data (pd.DataFrame): The DataFrame from which to select a random row.

    Returns:
        pd.Series: The selected row from the DataFrame.
    """
    return data.sample().iloc[0]


# Extract relevant information from the row
def extract_info(row: pd.Series) -> tuple:
    """Extract relevant information from the row.

    Args:
        row (pd.Series): The row from which to extract information.

    Returns:
        tuple: A tuple containing the dialog ID, slots, intents, requested slots,
        number of turns, and domains extracted from the row.
    """
    dialog_id = row["dialogue_id"]
    slots = eval(row["slot_values"])  # covert dict-looklike string to dict
    intents = row["active_intents"]
    requested_slots = row["requested_slots"]
    num_turns = row["turns"]
    domains = row["services"]
    return dialog_id, slots, intents, requested_slots, num_turns, domains


# Load text from JSON files
def load_text_from_json(path: str) -> dict:
    """Load text from a JSON file.

    Args:
        path (str): Path to the JSON file.

    Returns:
        dict: A dictionary containing the text loaded from the JSON file.
    """
    with open(path, "r") as f:
        return json.load(f)


# Create the prompt
def create_prompt(trial: optuna.trial.Trial, header_text: dict, footer_text: dict, services_description: dict,
                  slots_description: dict, intents_description: dict, domains: list, requested_slots: list,
                  slots: dict, intents: list, num_turns: int) -> str:
    """Create a prompt for the conversational AI model.

    Args:
        trial (optuna.trial.Trial): An Optuna trial object used for optimizing the prompt.
        header_text (str): Text to include at the beginning of the prompt.
        footer_text (str): Text to include at the end of the prompt.
        services_description (dict): A dictionary mapping domain names to descriptions.
        slots_description (dict): A dictionary mapping slot names to descriptions.
        intents_description (dict): A dictionary mapping intent names to descriptions.
        domains (list): A list of domains supported by the conversational AI model.
        requested_slots (list): A list of requested slots for the conversation.
        slots (dict): A dictionary mapping slot names to values.
        intents (list): A list of intents for the conversation.
        num_turns (int): The number of turns in the conversation.

    Returns:
        str: The complete prompt for the conversational AI model.
    """

    header_text = trial.suggest_categorical("header_text", header_text)
    footer_text = trial.suggest_categorical("end_text", footer_text)

    prompt = f"{header_text}."

    # Add domain information
    if domains == '' or domains is None:
        prompt += "This bot does not work with any specific domains. \n"
    else:
        prompt += f"This bot works with the following domains: {', '.join(domains)}. \n"
        for domain, domain_desc in services_description.items():
            if domain in domains:
                prompt += f"{domain}: {domain_desc} \n"

    # Add slot information
    if trial.suggest_categorical("with_slot", [False, True]):
        prompt += "The following slots are available: \n"
        for slot, slot_desc in slots_description.items():
            if slot in slots:
                prompt += f"{' '.join(slot.split('-'))}: {slot_desc} {slots.get(slot)[0]} \n"

    # Add requested slot information
    if trial.suggest_categorical("with_requested_slot", [False, True]):
        if len(requested_slots) != 0:
            prompt += "The user is interested in the following slots: \n"
            requested_slots_list = [element for sublist in requested_slots for element in sublist]
            for requested_slot in requested_slots_list:
                if requested_slot in slots_description:
                    prompt += f"{' '.join(requested_slot.split('-'))}: {slots_description.get(requested_slot)} \n"
        else:
            prompt += "The user is not interested in any specific slots. \n"

    # Add intent information
    if trial.suggest_categorical("with_intent", [False, True]):
        prompt += "The bot needs to perform the following intents: \n"
        for intent, intent_desc in intents_description.items():
            if intent in intents:
                prompt += f"{' '.join(intent.split('_'))}: {intent_desc} \n"

    # Add number of turns
    prompt += f"The conversation should have {num_turns} turns. \n"

    # Add footer text
    prompt += footer_text

    return prompt
