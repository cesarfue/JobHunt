import json
import os
import re

from config import Config
from dotenv import load_dotenv
from openai import OpenAI
from services.json_helper import clean_json

load_dotenv()

API_KEY = os.getenv("API_KEY")
client = OpenAI(api_key=API_KEY)


class OpenAIService:

    def __init__(self, job_content):
        self.load_resume_data()
        self.extract_job_info(job_content)

    def load_resume_data(self):
        try:
            with open(Config.RESUME_JSON, "r", encoding="utf-8") as f:
                self.resume_json = json.dumps(
                    json.load(f), ensure_ascii=False, indent=2
                )
        except Exception as e:
            print(f"Error loading resume.json: {e}")
            return None

    def query(self, prompt, include_job_content, include_resume):
        full_prompt = prompt
        if include_job_content:
            full_prompt = f"{prompt}\n\n## Job content\n{self.job_content}"
        if include_resume:
            full_prompt = f"{prompt}\n\n# Mon CV (JSON)\n\n{self.resume_json}"

        response = client.chat.completions.create(
            model="gpt-4.1", messages=[{"role": "user", "content": full_prompt}]
        )
        return response.choices[0].message.content.strip()

    def extract_job_info(self, content):
        prompt = f"""
    À partir du texte de page web ci-dessous, retourne uniquement en JSON, sans aucune autre information:
    {{
    "company": "Nom de la société qui poste l'offre d'emploi",
    "job_title": "Intitulé du poste",
    "platform": "Plateforme d'offres d'emploi, en un mot (ex: Hellowork, Welcometothejungle, etc)",
    "job_description": "Contenu de l'offre d'emploi et du profil recherché"
    }}
    Offre d'emploi:
    {content}
    """
        response = self.query(prompt, False, False)

        try:
            cleaned_response = clean_json(response)
            self.job_content = json.loads(cleaned_response)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", response, re.DOTALL)
            if match:
                json_str = match.group(0)
                try:
                    self.job_content = json.loads(json_str)
                except Exception as e:
                    print(f"Still not valid JSON: {e}")
            raise ValueError(f"Invalid JSON returned by model: {response}")
