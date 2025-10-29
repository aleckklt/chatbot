from ollama import Client

client = Client(host='http://localhost:11434')

KNOWLEDGE_BASE = {
    "droit_consommation": [
        "https://www.service-public.fr/particuliers/vosdroits/F1902",
        "https://www.economie.gouv.fr/dgccrf/garantie-legale-de-conformite",
        "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032038849/"
    ],
    "droit_travail": [
        "https://www.service-public.fr/particuliers/vosdroits/F2240",
        "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006900879/",
        "https://www.service-public.fr/particuliers/vosdroits/F41571"
    ],
    "finance_credit": [
        "https://www.banque-france.fr/credits-et-endettement",
        "https://www.amf-france.org/espace-epargnants/arbitrer-mes-placements/diversifier-son-epargne",
        "https://www.service-public.fr/particuliers/vosdroits/N34"
    ],
    "fiscalite": [
        "https://www.impots.gouv.fr/portail/",
        "https://www.service-public.fr/particuliers/vosdroits/N411",
        "https://www.impots.gouv.fr/particulier/le-pfu-ou-flat-tax"
    ],
    "epargne": [
        "https://www.amf-france.org/",
        "https://www.service-public.fr/particuliers/vosdroits/N461",
        "https://www.banque-france.fr/epargne"
    ],
    "protection_donnees": [
        "https://www.cnil.fr/",
        "https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000036750024"
    ]
}

def get_relevant_knowledge(user_message):
    relevant_urls = []
    user_lower = user_message.lower()
    if any(word in user_lower for word in ['rétractation', 'consommateur', 'garantie', 'achat']):
        relevant_urls.extend(KNOWLEDGE_BASE['droit_consommation'][:2])
    
    if any(word in user_lower for word in ['travail', 'emploi', 'cdi', 'démission']):
        relevant_urls.extend(KNOWLEDGE_BASE['droit_travail'][:2])
    
    if any(word in user_lower for word in ['crédit', 'prêt', 'endettement', 'banque']):
        relevant_urls.extend(KNOWLEDGE_BASE['finance_credit'][:2])
    
    if any(word in user_lower for word in ['impôt', 'fiscal', 'taxe', 'déclaration']):
        relevant_urls.extend(KNOWLEDGE_BASE['fiscalite'][:2])
    
    if any(word in user_lower for word in ['épargne', 'placement', 'investissement']):
        relevant_urls.extend(KNOWLEDGE_BASE['epargne'][:2])
    
    if any(word in user_lower for word in ['données', 'rgpd', 'vie privée']):
        relevant_urls.extend(KNOWLEDGE_BASE['protection_donnees'][:2])

    return list(set(relevant_urls))[:3]

def ask_ollama(prompt):
    relevant_urls = get_relevant_knowledge(prompt)
    
    if relevant_urls:
        urls_text = "Sources officielles pertinentes :\n- " + "\n- ".join(relevant_urls)
        enhanced_prompt = f"{urls_text}\n\nQuestion : {prompt}\n\nRéponds en t'appuyant sur ces sources officielles :"
    else:
        enhanced_prompt = prompt
    
    response = client.chat(model="llama3", messages=[
        {"role": "system",
         "content": "Tu es un assistant expert en finance et en droit. Tu ne réponds qu'aux questions sur la finance et le droit."
                    "Réponds avec clarté et précision aux questions posées par l'utilisateur en utilisant uniquement les informations fournies."
                    "Réponds toujours avec courtoisie et politesse."},
        {"role": "user", "content": enhanced_prompt},
    ], options={"temperature": 0.4})
    return response['message']['content']