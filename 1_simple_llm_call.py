from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

model_ollama = ChatOllama(model = 'llama3.2')

# Simple one-line prompt
prompt = PromptTemplate.from_template("{question}")

model_openai = ChatOpenAI(temperature = 0.8)
parser = StrOutputParser()

# Chain: prompt → model → parser
chain = prompt | model_ollama | parser

# Run it
result = chain.invoke({"question": "What is an asymptote ?"})
print(result)
