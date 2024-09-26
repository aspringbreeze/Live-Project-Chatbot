# Live Project Chatbot
## Introduction
This project implements chatbot for a pizza restaurant. First I built a Rule-based chabot using NLTK(WordNet) to match user intent. The chatbot can The chatbot can handle tasks such as taking orders and providing account information.

Then I built a Rule-based chabot using spaCy for Natural Language Processing (NLP). The chatbot can handle a broader range of user queries, even if they don’t fit the exact predefined structure, allowing for more flexible and natural interactions.

Last, I built an AI-based chatbot built using GPT-2 and PyTorch, trained to simulate a pizza restaurant assistant capable of dynamically responding to customer queries.
 
# Features
## Rule-based chabot
Intent Matching: User inputs are processed to match predefined intents (e.g., greeting, ordering).

NLP with spaCy: Tokenization and lemmatization are used to extract key words from user input for intent matching.

Response Logic: Predefined responses from a dictionary based on the matched intent guide the conversation.

Context-Aware Conversations: The chatbot maintains a follow-up state to manage context and ask relevant follow-up questions.

This bot uses deterministic rules to interact with users, providing consistent responses for common queries.

# AI-based chabot
GPT-2 Model: A fine-tuned transformer model that generates human-like responses to user inputs.

Custom Training Data: The model is trained on a dataset of pizza restaurant dialogues, covering orders, account inquiries, and business hours.

Flexible Conversations: Unlike the rule-based approach, this AI chatbot generates responses that adapt to the context of the conversation, making interactions more fluid and natural.

PyTorch for Training: Fine-tuning and training the model using PyTorch, with tokenization and data collation to prepare the conversational data.

This chatbot offers dynamic and varied responses, enhancing the customer experience with more human-like interactions.
