from config import LLAMA_MODEL_3_2_3B, LLAMA_MODEL_3_3_70B

current_model = LLAMA_MODEL_3_2_3B  # default model

def get_current_model():
    return current_model

def set_current_model(model_name):
    global current_model
    if model_name.lower() == "llama3.2:3b":
        current_model = LLAMA_MODEL_3_2_3B
    elif model_name.lower() == "llama3.3:70b":
        current_model = LLAMA_MODEL_3_3_70B
    else:
        raise ValueError(f"Invalid model name.")
    return current_model 