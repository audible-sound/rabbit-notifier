from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from RabbitProducer import RabbitProducer

app = FastAPI()

class Message(BaseModel):
  receiver: str
  data: str
  
@app.on_event("startup")
def startup_event():
  global producer
  producer = RabbitProducer(host="rabbitmq", port=5672, username="pbc", password="password")
  
@app.post("/publish-message")
def publish_message(request: Message):
  try:
    producer.publish_message("incident_report", dict(request))
    return {"status": "Message sent succesfully!"}
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Failed to send message: {e}")
