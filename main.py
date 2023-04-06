import optuna

from prompt_generator import load_data, load_text_from_json, select_random_row, extract_info, create_prompt

if __name__ == "__main__":
    # Load data
    path = "data/multiwoz_dialogs.csv"
    data = load_data(path)

    # Select a random row
    row = select_random_row(data)

    # Extract relevant information
    dialog_id, slots, intents, requested_slots, num_turns, domains = extract_info(row)

    # Load text for the header and footer
    header_texts = load_text_from_json("data/header_footer/header.json")
    footer_text = load_text_from_json("data/header_footer/footer.json")
    # Load descriptions for services, slots, and intents
    services_description = load_text_from_json("data/descriptions/services_description.json")
    slots_description = load_text_from_json("data/descriptions/slots_description.json")
    intents_description = load_text_from_json("data/descriptions/intents_description.json")

    # Initialize Optuna trial
    trial = optuna.create_trial()

    # Create the prompt
    prompt = create_prompt(trial, header_texts, footer_text, services_description, slots_description,
                           intents_description, domains, requested_slots, slots, intents, num_turns)

    # Print the prompt
    print(prompt)
