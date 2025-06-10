from textwrap import dedent
from agno.agent import Agent, RunResponse
from agno.models.ollama import Ollama
from agno.models.deepseek import DeepSeek
from dotenv import load_dotenv
import pandas as pd
import pymupdf
import json
from agno.media import Image
from pathlib import Path
from pydantic import BaseModel, Field
from pathlib import Path

load_dotenv()


class DocumentData(BaseModel):
    Nome: str = Field(...,  description="Nome da pessoa extraído do documento.")
    Matricula: str = Field(..., description="Matrícula da pessoa extraída do documento.")
    Cargo: str = Field(..., description="Cargo da pessoa extraído do documento.")
# Import necessary libraries


# agente que usa visão computacional para extrair dados de documentos
agent = Agent(
        model=Ollama(id='qwen2.5vl:3b'),
        instructions=dedent('''Extraia os seguinte dados do documento.
            {'Nome':'none da pessoa', 
            'Matricula':'matricula da pessoa',  
            'Cargo':'cargo da pessoa'}. 
            } 
            '''),     
    response_model = DocumentData,  
    name="AnalistaRH",
    description="Analista de Recursos Humanos que extrai dados de documentos.",
    )
# Print the response in the terminal
doc = pymupdf.open("dados\\auxilio_n_pesq.pdf")
doc[0].get_pixmap(dpi=300).save("dados/Documento.png")

path_img = Path("dados/Documento.png")

doc_img = Image( filepath = path_img, name='Documento', description='Documento OCR')

response = agent.run(images=[doc_img])
dados = response.content
print('Nome :', dados.Nome)
print('Matricula :', dados.Matricula)
print('Cargo pessoa :', dados.Cargo)
print('json :', json.dumps(dados.model_dump(), indent=2, ensure_ascii=False))
json_data = dados.model_dump()
json_data['time'] = response.metrics['time'][0]
df = pd.DataFrame  ([json_data])
df.to_excel('dados\\funcionario.xlsx', index=False)
