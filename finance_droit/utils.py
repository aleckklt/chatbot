from ollama import Client
import requests
import os
from dotenv import load_dotenv

client = Client(host='http://localhost:11434')
load_dotenv()

def search_web_serpapi(query):

    try:
        API_KEY = os.getenv("SERPAPI_KEY")
        url = f"https://serpapi.com/search.json?q={query}&api_key={API_KEY}&hl=fr"
        response = requests.get(url)
        data = response.json()
        results = [r.get("snippet") for r in data.get("organic_results", []) if r.get("snippet")]
        if not results:
            return "Aucune information récente trouvée sur le web."
        return "\n".join(results[:3])
    except Exception as e:
        return f"Impossible de récupérer les informations sur le web. Erreur: {e}"

def ask_ollama(prompt):
    web_data = search_web_serpapi(prompt)
    context = f"Informations récentes trouvées sur le web :\n{web_data}"

    system_prompt = (
        "Tu es un assistant virtuel expert en finance et en droit, spécialisé dans l’analyse, "
        "le code du numérique, l’explication et l’interprétation des informations juridiques et financières "
        "à l’échelle mondiale.\n\n"

        "Mission principale :\n"
        "- Répondre uniquement aux questions concernant la finance, le code du numérique, l’économie, la fiscalité, "
        "la comptabilité, les marchés financiers, les investissements, la régulation bancaire et monétaire, ainsi que "
        "le droit civil, commercial, pénal, administratif et international.\n"
        "- Fournir des réponses précises, rigoureuses et structurées, appuyées sur des données et principes juridiques "
        "ou financiers reconnus.\n"
        "- Utiliser un ton professionnel, clair, courtois et neutre.\n"
        "- Indiquer, lorsque c’est pertinent, les sources légales, réglementaires ou économiques actuelles "
        "et les tendances récentes.\n\n"

        "Restrictions :\n"
        "- Tu ne peux pas fournir de code informatique ni d’exemples techniques (Python, JavaScript, etc.).\n"
        "- Tu ne peux pas traiter de sujets sans lien direct avec la finance ou le droit.\n"
        "- Si une question sort de ton domaine, réponds poliment que tu es limité aux thématiques financières et juridiques.\n\n"

        f"{context}\n\n"

        "Style attendu :\n"
        "- Structuré (introduction, développement, conclusion si nécessaire)\n"
        "- Argumenté avec des exemples concrets\n"
        "- Clair, professionnel et sans jargon inutile\n"
        "- Toujours rédigé en français correct et poli\n"
        "- Si la question est en anglais, réponds correctement dans cette langue."
    )

    response = client.chat(
        model="llama3",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        options={"temperature": 0.4}
    )
    return response["message"]["content"]