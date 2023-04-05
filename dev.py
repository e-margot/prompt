import optuna
import pandas as pd
import numpy as np


df = pd.DataFrame()  # dataset


def create_prompt(dialog, trial):
    if trial.suggest_catigorical("use_intents", [False, True]):
        use_part_of_intents = trial.suggest_float("use_part_of_intents", 0, 1)  # 0.5
        pass  #

    prompt = None
    return prompt


def get_dialog_with_params(dialog, trial):
    # create prompt for ChatGPT
    prompt = create_prompt(dialog, trial)
    # push to ChatGPT get generated dialog
    generated_dialog = None
    return generated_dialog


def sim_func(gold_dialogs, new_dialogs):
    return np.mean([sim(d1, d2) for d1, d2 in zip(gold_dialogs, new_dialogs)])


def objective_v1(trial):
    # seria = df.sample(1)
    new_dialogs = []
    for dialog in df.iterrows():
        new_dialogs += get_dialog_with_params(dialog, trial)

    return sim_func(df.iterrows(), new_dialogs)


def objective_v2(trial):
    # seria = df.sample(1)
    new_dialogs = []
    prompts = []
    for dialog in df.iterrows():
        new_dialogs += get_dialog_with_params(dialog, trial)
        prompts += create_prompt(dialog, trial)

    return sim_func(df.iterrows(), new_dialogs), np.mean(map(len, prompts))


study = optuna.create_study(
    study_name=__file__,
    load_if_exists=True,
    directions=["maximize", "minimize"],
)
study.optimize(objective_v2, n_trials=100)

best_params = study.best_params
domain = best_params["domain"]
slot = best_params["slot"]
intent = best_params["intent"]
start_text = best_params["start_text"]
end_text = best_params["end_text"]
input_text = f"{start_text} {intent} {domain} {slot}. {end_text}"

# use_intents
# use_intents_description (from dataset\from chatgpt)
# use_slots
# use_slots_description (from dataset\from chatgpt)
# use_n_turns
# use_message (summary)
# use_generated_summary  (from chatgpt in 3 turns)
# instruction_version (len(instruction_versions) == 5):
# - examples of dialog with params + target params
# - short instraction
