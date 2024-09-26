import spacy
import random

# Load spaCy language model
nlp = spacy.load('en_core_web_sm')

# Define intent and follow-up response mapping
intent_flow = {
    "greetings": {
        "responses": ["Hello! How can I assist you today?", "Hi there! What can I do for you?"],
        "follow_up": None
    },
    "order": {
        "responses": ["What would you like to order? We have pizza, salad, and drinks."],
        "follow_up": None
    },
    "pizza_order": {
        "responses": ["Which size of pizza would you like to order? Small, Medium, or Large?"],
        "follow_up": None
    },
    "salad_order": {
        "responses": ["A salad has been ordered."],
        "follow_up": None
    },
    "drink_order": {
        "responses": ["A drink has been ordered."],
        "follow_up": None
    },
    "account": {
        "responses": ["Here is your account info. Would you like to see your previous orders? (yes/no)"],
        "follow_up": "previous_orders"
    },
    "previous_orders": {
        "responses": ["Here are your previous orders: [Order details displayed]."],
        "follow_up": None
    },
    "open_hours": {
        "responses": ["We are open from 10 AM to 9 PM, Monday to Sunday."],
        "follow_up": None
    },
    "thanks": {
        "responses": ["You're welcome!", "No problem!"],
        "follow_up": None
    },
    "goodbye": {
        "responses": ["Goodbye! Have a great day!"],
        "follow_up": None
    },
    "fallback": {
        "responses": ["I'm sorry, I didn’t quite understand that. Could you rephrase?"],
        "follow_up": None
    },
    "cancel_order": {
        "responses": ["Your order has been canceled."],
        "follow_up": None
    }
}

# Intents and keywords to detect using spaCy (dynamically map words)
intents = {
    "greetings": ["hello", "hi", "hey", "greetings"],
    "thanks": ["thank", "thanks"],
    "cancel_order": ["cancel"],
    "order": ["order", "buy", "purchase"],
    "pizza_order": ["pizza", "piza", "pizzza"],
    "salad_order": ["salad"],
    "drink_order": ["drink"],
    "account": ["account", "profile", "information"],
    "previous_orders": ["previous", "history"],
    "open_hours": ["hours", "time", "open"],
    "goodbye": ["bye", "goodbye", "exit"]
}

# Function to preprocess user input and match with an intent using spaCy
def get_intent_spacy(user_input):
    doc = nlp(user_input)
    # Extract keywords from user input
    tokens = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct]
    
    # Match tokens to intent
    for intent, keywords in intents.items():
        if any(token in keywords for token in tokens):
            return intent
    return "fallback"

# Function to extract entities like pizza size or type using spaCy
def extract_order_details(doc):
    order_details = {"size": None, "item": None}
    for token in doc:
        if token.text.lower() in ["small", "medium", "large"]:
            order_details["size"] = token.text.lower()
        if token.text.lower() == "pizza":
            order_details["item"] = token.text.lower()
    return order_details

# Function to dynamically respond based on intent and follow-up state
def respond_to_intent(intent, user_input=None):
    doc = nlp(user_input) if user_input else None
    if intent == "pizza_order" and doc:
        order_details = extract_order_details(doc)
        if order_details["size"]:
            return f"A {order_details['size']} pizza has been ordered.", None
        return random.choice(intent_flow["pizza_order"]["responses"]), "pizza_order"
    
    # Fallback for any unmapped or complex intents
    return random.choice(intent_flow[intent]["responses"]), intent_flow[intent]["follow_up"]

# Main chatbot logic with dynamic follow-up handling
def chatbot_spacy():
    print("Bot: Welcome! How can I assist you today? Here\'s what I can help with:\n1. Open time\n2. Place an order\n3. Account information")
    follow_up_state = None

    while True:
        user_input = input("You: ").lower()

        # If user says goodbye, exit the chatbot
        if "goodbye" in user_input or any(word in user_input for word in intents["goodbye"]):
            print(f"Bot: {random.choice(intent_flow['goodbye']['responses'])}")
            break

        # Determine the intent based on user input and previous follow-up state
        if follow_up_state:
            # Use follow-up state if we're in a follow-up context
            current_intent = follow_up_state
        else:
            current_intent = get_intent_spacy(user_input)

        # Generate response based on current intent and check if there's a follow-up needed
        response, follow_up_state = respond_to_intent(current_intent, user_input)
        print(f"Bot: {response}")

# Run the chatbot with dynamic follow-up handling
chatbot_spacy()
