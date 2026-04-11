import sqlite3
from pathlib import Path

import pandas as pd
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from tqdm import tqdm

from unga80.config import DATA_DIR, ROOT_DIR
from unga80.database import QUERIES

DB = DATA_DIR / "countries.db"
model: str = "artifish/llama3.2-uncensored"


def llm_call(model: str, template: str, text: str):
    llm = ChatOllama(
        model=model,
        temperature=0,
        keep_alive=False,
    )
    prompt = PromptTemplate.from_template(template)
    formatted_prompt = prompt.format(text=text)
    result = llm.invoke(formatted_prompt)
    return result


def update_database(db: Path, query: str):
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        cursor.close()


def generate_summary(model: str, text: str):
    template = """
    Summarize the following speech. Ignore the speaker and focus on the content:

    {text}
    """
    result = llm_call(model=model, template=template, text=text)
