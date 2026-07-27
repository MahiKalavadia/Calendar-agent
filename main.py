from fastapi import FastAPI
from langfuse import get_client
from langfuse.langchain import CallbackHandler
from agents import agent
from schemas import ChatRequest, ChatResponse
from logger import logger
from dotenv import load_dotenv

load_dotenv()

langfuse = get_client()
langfuse_handler = CallbackHandler()

app = FastAPI(
    name="Calender Scheduling Agent",
    description="Schedule Events inside Calender",
    version="1.0.0"
)

@app.get("/health")
def health():
    try:
        logger.info("Health check is working")
        return {
            "status":"ok"
        }
    finally:
        logger.info("Health check called!")
        langfuse.flush()

@app.post("/query", response_model=ChatResponse)
def query(request: ChatRequest):
    try:
        logger.info(f"User's query: {request.query}")
        logger.info("Invoking agent...")
        response = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": request.query
                    }
                ]
            },
            config = {
                        "callbacks" : [langfuse_handler]
                    }
        )
        logger.info(f"Invoked the agent.")
        answer = response["messages"][-1].content
        logger.info(f"Response received: {answer}")
        return ChatResponse(output=answer)
 
    except Exception as e:
        logger.error(f"Exception occurred: {str(e)}")
        return f"Exception occurred while processing query {request.query}!"
    finally:
        langfuse.flush()