from dotenv import load_dotenv

load_dotenv('/home/mohan/Documents/learning/agents_learn/.env')

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama


def llm_google():
    llm_gemini = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        # other params...
    )
    return llm_gemini


def llm_ollama_model():
    llm_ollama = ChatOllama(temperature=0, model="deepseek-r1:1.5b")
    return llm_ollama
