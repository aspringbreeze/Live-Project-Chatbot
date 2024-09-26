import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load pre-trained GPT-2 model and tokenizer
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Make sure the model runs in evaluation mode
model.eval()

# If you have a GPU, you can use it for faster inference
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Function to generate responses from the chatbot
def generate_response(prompt, max_length=100, num_return_sequences=1):
    # Token input prompt
    input_ids = tokenizer.encode(prompt, return_tensors="pt").to(device)

    # Generate the output using the GPT-2
    output = model.generate(
        input_ids,
        max_length = max_length,
        num_return_sequences = num_return_sequences,
        no_repeat_ngram_size=2, # Prevent repetitive phrases
        do_sample=True,         # Enable sampling to generate diverse responses
        top_p=0.95,             # Nucleus sampling
        top_k=50,               # Top-k sampling
        temperature=0.7         # Adjust temperature for randomness
    )

    # Decode the generated response and return it
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response

# Chatbot conversion loop
def chat():
    print("Bot: Welcome! How can I assist you today? Here\'s what I can help with:\n1. Open time\n2. Place an order\n3. Account information")

    while True:
        user_input = input("You: ")

        # Check if user wants to exit the chat
        if user_input.lower() in ["bye", "exit", "quit"]:
            print("Bot: Bye!")
            break

        # Generate response using GPT-2 model
        bot_response = generate_response(user_input)
        print(f"Bot: {bot_response}")

# Satrt the chatbot
if __name__ == "__main__":
    chat()
    