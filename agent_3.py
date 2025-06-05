from textwrap import dedent
from agno.agent import Agent, RunResponse
from agno.models.ollama import Ollama
from agno.models.deepseek import DeepSeek
from dotenv import load_dotenv
import pandas as pd
import pymupdf
import json
from agno.media import Image
from agno.tools.shell import ShellTools
from agno.tools.file import FileTools
from pathlib import Path

from pydantic import BaseModel, Field
class DocumentData(BaseModel):
    Nome: str = Field(...,  description="Nome da pessoa extraído do documento.")
    Matricula: str = Field(..., description="Matrícula da pessoa extraída do documento.")
    Cargo: str = Field(..., description="Cargo da pessoa extraído do documento.")
# Import necessary libraries
load_dotenv()

# agente que usa visão computacional para extrair dados de documentos
agent = Agent(
        model=Ollama(id='qwen3'),
        instructions=dedent('''Extraia o texto do documento
            '''),     
    #response_model = DocumentData,  
    tools=[FileTools(base_dir=Path('dados'))],
    name="AnalistaRH",
    description="Vc é um OCR",
    )
# Print the response in the terminal
path_img = Path("dados/Documento.png")
doc1 = Image( filepath = path_img, name='Documento', description='Documento OCR')
response = agent.run('dados/Documento OCR.pdf')
dados = response.content
print('Nome :', dados.Nome)
print('Matricula :', dados.Matricula)
print('Cargo pessoa :', dados.Cargo)
print('json :', json.dumps(dados.model_dump(), indent=2, ensure_ascii=False))
df = pd.DataFrame  ([dados.model_dump()])
df.to_excel('dados\\funcionario.xlsx', index=False)
json.load(response.content)