from langchain.agents import create_agent
from prompts.prompts import SYSTEM_PROMPT
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from tools.create_event import create_event
from tools.get_events import get_events
from tools.cancel_event import cancel_event
from tools.check_availability import check_availability
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
import logging

load_dotenv()

logger = logging.getLogger(__name__)

llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash")
# model = ChatGroq(model="llama-3.3-70b-versatile")
memory = InMemorySaver()

TOOLS = [
    create_event,
    get_events,
    check_availability,
    cancel_event
]

logger.info("Creating agent!")

agent = create_agent(
    model=llm,
    tools=TOOLS,
    system_prompt=SYSTEM_PROMPT,
    checkpointer=memory
)