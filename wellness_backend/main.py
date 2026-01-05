from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from multi_agents import main_agent, draft_message

class SubscribeRequest(BaseModel):
    email: str

app = FastAPI()
#Allow React to talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://localhost:49622"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/subscribe")
def subscribe(payload: SubscribeRequest):
    #Later store in DB or send to marketing tool
    print("New email: ", payload.email)
    main_agent.invoke({"messages": [{
        "role": "user", 
        "content": "First search for a positive quote and wellness tip. Second, compose a wellness email and send the email to this subscriber: " + payload.email
    }]})
    return {"message": "Subscribed successfully"}