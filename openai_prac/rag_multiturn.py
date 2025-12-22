import redis
import os
import openai


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

r = redis.Redis(
    host='localhost',
    port=6379,
    db=0)

def add_football_player(player_id, name, age, club, position, ranking, goals):
    player_data = {
        'name': name,
        'age': age,
        'club': club,
        'position': position,
        'ranking': ranking,
        'goals': goals
    }
    r.hset(f"football_player:{player_id}", mapping=player_data)

def get_football_player(player_id):
    player_data = r.hgetall(f"football_player:{player_id}")
    if not player_data:
        return None
    return {key.decode('utf-8'): value.decode('utf-8') for key, value in player_data.items()}

def delete_football_player(player_id):
    r.delete(f"football_player:{player_id}")

def list_all_players():
    keys = r.keys("football_player:*")
    players = []
    for key in keys:
        player_data = r.hgetall(key)
        if player_data:
            players.append({k.decode('utf-8'): v.decode('utf-8') for k, v in player_data.items()})
    return players

def chatbot(messages):
    while True:
        question = input("Ask a question about football players (or type 'exit' to quit): ")
        if question.lower() != 'exit':
            messages.append({"role": "user", "content": f"{question}\nSources: {messages}"})
            response = openai.OpenAI(api_key= openai_api_key).chat.completions.create(model="gpt-4.1-nano", messages=messages)
            



if __name__ == "__main__":
    add_football_player(1, "Lionel Messi", 36, "Inter Miami", "Forward", 1, 800)
    add_football_player(2, "Cristiano Ronaldo", 38, "Al Nassr", "Forward", 2, 850)
    
    print("All Players: \n", list_all_players())

