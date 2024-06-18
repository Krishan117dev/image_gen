# main.py
from fastapi import FastAPI, Body
from app_fuctions.fucstions import generate_prompt,process_prompts
import re
app = FastAPI()

@app.post("/generate_prompts")
async def process_prompts_endpoint(L2_Category: str, L1_Category: str, directory: str):
    process_prompts(L2_Category, L1_Category, directory)
    return {"message": "Prompts processed successfully"}