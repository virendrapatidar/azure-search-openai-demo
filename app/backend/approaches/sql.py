from text import nonewlines
from approaches.approach import Approach
import openai
import os
import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import text
import urllib.parse
urllib.parse.quote_plus("123")


class SqlApproach(Approach):
    def __init__(self, chatgpt_deployment: str, gpt_deployment: str,):
        self.chatgpt_deployment = chatgpt_deployment
        self.gpt_deployment = gpt_deployment
        self.transactions = pd.read_csv('data/Orders.csv')
        self.transactions.head()
        self.temp_db = create_engine('sqlite:///:sqllitedatabase', echo=True)
        # self.transactions.to_sql(name='transactions',con=self.temp_db)

    def create_table_definition(self, df):
        prompt = """### sqlite SQL table, with its properties:
        #
        # transactions({})
        #
        """.format(",".join(str(col) for col in df.columns))
        return prompt

    def combine_prompts(self, df, query_prompt):
        definition = self.create_table_definition(df)
        query_init_string = f"### A query to answer: {query_prompt}\n SELECT"
        return definition+query_init_string

    def run(self, q: str, overrides: dict) -> any:
        self.results = None
        response = openai.Completion.create(
            engine=self.chatgpt_deployment,
            model=self.gpt_deployment,
            prompt=self.combine_prompts(self.transactions, q),
            temperature=0,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0,
            presence_penalty=0,
            stop=['#', ';']
        )
        with self.temp_db.connect() as conn:
            query = f"SELECT {response.choices[0].text}"
            records = conn.execute(text(query)).fetchall()           
            return str(records)
           
