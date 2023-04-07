import optuna

from prompt_generator import load_data, load_text_from_json, select_random_row, extract_info, create_prompt

if __name__ == "__main__":
    # Load data
    path = "data/multiwoz_dialogs.csv"
    data = load_data(path)

    # Select a random row
    row = select_random_row(data)

    # Extract relevant information
    dialogue_id, services, active_intents, requested_slots, slot_values, turns, dialog, summary = extract_info(row)

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
    prompt = create_prompt(trial=trial,
                           header_text=header_texts,
                           footer_text=footer_text,
                           services_description=services_description,
                           slots_description=slots_description,
                           intents_description=intents_description,
                           services=services,
                           requested_slots=requested_slots,
                           slot_values=slot_values,
                           active_intents=active_intents,
                           num_turns=turns,
                           summary=summary)

    # Print the prompt
    print(prompt)
