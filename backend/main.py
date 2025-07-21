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
   # allow_origins= ["*"],  # coloque exatamente a origem que está acessando o backend
    allow_origins=["http://127.0.0.1:5500"],  # Adicione a origem do frontend
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
            "Para ajudar entender a estrutura do texto que deve xer criado, aqui um exemplo de 3 topicos criados para apresentar as problemas e questões declaradas por um cliente aleatorio:"
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
            "Para ajudar entender a estrutura do texto que deve xer criado, aqui um exemplo de 3 topicos criados para apresentar as problemas e questões declaradas por um cliente aleatorio:"
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
        "Escopo do Trabalho": (
            "Você é um assistente de IA especializado em propostas comerciais.\n"
            f"Baseado no briefing geral: '''{request.content}''', crie um texto para a seção 'Escopo do Trabalho'.\n"
            "Exemplo:\n"
            "Este projeto inclui a implementação de um acelerador GenAI para apoiar o desenvolvimento de casos de uso priorizados em duas áreas de negócios. "
            "O escopo também envolve a formação de uma equipe dedicada, a realização de sessões de Alfabetização em IA e o estabelecimento de uma estrutura de governança (CoE GenAI).\n"
            "Responda em HTML (use <p>)."
        ),
        "Principais Resultados": (
            "Você é um assistente de IA especializado em propostas comerciais.\n"
            f"Baseado no briefing geral: '''{request.content}''', crie um texto para a seção 'Principais Resultados'.\n"
            "Exemplo:\n"
            "As entregas incluem protótipos funcionais (PoCs/MVPs), um backlog reutilizável de casos de uso, materiais de capacitação de IA e um modelo de governança de base para garantir a adoção responsável e escalável do GenAI dentro da organização.\n"
            "Responda em HTML (use <p>)."
        ),
        "Fora do Escopo": (
            "Você é um assistente de IA especializado em propostas comerciais.\n"
            f"Baseado no briefing geral: '''{request.content}''', crie um texto para a seção 'Fora do Escopo'.\n"
            "Exemplo:\n"
            "Atividades relacionadas à implantação de produção em larga escala, integração em toda a empresa, engenharia avançada de dados e treinamento de modelos personalizados não estão incluídas nesta fase.\n"
            "Responda em HTML (use <p>)."
        ),
         "Abordagem de Entrega": (
            "Você é um assistente de IA especializado em propostas comerciais.\n"
            f"Baseado no briefing geral: '''{request.content}''', crie um texto para a seção 'Abordagem de Entrega'.\n"
            "Exemplo:\n"
            "A entrega seguirá um modelo ágil, baseado em sprints, centrado na cocriação e no feedback contínuo. "
            "Cada iteração entregará ativos funcionais alinhados aos casos de uso priorizados, permitindo validação rápida e engajamento do negócio.\n"
            "Responda em HTML (use <p>)."
        ),
        "Estratégia de Sourcing": (
            "Você é um assistente de IA especializado em propostas comerciais.\n"
            f"Baseado no briefing geral: '''{request.content}''', crie um texto para a seção 'Estratégia de Sourcing'.\n"
            "Exemplo:\n"
            "Os recursos serão obtidos do pool de talentos especializados em GenAI da Avanade, garantindo acesso a engenheiros de IA, arquitetos de soluções e analistas de negócios. "
            "Uma combinação flexível de profissionais locais e locais será usada para equilibrar custo, expertise e colaboração.\n"
            "Responda em HTML (use <p>)."
        ),
        "Mobilização": (
            "Você é um assistente de IA especializado em propostas comerciais.\n"
            f"Baseado no briefing geral: '''{request.content}''', crie um texto para a seção 'Mobilização'.\n"
            "Exemplo:\n"
            "O projeto utilizará a infraestrutura e as ferramentas existentes do cliente, garantindo tempo mínimo de configuração. "
            "Dado o modelo de execução baseado em capacidade, os membros da equipe serão alocados dinamicamente para atender às demandas do projeto. "
            "A mobilização será estruturada para garantir integração eficiente, colaboração contínua e adaptabilidade às necessidades em evolução.\n"
            "Responda em HTML (use <p>)."
        ),
        "Work Products & Deliverables": (
            "Você é um assistente de IA especializado em propostas comerciais.\n"
            f"Baseado no briefing geral: '''{request.content}''', crie uma tabela para a seção 'Work Products & Deliverables'.\n"
            "Gere uma tabela HTML com as seguintes colunas:\n"
            "- Título\n"
            "- Descrição\n"
            "- Formato\n"
            "- Critérios de Aceitação\n"
            "- Tipo\n\n"
            "Certifique-se de que a tabela tenha exatamente 5 linhas, cada uma representando um tipo: Funcional, Técnico, Capacitação, Gerencial e Estratégico.\n"
            "Certifique-se de que cada linha da tabela tenha conteúdo único e relevante em todas as colunas: Título, Descrição, Formato, Critérios de Aceitação e Tipo.\n"
            "Não inclua conteúdo concatenado ou mal formatado em uma única célula.\n"
            "Cada linha deve conter conteúdo único e relevante, baseado no briefing geral fornecido. Não inclua linhas genéricas ou exemplos padrão.\n"
            "Use o seguinte exemplo como referência:\n\n"
            "| Título                          | Descrição                                                                 | Formato                | Critérios de Aceitação                                                | Tipo         |\n"
            "|---------------------------------|---------------------------------------------------------------------------|------------------------|------------------------------------------------------------------------|--------------|\n"
            "| Protótipos de Casos de Uso GenAI| PoCs/MVPs funcionais alinhados aos problemas de negócios priorizados.     | Demos Interativos      | Validados pelos usuários de negócios e atendem aos critérios de sucesso definidos. | Funcional    |\n"
            "| Onboarding do Acelerador GenAI  | Implantação e configuração inicial dos aceleradores GenAI da Avanade.     | Configuração & Scripts | Implantados com sucesso e prontos para uso pela equipe.               | Técnico      |\n"
            "| Pacote de Capacitação em IA     | Sessões de treinamento, materiais e ativos para engajamento da equipe interna. | Apresentações & Kits  | Entregues ao público-alvo e confirmada a participação/feedback.       | Capacitação  |\n"
            "| Playbook CoE GenAI              | Guia de governança com templates, papéis, melhores práticas e KPIs.       | Documentação           | Revisado e aceito pelos stakeholders de governança de IA.             | Gerencial    |\n"
            "| Backlog & Framework de Priorização | Backlog de casos de uso GenAI curado e categorizado para 2 áreas de negócios. | Lista Priorizada      | Aprovado conjuntamente pelo product owner e pela equipe de entrega.   | Estratégico  |\n\n"
            "A tabela gerada deve estar formatada em HTML usando <table>, <thead>, <tbody>, <tr>, <th> e <td>. Não inclua explicações fora da tabela."
        ),
        "Processo de Aceitação de Entregas": (
            "Você é um assistente de IA especializado em propostas comerciais.\n"
            f"Baseado no briefing geral: '''{request.content}''', crie um texto para a seção 'Processo de Aceitação de Entregas'.\n"
            "Descreva o processo de aceitação de entregas, incluindo critérios de validação, etapas de aprovação e responsabilidades das partes envolvidas.\n"
            "Exemplo:\n"
            "Todas as entregas seguirão um processo de aceitação estruturado, definido em conjunto pela Avanade e pela ConectCar. Isso inclui:\n"
            "- Validação de protótipos funcionais (PoCs/MVPs) pelas partes interessadas do negócio.\n"
            "- Aprovação de materiais de treinamento e governança pelas equipes designadas.\n"
            "- Alinhamento com o backlog definido.\n"
            "Cada entrega será revisada quanto à aderência ao escopo, funcionalidade técnica (quando aplicável) e resultados de negócio esperados. A aprovação formal será documentada por meio de relatórios resumidos ou formulários de aprovação.\n"
            "Responda em HTML (use <p>)."
        ),
        "Principais Dependências/Obrigações Externas": (
            "Você é um assistente de IA especializado em propostas comerciais.\n"
            f"Baseado no briefing geral: '''{request.content}''', crie uma tabela para a seção 'Principais Dependências/Obrigações Externas'.\n"
            "Gere uma tabela HTML com as seguintes colunas:\n"
            "- Dependência\n"
            "- Impacto\n"
            "- Quando\n"
            "- Obrigação com\n"
            "- Comentários\n\n"
            "Certifique-se de que a tabela tenha exatamente 6 linhas, cada uma representando uma dependência única e relevante.\n"
            "Cada linha deve conter conteúdo único e relevante em todas as colunas: Dependência, Impacto, Quando, Obrigação com e Comentários.\n"
            "Não inclua conteúdo genérico ou mal formatado em uma única célula.\n"
            "Use o seguinte exemplo como referência:\n\n"
            "| Dependência                        | Impacto                                      | Quando       | Obrigação com         | Comentários                                    |\n"
            "|------------------------------------|---------------------------------------------|--------------|-----------------------|-----------------------------------------------|\n"
            "| Acesso a Dados e APIs do Cliente   | Atrasos na integração e contextualização do modelo de IA. | Início do Projeto | Equipe de TI do Cliente | Requer provisionamento e testes antecipados. |\n"
            "| Agendamento de Stakeholders        | Atrasos na validação de PoC e feedback dos usuários. | Sprint 1     | Líderes de Negócio    | Necessário para demonstrações e revisão de critérios de sucesso. |\n"
            "| Identificação de Participantes de Alfabetização em IA | Adiamento de sessões de treinamento. | Semana 1     | Equipe de RH/Treinamento | Necessário alinhamento de calendário e número mínimo de participantes. |\n"
            "| Nomeação de Product Owner para Casos de Uso | Atrasos na tomada de decisão e grooming do backlog. | Início do Projeto | PMO do Cliente         | Habilita planejamento e priorização eficazes. |\n"
            "| Participantes de Revisão de Governança | Atrasos na validação do framework de CoE. | Meio do Projeto | Líder de Conformidade | Necessário para playbook de governança e política. |\n"
            "| Provisionamento de Ambiente (Sandbox/Dev) | Atrasos na implantação de componentes técnicos de PoC. | Sprint 1     | Infraestrutura do Cliente | Deve atender aos requisitos mínimos de recursos Azure. |\n\n"
            "A tabela gerada deve estar formatada em HTML usando <table>, <thead>, <tbody>, <tr>, <th> e <td>. Não inclua explicações fora da tabela."
        ),
        "Riscos Chaves": (
            "Você é um assistente de IA especializado em propostas comerciais.\n"
            f"Baseado no briefing geral: '''{request.content}''', crie uma tabela para a seção 'Riscos Chaves'.\n"
            "Gere uma tabela HTML com as seguintes colunas:\n"
            "- #\n"
            "- Risk\n"
            "- Consequence\n"
            "- Mitigation Action(s) & Date\n"
            "- Impact\n"
            "- Probability\n"
            "- Owner\n"
            "- Comments\n\n"
            "Certifique-se de que a tabela tenha exatamente 5 linhas, cada uma representando um risco único e relevante.\n"
            "Cada linha deve conter conteúdo único e relevante em todas as colunas: Risk, Consequence, Mitigation Action(s) & Date, Impact, Probability, Owner e Comments.\n"
            "Não inclua conteúdo genérico ou mal formatado em uma única célula.\n"
            "Use o seguinte exemplo como referência:\n\n"
            "| # | Risk                                | Consequence                     | Mitigation Action(s) & Date       | Impact | Probability | Owner                 | Comments                                   |\n"
            "|---|-------------------------------------|----------------------------------|------------------------------------|--------|-------------|-----------------------|-------------------------------------------|\n"
            "| 1 | Delay in receiving business data & APIs | Slower integration and testing | Early engagement with client IT team | H      | M           | Delivery Manager      | API access must be prioritized for smooth progress |\n"
            "| 2 | Low availability of business stakeholders | Delayed feedback and slower backlog refinement | Align calendars during project kickoff | M      | H           | Client Sponsor        | Business team allocation must be secured early |\n"
            "| 3 | Misalignment on AI use case expectations | Rework and scope changes       | Joint backlog review sessions before development | H      | M           | Product Owner         | Clarity on success metrics is key for each use case |\n"
            "| 4 | Lack of engagement in AI Literacy sessions | Low adoption and resistance to change | Incentivize participation and link to strategic goals | M      | M           | HR / Enablement Lead | Internal communication campaign may be required |\n"
            "| 5 | Delays in provisioning dev/test environments | Blocked implementation of PoCs | Request provisioning in Sprint 0 | H      | M           | Client IT Infrastructure | Ensure environments meet min. Azure GenAI requirements |\n\n"
            "A tabela gerada deve estar formatada em HTML usando <table>, <thead>, <tbody>, <tr>, <th> e <td>. Não inclua explicações fora da tabela."
        ),
        "Key Assumptions": (
            "Você é um assistente de IA especializado em propostas comerciais.\n"
            f"Baseado no briefing geral: '''{request.content}''', crie uma tabela para a seção 'Key Assumptions'.\n"
            "Gere uma tabela HTML com as seguintes colunas:\n"
            "- Assumption\n"
            "- Verification\n"
            "- Impact\n"
            "- Owner\n"
            "- Comments\n\n"
            "Certifique-se de que a tabela tenha exatamente 8 linhas, cada uma representando uma suposição única e relevante.\n"
            "Cada linha deve conter conteúdo único e relevante em todas as colunas: Assumption, Verification, Impact, Owner e Comments.\n"
            "Não inclua conteúdo genérico ou mal formatado em uma única célula. GERE todo CONTEúDO em português e traduza as colunas tbm para português\n"
            "Use o seguinte exemplo como referência:\n\n"
            "| Assumption                          | Verification                          | Impact | Owner                 | Comments                                   |\n"
            "|-------------------------------------|---------------------------------------|--------|-----------------------|-------------------------------------------|\n"
            "| Client will provide business rules documentation continuously. | Confirm during backlog refinement sessions. | High   | Client                | Business rules may evolve, impacting backlog. |\n"
            "| Key business stakeholders will be available for review cycles. | Confirm stakeholder attendance in sprint demos. | High   | Client PMO            | Engagement is critical to validate use cases and priorities. |\n"
            "| Client will designate Product Owner(s) for use case alignment. | Validate during project kickoff. | High   | Client                | Lack of ownership may delay decisions. |\n"
            "| Azure subscription and environments will be provisioned in advance. | Validate before Sprint 1 start. | Medium | Client IT             | Required for GenAI accelerator deployment. |\n"
            "| GenAI use cases will not require external model training. | Confirm during use case qualification. | Medium | Avanade & Client      | Project focuses on prompt-based and accelerator-based use. |\n"
            "| Data shared will not contain sensitive PII unless explicitly agreed. | Review during data onboarding. | High   | Client Security Team  | Ensures compliance with data privacy standards. |\n"
            "| Training participants will be pre-selected and available as planned. | Check participant list before each session. | Medium | Client Enablement Lead | AI Literacy depends on consistent participation. |\n"
            "| Governance team will review and validate CoE artifacts. | Approval checkpoints during CoE track. | Medium | Client Governance Lead | Needed to establish AI operating model and sustainment. |\n\n"
            "A tabela gerada deve estar formatada em HTML usando <table>, <thead>, <tbody>, <tr>, <th> e <td>. Não inclua explicações fora da tabela."
        ),
        "Funções e Responsabilidades - Solution RACI": (
            "Você é um assistente de IA especializado em propostas comerciais.\n"
            f"Baseado no briefing geral: '''{request.content}''', crie uma tabela para a seção 'Funções e Responsabilidades - Solution RACI'.\n"
            "Gere uma tabela HTML com as seguintes colunas:\n"
            "- Atividade/Tarefa\n"
            "- Cliente\n"
            "- Avanade Onshore\n\n"
            "Certifique-se de que a tabela tenha exatamente 10 linhas, cada uma representando uma atividade ou tarefa única e relevante.\n"
            "Cada linha deve conter conteúdo único e relevante em todas as colunas: Atividade/Tarefa, Cliente e Avanade Onshore.\n"
            "Use os seguintes valores para Cliente e Avanade Onshore:\n"
            "- R: Responsável\n"
            "- A: Aprovador\n"
            "- C: Consultado\n"
            "- I: Informado\n\n"
            "Use o seguinte exemplo como referência:\n\n"
            "| Atividade/Tarefa                     | Cliente | Avanade Onshore |\n"
            "|--------------------------------------|---------|-----------------|\n"
            "| Alinhamento Estratégico e Kickoff    | A       | R               |\n"
            "| Sessões de Alfabetização em IA       | R       | A               |\n"
            "| Brainstorming e Priorização de Casos | R       | A               |\n"
            "| Definição de Casos Piloto            | C       | R               |\n"
            "| Configuração da Plataforma GenAI     | I       | R               |\n"
            "| Workshop Prático para Estruturação   | R       | A               |\n"
            "| Desenvolvimento de MVP/Piloto        | I       | R               |\n"
            "| Validação de Casos e Feedback        | A       | R               |\n"
            "| Configuração de Governança e CoE     | C       | R               |\n"
            "| Transferência de Conhecimento        | I       | R               |\n\n"
            "A tabela gerada deve estar formatada em HTML usando <table>, <thead>, <tbody>, <tr>, <th> e <td>. Não inclua explicações fora da tabela."
        )
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
    # Valida e preenche lacunas apenas para a seção "Work Products & Deliverables"
    if request.section == "Work Products & Deliverables":
        refined_text = validate_table_output(raw_text, request)
    else:
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

def validate_table_output(html_table: str, request: PromptRequest) -> str:
    # Tipos esperados na tabela
    required_types = ["Funcional", "Técnico", "Capacitação", "Gerencial", "Estratégico"]
    missing_types = [tipo for tipo in required_types if tipo not in html_table]

    # Divide a tabela em linhas e verifica cada linha
    rows = html_table.split("\n")
    corrected_rows = []

    for row in rows:
        columns = row.split("|")
        if len(columns) == 6:
            # Verifica se todas as colunas estão preenchidas
            corrected_row = "|".join([col.strip() for col in columns])
            corrected_rows.append(corrected_row)
        elif len(columns) > 6:
            # Corrige linhas com excesso de conteúdo concatenado
            corrected_row = "|".join([col.strip() for col in columns[:6]])
            corrected_rows.append(corrected_row)
        else:
            # Reexecuta o prompt para corrigir linhas incompletas
            corrected_row = "|".join(columns + [""] * (6 - len(columns)))  # Preenche colunas vazias
            corrected_rows.append(corrected_row)

    # Reexecuta o prompt se houver tipos faltantes ou linhas incompletas
    if missing_types or len(corrected_rows) < 5:
        prompt = (
            f"Você é um assistente de IA especializado em propostas comerciais.\n"
            f"Baseado no briefing geral: '''{request.content}''', crie linhas adicionais para corrigir os seguintes problemas:\n"
            f"- Tipos faltantes: {', '.join(missing_types)}.\n"
            f"- Total de linhas insuficiente: {5 - len(corrected_rows)} linhas adicionais necessárias.\n"
            "Cada linha deve conter conteúdo único e relevante, baseado no briefing fornecido.\n"
            "Use o seguinte formato:\n\n"
            "| Título                          | Descrição                                                                 | Formato                | Critérios de Aceitação                                                | Tipo         |\n"
            "|---------------------------------|---------------------------------------------------------------------------|------------------------|------------------------------------------------------------------------|--------------|\n"
        )
        response = openai.ChatCompletion.create(
            engine="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300,
            top_p=1.0
        )
        additional_rows = response.choices[0].message["content"].strip()
        corrected_rows += additional_rows.split("\n")

    # Reconstrói a tabela corrigida
    html_table = "\n".join(corrected_rows)
    return html_table

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
