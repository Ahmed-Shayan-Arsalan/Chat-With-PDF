# app.py
import os
import streamlit as st
from chatbot import ChatbotAgent

# Instantiate ChatbotAgent
chatbot_agent = ChatbotAgent()

# Function to save conversation to a text file
def save_conversation(user_query, bot_response):
    with open("conversation.pdf", "a") as file:
        file.write(f"User: {user_query}\n")
        file.write(f"Bot: {bot_response}\n\n")

# Function to erase conversation history
def erase_conversation_history():
    if os.path.exists("conversation.pdf"):
        os.remove("conversation.pdf")
    # Recreate the conversation.txt file
    with open("conversation.pdf", "w") as file:
        pass

# Streamlit app
def main():
    st.title("Sufi Chatbot")

    # Input field for user query
    user_query = st.text_input("Enter your query:")

    response = ""  # Initialize response variable

    if st.button("Ask"):
        # Query the QA interface with user input
        response = chatbot_agent.query_qa_interface(user_query)

        # Display the response
        st.write("Bot:", response)

        # Save conversation to text file
        save_conversation(user_query, response)

    # Previous inputs and outputs
    st.markdown("---")  # Separator
    st.write("Previous Conversations:")

    # Display previous conversations from text file
    with open("conversation.pdf", "r") as file:
        conversations = file.readlines()
        for line in conversations:
            st.write(line.strip())

    # Side button to erase conversation history
    if st.sidebar.button("Erase Conversation History"):
        erase_conversation_history()
        st.sidebar.write("Conversation history erased!")

if __name__ == "__main__":
    main()
