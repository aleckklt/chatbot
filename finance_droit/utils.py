from ollama import Client
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

client = Client(host='http://localhost:11434')

KNOWLEDGE_PAGES = {
    "droit_international": [
        "https://www.un.org/fr/",
        "https://www.ohada.org/",
        "https://www.wto.org/",
        "https://www.ilo.org/global/lang--fr/index.htm",
        "https://eur-lex.europa.eu/",
    ],
    "finance_internationale": [
        "https://www.imf.org/fr/Home",
        "https://www.worldbank.org/fr",
        "https://www.bis.org/",
        "https://www.sec.gov/",
        "https://www.ecb.europa.eu/home/html/index.fr.html",
    ],
    "droit_pays": [
        "https://www.legifrance.gouv.fr/",
        "https://www.gouv.bj/",
        "https://www.usa.gov/",
        "https://www.canada.ca/fr.html",
        "https://www.gov.uk/",
        "https://www.china.org.cn/",
    ],
    "finance_pays": [
        "https://www.finances.gouv.fr/",
        "https://www.finances.gouv.bj/",
        "https://www.federalreserve.gov/",
        "https://www.bankofcanada.ca/",
        "https://www.bceao.int/",
    ],
    "numerique_droit": [
        "https://www.itu.int/",
        "https://www.wipo.int/portal/fr/",
        "https://www.ansib.bj/",
        "https://www.cnil.fr/",
        "https://www.ftc.gov/",
    ]
}

def smart_scrape_website(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        main_content = (soup.find('main') or 
                       soup.find('article') or 
                       soup.find('div', class_=re.compile('content|main|article')) or
                       soup.find('body'))
        
        if main_content:
            for element in main_content(["script", "style", "nav", "header", "footer", "aside"]):
                element.decompose()
            text = main_content.get_text()
        else:
            text = soup.get_text()
        
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        clean_text = ' '.join(chunk for chunk in chunks if chunk)
        
        return clean_text[:2000]
        
    except Exception as e:
        return ""

def get_smart_knowledge(user_message):
    user_lower = user_message.lower()
    relevant_urls = []
    
    if any(word in user_lower for word in ['droit', 'loi', 'juridique', 'legal']):
        relevant_urls.extend(KNOWLEDGE_PAGES['droit_international'][:2])
    
    if any(word in user_lower for word in ['finance', 'économique', 'banque', 'investissement', 'crédit']):
        relevant_urls.extend(KNOWLEDGE_PAGES['finance_internationale'][:2])
    
    if any(word in user_lower for word in ['numérique', 'digital', 'internet', 'cyber', 'technologie']):
        relevant_urls.extend(KNOWLEDGE_PAGES['numerique_droit'][:2])
    
    if any(word in user_lower for word in ['france', 'français']):
        relevant_urls.extend([KNOWLEDGE_PAGES['droit_pays'][0], KNOWLEDGE_PAGES['finance_pays'][0]])
    
    if any(word in user_lower for word in ['bénin', 'benin']):
        relevant_urls.extend([KNOWLEDGE_PAGES['droit_pays'][1], KNOWLEDGE_PAGES['finance_pays'][1]])
    
    if any(word in user_lower for word in ['usa', 'états-unis', 'américain']):
        relevant_urls.extend([KNOWLEDGE_PAGES['droit_pays'][2], KNOWLEDGE_PAGES['finance_pays'][2]])
    
    if any(word in user_lower for word in ['canada', 'canadien']):
        relevant_urls.extend([KNOWLEDGE_PAGES['droit_pays'][3], KNOWLEDGE_PAGES['finance_pays'][3]])
    
    if any(word in user_lower for word in ['uk', 'royaume-uni', 'britannique']):
        relevant_urls.extend([KNOWLEDGE_PAGES['droit_pays'][4], KNOWLEDGE_PAGES['finance_pays'][3]])
    
    if any(word in user_lower for word in ['chine', 'chinois']):
        relevant_urls.extend([KNOWLEDGE_PAGES['droit_pays'][5], KNOWLEDGE_PAGES['finance_internationale'][0]])
    
    if not relevant_urls:
        relevant_urls = KNOWLEDGE_PAGES['droit_international'][:1] + KNOWLEDGE_PAGES['finance_internationale'][:1]
    
    return list(set(relevant_urls))[:3]

def ask_ollama(prompt):
    relevant_urls = get_smart_knowledge(prompt)
    
    web_content = ""
    for url in relevant_urls:
        content = smart_scrape_website(url)
        if content and "Erreur" not in content:
            web_content += f"\n--- {url} ---\n{content}\n"

    current_date = datetime.now().strftime("%d/%m/%Y")
    current_year = datetime.now().strftime("%Y")
    
    enhanced_prompt = f"""
**CONTEXTE INTERNATIONAL {current_year} :**
- Date : {current_date}
- Organisations : ONU, FMI, Banque Mondiale, OMC, OIT, OHADA, UE
- Systèmes juridiques : Common Law, Civil Law, Droit Musulman
- Actualité financière mondiale

**SOURCES CONSULTÉES :**
{web_content if web_content else "Aucune source spécifique consultée"}

**QUESTION :** {prompt}

**RÉPONSE DIRECTE :**
"""
    
    response = client.chat(model="llama3", messages=[
        {"role": "system",
         "content": "Tu es un assistant expert en finance et en droit. Tu ne réponds qu'aux questions sur la finance et le droit."
                    "Réponds avec clarté et précision aux questions posées par l'utilisateur en utilisant uniquement les informations fournies."
                    "Réponds toujours avec courtoisie et politesse."},
        {"role": "user", "content": enhanced_prompt},
    ], options={"temperature": 0.4})
    return response['message']['content']