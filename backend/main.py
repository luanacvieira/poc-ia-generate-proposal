from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
from pydantic import BaseModel
import re

app = FastAPI()
 
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins= ["http://localhost:5500", "http://127.0.0.1:5500"],  # coloque exatamente a origem que está acessando o backend
    allow_credentials=True,
    allow_methods=["*"],


    allow_headers=["*"],
)
 
# Azure OpenAI configuration (replace with your keys and endpoint)
openai.api_type = "azure"
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = "2023-05-15" #"gpt-4o-2024-11-20" #"2023-05-15"
 
class PromptRequest(BaseModel):
    section: str
    content: str

class BriefingRequest(BaseModel):
    briefing: str
 
@app.post("/generate")
async def generate_all_sections(request: BriefingRequest):
    sections = [
        "Client Stated Needs",
        "Corresponding Strategic Objectives",
        "Key Issues and Problems",
        "Opportunities",
        "Client Value Objectives",
        "Corresponding Solution Components"
    ]

# Defina um prompt específico para cada seção
    section_prompts = {
        "Client Stated Needs": (
            "Você é um assistente de IA especializado em propostas comerciais.\n"
            f"Baseado no briefing geral: '''{request.briefing}''', crie um texto para a seção 'Client Stated Needs'.\n"
            " Esse texto deve serfeito baseado nesse briefing fazendo levantamento das Necessidades declaradas pelo cliente"
            "Para ajudar entender a estrutura do texto que deve xer criado, aqui um exemplo de 3 topicos criados para apresentar as necessidades declaradas de um cliente aleatorio:"
            "1. Transformar a organização por meio da tecnologia de IA generativa."
            "2. Melhorar a eficiência operacional e a experiência dos funcionários e clientes."
            "3. Lançar novos produtos e serviços com tempo de lançamento no mercado reduzido."
            "Liste claramente as necessidades declaradas pelo cliente com base no briefing abaixo. "
            "Responda em até 3 tópicos objetivos, estruturados e claros, em HTML (use <ul><li>)."
        ),
        "Corresponding Strategic Objectives": (
            "Você é um assistente de IA especializado em propostas comerciais.\n"
            f"Baseado no briefing geral: '''{request.briefing}''', crie um texto para a seção 'Corresponding Strategic Objectives'.\n"
            " Esse texto deve ser feito baseado nesse briefing fazendo levantamento dos Objetivos Estratégicos declarados pelo cliente"
            "Para ajudar entender a estrutura do texto que deve xer criado, aqui um exemplo de 3 topicos criados para apresentar as necessidades declaradas de um cliente aleatorio:"
            "1. Aumente a eficiência operacional com a automação orientada por IA."
            "2. Aumente o engajamento de funcionários e clientes com soluções personalizadas."
            "3. Acelere a inovação de produtos e serviços integrando IA aos fluxos de trabalho."
            "Com base no briefing, identifique e Liste claramente os objetivos estratégicos correspondentes do cliente. "
            "Responda em até 3 tópicos objetivos, estruturados e claros, em HTML (use <ul><li>)."
        ),
        "Key Issues and Problems": (
            "Você é um assistente de IA especializado em propostas comerciais.\n"
            f"Baseado no briefing geral: '''{request.briefing}''', crie um texto para a seção 'Key Issues and Problems'.\n"
            " Esse texto deve serfeito baseado nesse briefing fazendo levantamento dos Principais problemas e questões declarados pelo cliente"
            "Para ajudar entender a estrutura do texto que deve xer criado, aqui um exemplo de 3 topicos criados para apresentar as problemas e questões declarados por um cliente aleatorio:"
            "1. Falta de escalabilidade para lidar com grandes volumes de interações de IA."
            "2. Complexidades de integração entre sistemas e modelos de IA."
            "3. Flexibilidade limitada na personalização de soluções de IA para necessidades comerciais específicas."
            "Aponte os principais problemas e desafios enfrentados pelo cliente, conforme o briefing. "
            "Responda em até 3 tópicos objetivos, estruturados e claros, em HTML (use <ul><li>)."
        ),
        "Opportunities": (
            "Você é um assistente de IA especializado em propostas comerciais.\n"
            f"Baseado no briefing geral: '''{request.briefing}''', crie um texto para a seção 'Opportunities'.\n"
            "Esse texto deve ser feito baseado nesse briefing fazendo levantamento dos Principais oportunidades de projeto com o cliente"
            "Para ajudar entender a estrutura do texto que deve xer criado, aqui um exemplo de 3 topicos criados para apresentar as oportunidades levantadas ou declaradas de um cliente aleatorio:"
            "1. Implemente uma plataforma de IA escalável para lidar com o crescimento futuro."
            "2. Use o suporte a vários modelos para uma integração perfeita com diversas soluções de IA."
            "3. Crie uma plataforma flexível e de baixo código para personalizar fluxos de trabalho rapidamente."
            "Identifique oportunidades relevantes para o cliente a partir do briefing. "
            "Responda em até 3 tópicos objetivos, estruturados e claros, em HTML (use <ul><li>)."
        ),
        "Client Value Objectives": (
            "Você é um assistente de IA especializado em propostas comerciais.\n"
            f"Baseado no briefing geral: '''{request.briefing}''', crie um texto para a seção 'Client Value Objectives'.\n"
            "Esse texto deve ser feito baseado nesse briefing fazendo levantamento dos Principais Objetivos de valor para o cliente"
            "Para ajudar entender a estrutura do texto que deve ser criado, aqui um exemplo de 3 topicos criados para apresentar as os Principais Objetivos de valor para o cliente levantadas ou declaradas de um cliente aleatorio:"
            "1. Alcance um desempenho operacional aprimorado com processos baseados em IA. ​"
            "2. Garanta a rápida implantação de novos modelos e soluções de IA. ​"
            "3. Capacite o negócio com uma plataforma personalizável e segura."
            "Descreva os objetivos de valor que o cliente espera alcançar, conforme o briefing. "
            "Responda em até 3 tópicos objetivos, estruturados e claros, em HTML (use <ul><li>)."
        ),
        "Corresponding Solution Components": (
            "Você é um assistente de IA especializado em propostas comerciais.\n"
            f"Baseado no briefing geral: '''{request.briefing}''', crie um texto para a seção 'Corresponding Solution Components'.\n"
            "Esse texto deve ser feito baseado nesse briefing fazendo levantamento dos Componentes da solução correspondentes"
            "Para ajudar entender a estrutura do texto que deve ser criado, aqui um exemplo de 3 topicos criados para apresentar as os Principais Objetivos de valor para o cliente levantadas ou declaradas de um cliente aleatorio:"
            "Infraestrutura de nuvem escalável usando o Azure."
            "Compatibilidade com vários modelos, incluindo o Azure OpenAI e outros modelos."
            "Plataforma de baixo código para personalização e testes rápidos de casos de uso de IA."
            "Sugira componentes de solução que atendam ao briefing do cliente. "
            "Responda em até 3 tópicos objetivos, estruturados e claros, em HTML (use <ul><li>)."
        )
    }

    briefing = request.briefing
    results = {}

    for section in sections:
        prompt = (
            f"{section_prompts[section]}\n\nBriefing do cliente:\n'''{briefing}'''\n"
            #f"Você é um assistente de IA especializado em propostas comerciais.\n"
            #f"Baseado no briefing geral: '''{briefing}''', crie um texto para a seção '{section}'.\n"
            #f"Esse texto deve ser claro, objetivo e estruturado. Que sejam 3 bullets contendo principais informações relevantes.\n. NO retorno faça cada bullet aparecer em uma linha separada no html do frontend"
        )

        response = openai.ChatCompletion.create(
            engine="gpt-4o",  # use seu modelo ou deployment correto
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=300,
            top_p=1.0
        )

        raw_text = response.choices[0].message["content"].strip()
        cleaned_text = clean_code_blocks(raw_text)
        results[section] = cleaned_text
        results[f"{section}_prompt"] = prompt
    return results

@app.post("/generate-section")
async def generate_section(request: PromptRequest):
    section_prompts = {
        "Client Stated Needs": (
            "Você é um assistente de IA especializado em propostas comerciais.\n"
            f"Baseado no briefing geral: '''{request.content}''', crie um texto para a seção '{request.section}'.\n"
            "Liste claramente as necessidades declaradas pelo cliente com base no briefing abaixo. "
            "Responda em até 3 tópicos objetivos, estruturados e claros, em HTML (use <ul><li>)."
        ),
        "Corresponding Strategic Objectives": (
            "Você é um assistente de IA especializado em propostas comerciais.\n"
            f"Baseado no briefing geral: '''{request.content}''', crie um texto para a seção '{request.section}'.\n"
            "Com base no briefing, identifique os objetivos estratégicos correspondentes do cliente. "
            "Responda em até 3 tópicos objetivos, estruturados e claros, em HTML (use <ul><li>)."
        ),
        "Key Issues and Problems": (
            "Você é um assistente de IA especializado em propostas comerciais.\n"
            f"Baseado no briefing geral: '''{request.content}''', crie um texto para a seção '{request.section}'.\n"
            "Aponte os principais problemas e desafios enfrentados pelo cliente, conforme o briefing. "
            "Responda em até 3 tópicos objetivos, estruturados e claros, em HTML (use <ul><li>)."
        ),
        "Opportunities": (
            "Você é um assistente de IA especializado em propostas comerciais.\n"
            f"Baseado no briefing geral: '''{request.content}''', crie um texto para a seção '{request.section}'.\n"
            "Identifique oportunidades relevantes para o cliente a partir do briefing. "
            "Responda em até 3 tópicos objetivos, estruturados e claros, em HTML (use <ul><li>)."
        ),
        "Client Value Objectives": (
            "Você é um assistente de IA especializado em propostas comerciais.\n"
            f"Baseado no briefing geral: '''{request.content}''', crie um texto para a seção '{request.section}'.\n"
            "Descreva os objetivos de valor que o cliente espera alcançar, conforme o briefing. "
            "Responda em até 3 tópicos objetivos, estruturados e claros, em HTML (use <ul><li>)."
        ),
        "Corresponding Solution Components": (
            "Você é um assistente de IA especializado em propostas comerciais.\n"
            f"Baseado no briefing geral: '''{request.content}''', crie um texto para a seção '{request.section}'.\n"
            "Sugira componentes de solução que atendam ao briefing do cliente. "
            "Responda em até 3 tópicos objetivos, estruturados e claros, em HTML (use <ul><li>)."
        ),
    }

    prompt = (
        f"{section_prompts[request.section]}\n\nBriefing do cliente:\n'''{request.content}'''\n"
    #    f"Você é um assistente de IA especializado em propostas comerciais.\n"
    #    f"Baseado no briefing geral: '''{request.content}''', crie um texto para a seção '{request.section}'.\n"
    #    f"Esse texto deve ser claro, objetivo e estruturado. Que sejam 3 bullets contendo principais informações relevantes.\n. NO retorno faça cada bullet aparecer em uma linha separada no html do frontend"
    )

    response = openai.ChatCompletion.create(
        engine="gpt-4o",  # use seu modelo ou deployment correto
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=300,
        top_p=1.0
    )

    raw_text = response.choices[0].message["content"].strip()
    refined_text = clean_code_blocks(raw_text)
    return {
        "refined_text": refined_text,
        "prompt": prompt
    }

def clean_code_blocks(text):
    # Remove blocos markdown ```html ... ``` ou ``` ... ```
    text = re.sub(r"^```html\s*", "", text.strip(), flags=re.IGNORECASE | re.MULTILINE)
    text = re.sub(r"^```|```$", "", text.strip(), flags=re.MULTILINE)
    return text.strip()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
