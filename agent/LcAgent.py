from langchain import LLMMathChain, OpenAI, SerpAPIWrapper, SQLDatabase, SQLDatabaseChain
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from agent.tools import QueryEmailsAndTickets, QueryManuals
from langchain.memory import ConversationBufferMemory

class LcAgent:
    def __init__(self) -> None:
        self.llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

        self.toolsss = [QueryManuals(), QueryEmailsAndTickets()]

        self.memory = ConversationBufferMemory(memory_key="chat_history")
        
        self.agent = initialize_agent(
                    agent='conversational-react-description', 
                    tools=self.toolsss, 
                    llm=self.llm,
                    verbose=True,
                    max_iterations=3,
                    memory=self.memory,
                )
        
def run(self, query):
    self.agent.run(query)