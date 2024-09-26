import tkinter as tk
from tkinter import scrolledtext
import re
from nltk.corpus import wordnet

# Building a list of Keywords
list_words = ['hello', 'timings', 'order', 'account']
list_syn = {}
for word in list_words:
    synonyms = []
    for syn in wordnet.synsets(word):
        for lem in syn.lemmas():
            # Remove any special characters from synonym strings
            lem_name = re.sub('[^a-zA-Z0-9 \n\.]', ' ', lem.name())
            synonyms.append(lem_name)
    list_syn[word] = set(synonyms)
# print(list_syn)  # Optional: to see the list of synonyms generated

# Building a dictionary of intents & keywords
keywords = {}
keywords_dict = {}

# Populate the dictionary with intents like 'greet', 'timings', etc.
for intent in list_words:
    keywords[intent] = []
    for synonym in list(list_syn[intent]):
        keywords[intent].append('.*\\b'+synonym+'\\b.*')

for intent, keys in keywords.items():
    keywords_dict[intent] = re.compile('|'.join(keys))

# Building a dictionary of responses
responses = {
    'hello': 'Welcome! How can I help you?',
    'timings': 'We are open from 11AM to 9PM, Monday to Sunday.',
    'order': 'What would you like to order? We have pizza, salad and drink.',
    'account': 'Here is the information related to your account. Would you like to see your previous orders (yes/no)?',
    'fallback': 'I\'m sorry, I didn\'t quite get that. Could you rephrase or try asking about store timings, placing an order, or account information?'
}

# Define the exit words
exit_words = ["goodbye", "exit", "end chat", "close conversation", "bye"]

# Variable to track the follow-up state
follow_up_state = None

# Starting the chatbot dialogue flow
def chatbot_response(user_input):
    global follow_up_state
    user_input = user_input.lower()
    
    # Check for exit words to terminate the conversation
    if any(word in user_input for word in exit_words):
        return("Goodbye! Have a great day!")
    
    # Handle follow-up for pizza size
    if follow_up_state == 'pizza_order':
        if user_input in ['small', 'medium', 'large']:
            follow_up_state = None # Reset follow-up state
            return(f"A {user_input} pizza has been ordered.")
        else:
            return("Please choose a valid size: Small, Medium, or Large.")
    
    # Handle follow-up for "order" intent
    if follow_up_state == 'order_check':
        if 'pizza' in user_input:
            follow_up_state = 'pizza_order' 
            return("Which size would you like to order? Small, Medium or Large?")
        if "salad" in user_input:
            follow_up_state = None # Reset follow-up state
            return("A salad has been ordered.")
        if "drink" in user_input:
            follow_up_state = None # Reset follow-up state
            return("A drink has been ordered.")

    # Handle follow-up for "account" intent
    if follow_up_state == 'account_check':
        if user_input in ['yes', 'no']:
            follow_up_state = None # Reset follow-up state
            if user_input == 'yes':
                return(f"Here are your previous orders: [Order details displayed].")
            else:
                return("If you need to update your account information, let me know.")
        else:
            return("Please type in \'yes or no\'.")

    # If no follow-up, process the normal intents
    matched_intent = None
    for intent, pattern in keywords_dict.items():
        if re.search(pattern, user_input):
            matched_intent = intent
            break
    
    if matched_intent:
        response = responses[matched_intent]

        # Handle dialogue continuation for "order" intent
        if matched_intent == 'order':
            follow_up_state = 'order_check'
    
        # Handle dialogue continuation for "account" intent
        if matched_intent == 'account':
            follow_up_state = 'account_check'

        return response
    
    # Fallback responses if no intent is matched
    return responses['fallback']

# GUI function to send message and display response
def send_message():
    user_message = user_input.get() # Get the user input from the entry box
    chat_log.insert(tk.END, f'You: {user_message}\n') # Display user message in chat window

    # Get chatbot response and display it
    bot_message = chatbot_response(user_message)
    chat_log.insert(tk.END, f'Bot: {bot_message}\n')

    # Clear the input field after the message is sent
    user_input.delete(0, tk.END)

# Create the tkinter window
window = tk.Tk()
window.title("Chatbot")
window.geometry("500x500")

# Chat log where the conversation is displayed
chat_log = scrolledtext.ScrolledText(window, wrap=tk.WORD, height=20, width=50)
chat_log.pack(pady=10)

# Initial greeting message when the window opens
chat_log.insert(tk.END, 'Bot: Welcome! How can I assist you today? Here\'s what I can help with:\n1. Open time\n2. Place an order\n3. Account information\n')

# User input field
user_input = tk.Entry(window, width=40)
user_input.pack(pady=10)

# Button to send the message
send_button = tk.Button(window, text="Send", command=send_message)
send_button.pack()

# Start the GUI event loop
window.mainloop()
 
