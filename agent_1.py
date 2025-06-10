from textwrap import dedent
from agno.agent import Agent, RunResponse
from agno.models.deepseek import DeepSeek
from dotenv import load_dotenv
import pandas as pd
import pymupdf
import json
from pydantic import BaseModel, Field

load_dotenv()


class DocumentData(BaseModel):
    Nome: str = Field(...,  description="Nome da pessoa extraído do documento.")
    Matricula: str = Field(..., description="Matrícula da pessoa extraída do documento.")
    Cargo: str = Field(..., description="Cargo da pessoa extraído do documento.")

# Import necessary libraries
agent = Agent(
        model=DeepSeek(),
        instructions=dedent('''Extraia os seguinte dados do documento. devolva json com os dados extraídos.
            Exemplo de resposta:
            {'Nome':'none da pessoa', 
            'Matricula':'matricula da pessoa',  
            'Cargo':'cargo da pessoa'}. 
            } 
            '''), 
    use_json_mode=True, 
    response_model = DocumentData,  
    name="AnalistaRH",
    description="Analista de Recursos Humanos que extrai dados de documentos.",
    )
# Print the response in the terminal

doc = pymupdf.open("dados\\auxilio_pesq.pdf")

texto = ""

for page in doc:
     texto =texto +' ' + page.get_text("text").encode('utf-8').decode('utf-8')
acentamento = texto.strip()
response = agent.run(acentamento)
dados = response.content
print('nome pessoa :', dados.Nome)
print('Matricula pessoa :', dados.Matricula)
print('Cargo pessoa :', dados.Cargo)
print('json:', json.dumps(dados.model_dump(), indent=2, ensure_ascii=False))
json_data = dados.model_dump()
json_data['time'] = response.metrics['time'][0]

df = pd.DataFrame  ([json_data])
df.to_excel('dados\\funcionario.xlsx', index=False)