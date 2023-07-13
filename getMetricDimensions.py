import os
from pydantic import BaseModel, Field
from typing import List

def getMetric(self, metr: str) -> List[str]:
    p = []

    prompt = """1, if given {metr} means for the number of active users, else 0."""

    prompt = prompt.replace("{metr}", metr)

    messages = [{"role": "system", "content": prompt}]
    result = int(self.llm.chat_completion(messages, max_tokens=self.max_token_limit))
    if result:
        p.append("activeUsers")
    return p

def getDim(self, dim: str) -> List[str]:
    p=[]
    prompt = """1, if given {dim} means names of the cities the user activity originated from, else 0."""

    prompt = prompt.replace("{dim}", dim)

    messages = [{"role": "system", "content": prompt}]
    result = int(self.llm.chat_completion(messages, max_tokens=self.max_token_limit))
    if result:
        p.append("city")
    return p