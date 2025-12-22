import streamlit as st

def about():
    st.title("About This Application")
    st.write(
        "This application is designed to create a subscription for users who want to recieve wellness quotes via email, daily. "
    )
    
    st.subheader("Features")
    st.write(
        "- Subscribe to daily motivational quotes and activities\n"
        "- View motivational quote history and activities\n"
    )
    
    st.subheader("Technologies Used")
    st.write(
        "- Streamlit for the web interface\n"
        "- LangChain for AI model integration\n"
        "- OpenAI for natural language processing"
    )
    st.subheader("Contributors")
    st.write(
        "Jessica Nwachukwu, a software engineer with a passion for AI and web development. "
        "She is dedicated to creating user-friendly applications that leverage the power of AI."
    )
    st.write(
        "If you have any questions or feedback, feel free to reach out by using the contact form on the homepage."
    )
if __name__ == "__main__":
    about()
    # Note: This is a simple about page. You can expand it with more details about the application, its features, and the team behind it.
    # This is a simple about page. You can expand it with more details about the application, its features, and the team behind it.