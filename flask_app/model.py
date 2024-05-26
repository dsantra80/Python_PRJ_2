import torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from config import Config
import threading

# Load the Hugging Face token from the config
HF_TOKEN = Config.HF_TOKEN
model_name = Config.MODEL_NAME

# Set up quantization configuration for GPU usage
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_name, token=HF_TOKEN)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",  # Automatically place on GPU if available
    quantization_config=bnb_config,
    token=HF_TOKEN
)

# Set up the text generation pipeline
text_generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=Config.MAX_TOKENS,
    token=HF_TOKEN
)

# Create a lock for thread safety
model_lock = threading.Lock()

def generate_text(prompt, max_tokens=Config.MAX_TOKENS, temperature=Config.TEMPERATURE):
    with model_lock:  # Ensure only one thread can access the model at a time
        sequences = text_generator(prompt, max_new_tokens=max_tokens, temperature=temperature)
        gen_text = sequences[0]["generated_text"]
    return gen_text
