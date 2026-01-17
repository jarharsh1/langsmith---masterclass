from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

os.environ['LANGCHAIN_PROJECT'] = 'Sequential LLM App'

load_dotenv()

prompt1 = PromptTemplate(
    template='Generate a detailed report on \n {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='Generate a 7 pointer summary from the following text \n {text}',
    input_variables=['text']
)

model_openai = ChatOpenAI(model = 'gpt-4o-mini',temperature = 0.7)
model_ollama_3_2 = ChatOllama(model = 'llama3.2', tempearture = 0.86)
model_ollama_qwen = ChatOllama(model = 'ChatOllama(model="qwen2.5vl:7b")')

parser = StrOutputParser()

chain = prompt1 | model_ollama_3_2 | parser | prompt2 | model_openai | parser

config ={
        'run_name':'Sequential_chain',
        'tags':['llm-app','report-generation','summarization'],
         'metadata':{
                'model1':'llama3.2',
                'model1_temp': 0.7,
                'model2':'llama3.2',
                'model2_temp': 0.86}}

result = chain.invoke({'topic': 'Steps to do LLM Finetuning?'}, config= config)

print(result)
