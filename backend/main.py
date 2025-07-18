from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
from pydantic import BaseModel
import re
from dotenv import load_dotenv
from fastapi import Request, Body

load_dotenv()
app = FastAPI()
 
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"],  # coloque exatamente a origem que está acessando o backend
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
            f"Baseado no briefing geral: '''{request.content}''', crie um texto para a seção '{request.section}'.\n"
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
            f"Baseado no briefing geral: '''{request.content}''', crie um texto para a seção '{request.section}'.\n"
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
            f"Baseado no briefing geral: '''{request.content}''', crie um texto para a seção '{request.section}'.\n"
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
            f"Baseado no briefing geral: '''{request.content}''', crie um texto para a seção '{request.section}'.\n"
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
            f"Baseado no briefing geral: '''{request.content}''', crie um texto para a seção '{request.section}'.\n"
            "Esse texto deve ser feito baseado nesse briefing fazendo levantamento dos Componentes da solução correspondentes"
            "Para ajudar entender a estrutura do texto que deve ser criado, aqui um exemplo de 3 topicos criados para apresentar as os Principais Objetivos de valor para o cliente levantadas ou declaradas de um cliente aleatorio:"
            "Infraestrutura de nuvem escalável usando o Azure."
            "Compatibilidade com vários modelos, incluindo o Azure OpenAI e outros modelos."
            "Plataforma de baixo código para personalização e testes rápidos de casos de uso de IA."
            "Sugira componentes de solução que atendam ao briefing do cliente. "
            "Responda em até 3 tópicos objetivos, estruturados e claros, em HTML (use <ul><li>)."
        ),
        "Solution-to-Win (cost optimization)": (
            "Você é um assistente de IA especializado em propostas comerciais.\n"
            f"Baseado no briefing geral: '''{request.content}''', crie um texto para a seção 'Solution-to-Win (cost optimization)'.\n"
            "Liste 3 bullets objetivos e claros sobre otimização de custos, focando em uso de serviços Azure, arquitetura modular e aceleradores de IA para redução de tempo e esforço. Responda em HTML (use <ul><li>)."
        ),
        "Price-to-Win": (
            "Você é um assistente de IA especializado em propostas comerciais.\n"
            f"Baseado no briefing geral: '''{request.content}''', crie um texto para a seção 'Price-to-Win'.\n"
            "Liste 3 bullets objetivos e claros sobre estratégias de preço para vencer, como modelo Time & Materials, escopo focado e modelo pay-per-service. Responda em HTML (use <ul><li>)."
        ),
        "Core Areas of Responsibility": (
            "Você é um assistente de IA especializado em propostas comerciais.\n"
            f"Baseado no briefing geral: '''{request.content}''', crie uma tabela para a seção 'Core Areas of Responsibility', gere uma tabela HTML com o máximo de conteúdo possível, de preferencia com minimo de 10 linhas geradas na tabela, com conteudo estruturado e alinhado, com as seguintes colunas:\n"
            "- Track / Workstream\n"
            "- Accountability (com subcolunas: Client e Avanade, marcadas com 'X' quando aplicável)\n"
            "- Key notes (scope, dependencies, work plan, AVA/Client third parties)\n\n"
            "Use o seguinte exemplo como referência de estrutura, tipo de conteudo gerado e estilo da tabela:\n\n"
            "| Track / Workstream                        | Client | Avanade | Key notes (scope, dependencies, work plan, AVA/Client third parties) |\n"
            "|-------------------------------------------|--------|---------|------------------------------------------------------------------------|\n"
            "| Project Kickoff & Alignment               |   X    |    X    | Define project goals, objectives, expectations, and working model.     |\n"
            "| Use Case Prioritization                   |   X    |         | Co-create and approve the initial backlog of GenAI opportunities aligned to business priorities. |\n"
            "| AI Literacy Enablement                    |        |    X    | Client provides audience and engagement; Avanade delivers workshops and hands-on sessions. |\n"
            "| GenAI Squad Setup                         |        |    X    | Define team composition, roles, and onboarding for case development execution. |\n"
            "| Accelerator Deployment                    |        |    X    | Configure and deploy Avanade’s GenAI accelerator in the client’s environment or as a managed service. |\n"
            "| Security & Compliance Review              |   X    |    X    | Ensure GenAI usage complies with client’s internal governance, data privacy, and legal requirements. |\n"
            "| Use Case Implementation (PoC/MVP)         |        |    X    | Deliver prioritized use cases with agile cycles and value demonstration checkpoints. |\n"
            "| Knowledge Transfer & Sustainability Plan  |   X    |    X    | Empower client teams to maintain, scale, and govern AI solutions independently over time. |\n\n"
            "A tabela gerada deve ser nova a cada requisição, limpando layout anterior. Gere uma tabela HTML com o máximo de conteúdo possível, de preferencia com minimo de 10 linhas geradas de conteudo na tabela,\n"
            "A resposta deve estar formatada em HTML usando <table>, <thead>, <tbody>, <tr>, <th> e <td>. Não inclua explicações fora da tabela."
        ),
        "Opportunity Background - Win Themes": (
            "Você é um assistente de IA especializado em propostas comerciais.\n"
            f"Baseado no briefing geral: '''{request.content}''', crie uma tabela para a seção 'Opportunity Background - Win Themes', gere uma tabela HTML com duas colunas:\n"
            "- Theme\n"
            "- Evidence\n\n"
            "Use o seguinte exemplo como referência de estrutura, tipo de conteudo gerado e estilo da tabela:\n\n"
            "| Theme                          | Evidence                                                                 |\n"
            "|--------------------------------|--------------------------------------------------------------------------|\n"
            "| Expertise in Generative AI     | Successfully delivered similar Generative AI projects for major clients. |\n"
            "| Scalable AI Platform           | Proven architecture supporting multi-model AI deployments on Azure.      |\n"
            "| Accelerated Time-to-Value      | Use of pre-built AI accelerators and reusable assets enabled faster deployment of use cases. |\n"
            "| Governance & Responsible AI    | Established frameworks for ethical AI, privacy compliance, and lifecycle monitoring. |\n"
            "| Client Empowerment & Sustainability | AI Literacy programs and CoE models delivered to enable client autonomy and scale. |\n\n"
            "A tabela gerada deve ser nova a cada requisição, limpando layout anterior. gere uma tabela HTML com o máximo de conteúdo possível, de preferencia com minimo de 5 linhas gerados de conteudo na tabela,\n"
            "A resposta deve estar formatada em HTML usando <table>, <thead>, <tbody>, <tr>, <th> e <td>. Não inclua explicações fora da tabela."
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

@app.post("/generate-slide")
async def generate_slide(request: Request):
    data = await request.json()
    slide_html = f"""
    <div style='border:2px solid orange;padding:20px;font-family:sans-serif;background:#fff;'>
        <h3 style='color:#e67e22;'>Alignment to Buyer Value</h3>
        <table style='width:100%;border-collapse:collapse;'>
            <tr>
                <td style='vertical-align:top;width:50%;border:1px solid #e67e22;padding:10px;'>
                    <strong>Client Stated Needs:</strong><br>{data.get('Client Stated Needs', '')}
                    <br><br>
                    <strong>Corresponding Strategic Objectives:</strong><br>{data.get('Corresponding Strategic Objectives', '')}
                </td>
                <td style='vertical-align:top;width:50%;border:1px solid #e67e22;padding:10px;'>
                    <strong>Key Issues and Problems:</strong><br>{data.get('Key Issues and Problems', '')}
                    <br><br>
                    <strong>Opportunities:</strong><br>{data.get('Opportunities', '')}
                </td>
            </tr>
            <tr>
                <td style='vertical-align:top;width:50%;border:1px solid #e67e22;padding:10px;'>
                    <strong>Client value objectives</strong><br>{data.get('Client Value Objectives', '')}
                </td>
                <td style='vertical-align:top;width:50%;border:1px solid #e67e22;padding:10px;'>
                    <strong>Corresponding solution components</strong><br>{data.get('Corresponding Solution Components', '')}
                </td>
            </tr>
        </table>
        <div style='font-size:10px;color:#e67e22;margin-top:10px;'>©2020 Avanade Inc. All Rights Reserved.</div>
    </div>
    """
    return {"slide_html": slide_html}

slides_db = {}

@app.post("/save-slide")
async def save_slide(
    client_name: str = Body(...),
    project_name: str = Body(...),
    slide_html: str = Body(...)
):
    key = f"{client_name}_{project_name}"
    slides_db[key] = slide_html
    return {"status": "saved", "key": key}

@app.get("/get-slides")
async def get_slides(client_name: str, project_name: str):
    key = f"{client_name}_{project_name}"
    slides = []
    if key in slides_db:
        slides.append(slides_db[key])
    return {"slides": slides}

def clean_code_blocks(text):
    # Remove blocos markdown ```html ... ``` ou ``` ... ```
    text = re.sub(r"^```html\s*", "", text.strip(), flags=re.IGNORECASE | re.MULTILINE)
    text = re.sub(r"^```|```$", "", text.strip(), flags=re.MULTILINE)
    return text.strip()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
