import os
import getpass
import smtplib
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_tavily import TavilySearch
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.schema import HumanMessage
from email.mime.text import MIMEText
from langchain_openai import ChatOpenAI
import streamlit as st

try:
    from dotenv import load_dotenv
    load_dotenv()
    langsmith_api_key = os.getenv("LANGSMITH_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    gmail_user = os.getenv("GMAIL_USER")
    gmail_password = os.getenv("GMAIL_PASSWORD")
except ImportError:
    pass

def wellness_email_main():
    try:
        from dotenv import load_dotenv
        load_dotenv()
        langsmith_api_key = os.getenv("LANGSMITH_API_KEY")
        openai_api_key = os.getenv("OPENAI_API_KEY")
        tavily_api_key = os.getenv("TAVILY_API_KEY")
        gmail_user = os.getenv("GMAIL_USER")
        gmail_password = os.getenv("GMAIL_PASSWORD")
    except ImportError:
        pass

    os.environ["LANGCHAIN_TRACING"] = "true"
    if "LANGSMITH_API_KEY" not in os.environ:
        os.environ["LANGSMITH_API_KEY"] = getpass.getpass(
            prompt="Enter your LangChain API key (optional): "
        )
    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = getpass.getpass(
            prompt="Enter your OpenAI API key (optional): "
        )

    model = init_chat_model(
        "gpt-4.1-nano",
        model_provider="openai"
    )
    messages = [
        SystemMessage("Translate the following from English to French"),
        HumanMessage("Hi, how are you?"),
    ]

    # user_input = input("Enter your message (or type 'exit' to quit): ")
    # if user_input.lower() == "exit":
    #     break
    # messages.append(HumanMessage(user_input))
    # response = model.invoke(messages)
    # messages.append(AIMessage(response.content))
    # print(f"Assistant: {response.content}")
    # for token in model.stream(messages):
    #     print(token.content, end="")
    # tool = TavilySearch(
    #     max_results=5,
    #     topic="general",
    # )
    # tool_msg = tool.invoke({"query": "What happened at the last Wimbledon?"})
    # print(tool_msg)
    # search = TavilySearchResults(max_results=2)
    # search_results = search.invoke({"query": "What is the weather in SF?"})
    # print("Search Results: ", search_results)
    # tools = [search]
def get_ai_response(user_input):
    model = ChatOpenAI(openai_api_key=openai_api_key, temperature=0, model="gpt-4.1-nano")
    messages = [SystemMessage("You an expert at providing motivational quotes that will uplift a person's day. Return 1 motivational quote and 1 activity to improve the user's mental " \
    "health for instance 'go for a walk in nature'. The user will provide what they are feeling and going through"), HumanMessage(user_input)]
    response = model.invoke(messages)
    return response.content

def send_email(subject, body, to_email):
    msg = MIMEText(body, "plain")
    msg['Subject'] = subject
    msg['From'] = gmail_user
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(gmail_user, gmail_password)
            server.send_message(msg)
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")


if __name__ == "__main__":
    st.title("🤖 AnuriTalks: Your Motivational Quote Of The Day")
    user_input = st.text_input("How are you feeling at the moment? Be Honest, I am here for you. ")
    email = st.text_input("Enter your email address: ")
    if st.button("Get Motivational Quote"):
        try:
            response = get_ai_response(user_input)
            send_email("AnuriTalks: Your Motivational Quote Of The Day", response, email)
            st.success("Motivational quote sent to your email!")
        except Exception as e:
            print(f"An error occurred: {e}")
