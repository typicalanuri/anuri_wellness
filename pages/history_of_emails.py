import streamlit as st

def history_of_emails():
    st.title("History of Emails")
    st.write(
        "This page will display the history of emails sent and received."
        "You can view the details of each email, including the sender, recipient, subject, and content."
    )
    
    # Placeholder for email history
    email_history = [
        {
            "sender": ""
        }
    ]

if __name__ == "__main__":
    history_of_emails()
    # Note: The actual email history data should be fetched from a database or an API.
    # This is just a placeholder to demonstrate the structure of the page.