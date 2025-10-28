from ollama import Client

client = Client(host='http://localhost:11434')

def ask_ollama(prompt):
    
    response = client.chat(model="llama3", messages=[
        {"role": "system",
         "content": "Tu es un assistant expert en finance et en droit. "
         "Réponds avec clarté et précision."
         "Si la question est posé dans une langue donnée réponds toujours avec courtoisie et politesse dans la langue donnée.",
         "temparature": 0.6
        },
        {"role": "user", "content": prompt},
    ])
    return response['message']['content']