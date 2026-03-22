import os
import yaml
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

load_dotenv()

def load_llm(provider="groq"):
    """Load LLM based on provider name"""
    with open("config/config.yaml") as f:
        config = yaml.safe_load(f)

    if provider == "groq":
        return ChatGroq(
            model=config["llm"]["model"],
            api_key=os.getenv("GROQ_API_KEY")
        )
    elif provider == "openai":
        return ChatOpenAI(
            model_name="gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY")
        )
    else:
        raise ValueError(f"Unknown provider: {provider}")
