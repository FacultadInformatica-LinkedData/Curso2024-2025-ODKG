import streamlit as st
import chat  # Import rag.py



def main():
    # Set the Streamlit page title
    st.title("LLM Chatbot with RAG and Sidebar")

    # Run the RAG code
    chat.main() 


if __name__ == "__main__":
    main()

# Para ejecutarlo -> streamlit run main.py