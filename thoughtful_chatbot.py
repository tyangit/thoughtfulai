from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import gradio as gr
import os
import json

# %%
MODEL = "gpt-4.1-nano"
DB_NAME = "vector_db"
load_dotenv(override=True)


# %%
llm = ChatOpenAI(temperature=0, model_name=MODEL)

# %%
SYSTEM_PROMPT_TEMPLATE = """
You are a knowledgeable, friendly customer service support representing the company Thoughtful AI.
You are chatting with a user about Thoughtful AI.
If relevant, use the given context to answer any question.  

Context:
{context}
"""

# %%
def getContext():
    filename = "./thoughtful.json"
    try:   
    # Open the file in read mode ('r')
        with open(filename, 'r') as file:
            # Use json.load() to parse the file data into a Python object
            data = json.load(file)
    except FileNotFoundError:
        print("Error: The file "+ filename + " was not found.")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from the file (malformed JSON).")

    text = ""
    for item in data["questions"]:
        text += "Question: " + item["question"] + "\n"
        text += "Answer: " + item["answer"] + "\n\n"

    return text
    

# %%
def answer_question(question: str, history):
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(context=getContext())
    response = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=question)])
    return response.content

# %%
gr.ChatInterface(answer_question).launch()


