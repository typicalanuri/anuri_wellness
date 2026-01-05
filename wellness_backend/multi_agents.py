import os
import getpass
import smtplib
from email.mime.text import MIMEText
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

try:
    from dotenv import load_dotenv
    load_dotenv()
    langsmith_api_key = os.getenv("LANGSMITH_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    gmail_user = os.getenv("GMAIL_USER")
    gmail_password = os.getenv("GMAIL_PASSWORD")
    print("GMAIL_USER: ", gmail_user)
    print("GMAIL_PASSWORD: ", gmail_password)
except ImportError:
    pass


#Create a subagent
positivity_wellness_agent = create_agent(
    model="gpt-4o-mini",
    tools=[],
)
#Wrap positivity_wellness_agent in a tool]
@tool("get_positivity_wellness_agent", description="Search internet for an uplifting and positive quote to share with the user and a wellness tip to help the user improve their well-being. The tip could be related to physical health, mental health, nutrition, exercise, sleep, or stress management. An example of a wellness tip is to take a short walk during breaks to boost energy and reduce stress.")
def call_positivity_wellness_agent(query: str) -> str:
    result = positivity_wellness_agent.invoke({"messages": [{"role": "user", "content":query}]})
    print("positivity_wellness_agent result: ", result)
    return result["messages"][-1].content

wellness_tip_agent = create_agent(
    model="gpt-4o-mini",
    tools=[],
)

#Create a subagent
positivity_quote_agent = create_agent(
    model="gpt-4o-mini",
    tools=[],
)
#Wrap positivity_quote_agent in a tool]
@tool("get_positivity_quote", description="Search internet for an uplifting and positive quote to share with the user.")
def call_positivity_quote_agent(query: str) -> str:
    result = positivity_quote_agent.invoke({"messages": [{"role": "user", "content":query}]})
    print("Positivity Quote Agent Result: ", result)
    return result["messages"][-1].content

wellness_tip_agent = create_agent(
    model="gpt-4o-mini",
    tools=[],
)

@tool("get_wellness_tip", description="Search internet for a wellness tip to user with the user to help them improve their well-being. The tip could be related to physical health, mental health, nutrition, exercise, sleep, or stress management. An example of a wellness tip is to take a short walk during breaks to boost energy and reduce stress.")
def call_wellness_tip_agent(query: str):
    result = wellness_tip_agent.invoke({"messages": [{"role": "user", "content": query}]})
    print("Wellness Tip Agent Result: ", result)
    return result["messages"][-1].content

@tool
def send_email(to_email: str, subject: str, body: str) -> str:
    """Send an email to the specified address.
    
    Args:
        to_email (str): Recipient email address.
        subject (str): Subject of the email.
        body (str): Body of the email.
    """
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

email_agent = create_agent(
    model="gpt-4o-mini",
    tools=[send_email]
)

@tool("create_and_send_email", description="Create and send an email to the subscriber based given the positive quote and wellness tip. The email should be engaging and well-structured. Make sure to include a subject line and a friendly greeting.")
def call_email_agent(query: str):
    result = email_agent.invoke({"messages": [{"role": "user", "content": query}]})
    print("Email Agent Result: ", result)
    return result["messages"][-1].content

main_agent = create_agent(
    model="gpt-4o-mini",
    tools=[call_positivity_wellness_agent, call_email_agent]
)

def get_ai_response(user_input):
    model = ChatOpenAI(openai_api_key=openai_api_key, temperature=0, model="gpt-4.1-nano")
    messages = [SystemMessage("You an expert at providing motivational quotes that will uplift a person's day. Return 1 motivational quote and 1 activity to improve the user's mental " \
    "health for instance 'go for a walk in nature'."), HumanMessage(user_input)]
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

def draft_message(email:str):
    response = get_ai_response("I am feeling down and unmotivated. Can you provide me with a motivational quote and a wellness activity to help improve my mental health?")
    send_email("AnuriTalks: Your Motivational Quote Of The Day", response, email)
