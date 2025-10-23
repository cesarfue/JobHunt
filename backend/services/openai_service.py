import json
import os
import re

from dotenv import load_dotenv
from openai import OpenAI

from config import Config

load_dotenv()

API_KEY = os.getenv("API_KEY")
client = OpenAI(api_key=API_KEY)


def query_openai(prompt):
    response = client.chat.completions.create(
        model="gpt-4.1", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


def extract_job_info(content):
    prompt = f"""
À partir du texte de page web ci-dessous, retourne uniquement en JSON, sans aucune autre information:
{{
  "company": "Nom de la société qui poste l'offre d'emploi",
  "job_title": "Intitulé du poste",
  "platform": "Plateforme d'offres d'emploi, en un mot",
  "job_description": "Contenu de l'offre d'emploi et du profil recherché"
}}
Offre d'emploi:
{content}
"""
    response = query_openai(prompt)

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", response, re.DOTALL)
        if match:
            json_str = match.group(0)
            try:
                return json.loads(json_str)
            except Exception as e:
                print(f"Still not valid JSON: {e}")
        raise ValueError(f"Invalid JSON returned by model: {response}")


def get_prompts():
    prompts = {}

    if not Config.PROMPTS_DIR.exists():
        print(f"Warning: Prompts directory not found: {Config.PROMPTS_DIR}")
        return prompts

    for filepath in Config.PROMPTS_DIR.glob("*.txt"):
        key = filepath.stem
        with open(filepath, "r", encoding="utf-8") as f:
            prompts[key] = f.read().strip()

    return prompts
