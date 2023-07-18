import os
from pydantic import BaseModel, Field
from typing import List
from superagi.llms.base_llm import BaseLlm

def generate(self, prompt, metr)->bool:
    prompt = prompt.replace("{metr}", metr)

    messages = [{"role": "system", "content": prompt}]
    result = int(self.llm.chat_completion(messages, max_tokens=self.max_token_limit))
    return result

def getMetric(metr: str) -> List[str]:
    p = []

    prompt = """1, if given {metr} means for the number of active users, else 0."""
    if generate(prompt,metr):
        p.append("activeUsers")
    prompt = """1, if given {metr} means for the number of times users added items to their shopping carts., else 0."""
    if generate(prompt,metr):
        p.append("addToCarts")
    p.append("country")
    return p

def getDim(dim: str) -> List[str]:
    p=[]
    prompt = """1, if given {dim} means names of the cities the user activity originated from, else 0."""
    if generate(prompt,dim):
        p.append("city")
    prompt = """1, if given {dim} means the IDs of the cities the user activity originated from, else 0."""
    if generate(prompt, dim):
        p.append("cityId")
    prompt = """1, if given {dim} means the name of the marketing campaign, else 0."""
    if generate(prompt, dim):
        p.append("campaignName")
    p.append("addToCarts")
    return p