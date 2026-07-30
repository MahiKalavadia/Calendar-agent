from langchain.agents import create_agent
from prompts import SYSTEM_PROMPT
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from tools import create_event, get_events, check_availability, cancel_event
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
import logging

load_dotenv()

logger = logging.getLogger(__name__)

llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash")
model = ChatGroq(model="llama-3.3-70b-versatile")
memory = InMemorySaver()

TOOLS = [
    create_event,
    get_events,
    check_availability,
    cancel_event
]

logger.info("Creating agent!")

agent = create_agent(
    model=model,
    tools=TOOLS,
    system_prompt=SYSTEM_PROMPT,
    checkpointer=memory
)