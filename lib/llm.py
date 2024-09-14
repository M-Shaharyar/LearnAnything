from openai import OpenAI
from pydantic import BaseModel
import pandas as pd
import streamlit as st
import os

base_url = "https://api.aimlapi.com/v1"
api_key = os.getenv("AIML_API_KEY")

system_prompt = "You are an AI tutor. Be descriptive and helpful."

api = OpenAI(api_key=api_key, base_url=base_url)

class FlashcardList(BaseModel):
    flashcards: list[(str, str)]

def get_flashcards(document, n):

    user_prompt = f"""
        Prepare {n} questions from the input document.
        Each question should be related to some important information like: fact, place, person, date, work.
        Questions should be so formulated as the answer is only one word.

        Return questions and answers in CSV format.

        __

        Output example:

        Question1, answer1
        Question2, answer2

        ---
        {document}
        ---
        """


    completion = api.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.01,
        max_tokens=16000,
        response_format=FlashcardList,
    )

    response = completion.choices[0].message.parsed
    q = [r.split(', ') for r in response.flashcards]
    df = pd.DataFrame(q, columns=['Question', 'Answer'])

    return df


def run_openai(prompt):

    try:
        # Sending the answer text to OpenAI API using the updated method
        completion = api.chat.completions.create(
            model="gpt-4o-2024-08-06",  # You can choose a different model as needed
            messages=[
              {"role": "system", "content": system_prompt},
              {"role": "user", "content": prompt}
            ]
            )
        return completion.choices[0].message.content  # Display the response
    except Exception as e:
        return
        #st.write("An error occurred:", e) 



def get_question(document):

    # st.write(document)

    user_prompt = f"""
        Prepare one questions from the input document.
        The question should be related to some important information like: fact, place, person, date, work.
        Write only this question, without any introduction or explaination.
        ---
        {document}
        ---
        """

    return run_openai(user_prompt)