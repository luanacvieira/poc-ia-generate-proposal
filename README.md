<<<<<<< HEAD
<<<<<<< HEAD
# poc-ia-generate-proposal
# Projeto Backend/Frontend
Este projeto contém:
- Backend em Python (`backend/`)
- Frontend em HTML/CSS/JS (`frontend/`)
- Pasta `uploads/` para arquivos enviados
- Arquivo `.env` para variáveis de ambiente --> Necessário alterar e colocar sua chave Open AI
![image](https://github.com/user-attachments/assets/545f3cc9-ea4f-47c8-8825-0b394d69ac94)


# poc-iac-ocr
Este repsoitório tem uma POC onde testamos a leitura de campos de arquivos OCR, com opção de consultar o histórico dos arquivos lidos, salvando o histório das leituras em arquivo json.

# Fluxo na Tela
Usuário faz upload de um PDF de uma fatura.
O texto da fatura aparece em uma área de texto na tela.
Usuário insere o prompt: "Extraia o nome do cliente, data de emissão e valor total."
Usuário clica em "Analisar".
O resultado aparece na tela: "Nome: João Silva, Data: 10/10/2023, Valor: R$ 500,00".

# Aqui está o passo a passo detalhado para testar localmente o histórico de arquivos lidos na sua aplicação IA-POC:
1. Inicie o backend Python
1.1. Abra o terminal no Visual Studio Code na pasta do projeto (IA-POC).
1.2. Execute o backend com o comando (ou use a task "Run Backend (Python)"):
	uvicorn backend.main:app --reload
	Se não tiver o uvicorn instalado, instale com: 
	pip install uvicorn fastapi python-dotenv pytesseract pymupdf pdf2image

2. Inicie o frontend
2.1. No terminal, ainda na pasta do projeto, execute:
	start frontend/index.html
	Ou simplesmente abra o arquivo index.html no seu navegador.

3. Teste o fluxo
3.1. Na interface web:
Faça upload de um PDF.
Aguarde o texto ser extraído.
Clique em "Analisar" se quiser testar a análise.

3.2. Clique no botão "Carregar Histórico" (na seção 6).
O histórico dos arquivos lidos aparecerá em uma tabela.

4. Dicas e observações
O backend deve estar rodando em http://localhost:8000.
O histórico é salvo no arquivo history.json.
Se quiser limpar o histórico, apague o conteúdo desse arquivo (deixe como []).
=======
# poc-ia-generate-proposal
>>>>>>> 8a0b42f8344f42164055d1298a6befdf6aeacc21
=======
# poc-ia-generate-proposal
>>>>>>> 8a0b42f8344f42164055d1298a6befdf6aeacc21
