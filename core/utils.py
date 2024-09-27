import google.generativeai as genai
import os
from dotenv import load_dotenv
from difflib import SequenceMatcher


load_dotenv()


def init_sessions(request):
    request.session["i"] = 0
    request.session["menu_option"] = None
    request.session["question_ia"] = None


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Inicialize o histórico fora da função
historico = []


def similar(a, b):
    print(SequenceMatcher(None, a, b).ratio())
    return SequenceMatcher(None, a, b).ratio()


def create_prompt(context: str):
    global historico

    # Define um limite de similaridade para considerar a mudança de contexto
    LIMITE_SIMILARIDADE = 0.2

    # Verifica se o histórico não está vazio
    if historico:
        ultima_pergunta = historico[-1].replace("Pergunta: ", "")
        if similar(ultima_pergunta, context) < LIMITE_SIMILARIDADE:
            # Reinicia o histórico se a nova pergunta for significativamente diferente
            historico = []

    # Adiciona a nova pergunta ao histórico
    historico.append(f"Pergunta: {context}")

    response = model.generate_content(f"""Você é um especialista em medicina ocular. Quando receber uma pergunta, verifique se ela está relacionada a condições oculares, tratamentos ou cuidados. 

- Se a pergunta não for sobre medicina ocular, responda que não está capacitado para ajudar.
- Se a pergunta for pertinente, forneça uma resposta clara e objetiva de forma amigável. 

Caso o usuário pergunte sobre o Centro Óptico Visão Futurista, forneça as seguintes informações:

**Centro Óptico Visão Futurista:**  
Localizado na Avenida das Inovações, 123, em Lumina, com fácil acesso a transporte público e estacionamento.  
Oferecemos:
- Exames de visão avançados
- Lentes e armações personalizadas
- Óptica digital
- Consultoria de estilo
- Atendimento ao cliente
- Serviços de saúde ocular  

**Contato:**
- Telefone: (11) 1234-5678
- E-mail: contato@visao-futurista.com
- App WhatsApp: (11) 1234-5678
Inclua na sua resposta icones bem descritivos.
No final da resposta sobre condições oculares, incentive o usuário a entrar em contato com o Centro Óptico Visão Futurista se tiver alguma dúvida ou condição ocular.
    Histórico de Perguntas:
    {', '.join(historico)}\n
    Pergunta: {context}""")

    return response.text
