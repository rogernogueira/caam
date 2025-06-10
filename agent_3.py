from textwrap import dedent
from agno.agent import Agent, RunResponse
from agno.models.ollama import Ollama
from dotenv import load_dotenv
import pandas as pd
import pymupdf
import os
from agno.media import Image
from pathlib import Path
from pydantic import BaseModel, Field
from text_util import apply_ocr

dir_name = 'dados' # local onde estão os documentos
model_name = 'qwen2.5vl:3b' # modelo que será usado para extrair os dados

data_dir = Path(dir_name)
class DocumentData(BaseModel):
    Nome: str = Field(...,  description="Nome da pessoa extraído do documento.")
    Matricula: str = Field(..., description="Matrícula da pessoa extraída do documento.")
    Cargo: str = Field(..., description="Cargo da pessoa extraído do documento.")

agent = Agent(
        model=Ollama(id=model_name, options={'temperature': 0, 'nun_ctx':'4096' }),
        instructions=dedent('''Extraia os seguinte dados do documento.
            {'Nome':'none da pessoa', u
            'Matricula':'matricula da pessoa',  
            'Cargo':'cargo da pessoa'}. 
            } 
            '''),     
    response_model = DocumentData,  
    name="AnalistaRH",
    description="Analista de Recursos Humanos que extrai dados de documentos.",
    )
data_extract_docs = []
for file in os.listdir(data_dir):
    if not file.endswith('.pdf'):
        continue
    file= Path.joinpath(data_dir, file)
    if  file.exists():
        doc = pymupdf.open(file)
        texto = ""
        for page in doc:
            texto = texto + ' ' + page.get_text("text").encode('utf-8').decode('utf-8')
        text = texto.strip()
        # se o texto for muito curto, não faz sentido continuar, vamos tentar OCR
        imgs = []
        couse = apply_ocr(text)
        if len(couse) > 0:
            print(f"Aplicando OCR ao documento...{file.name}")
            print(f"Motivos: {', '.join(couse)}")
            for i, page in enumerate(doc):
                # converte a página em imagem
                file_img = str(file.absolute()).replace('.pdf', f'_{i}.png')
                page.get_pixmap(dpi=300).save(file_img)
                imgs.append(Image(filepath=Path(file_img), name=f'Pagina {i}', description='Documento OCR'))
            response = agent.run(images=imgs)
            ocr = True
            # deleta  as imagens criadas
            for img in imgs:
                if img.filepath.exists():
                    os.remove(img.filepath)               
        else:
            try:
                ocr = False
                print(f"Coletando dados do texto do documento...{file.name}")
                response = agent.run(text)
            except Exception as e:
                print(f"Erro ao processar o texto: {e}")
                response = RunResponse(content=DocumentData(Nome='Erro', Matricula='Erro', Cargo='Erro'))
        data_doc = response.content.model_dump()
        data_doc['file_name'] = file.name
        data_doc['time'] = response.metrics['time']
        data_doc['ocr'] =  ocr  
        data_doc['agent_id'] = response.agent_id 
        data_extract_docs.append(data_doc)

df  = pd.DataFrame(data_extract_docs)
df.to_excel(f'dados_extraido_qwen2.5vl-3b.xlsx', index=False)


            
        
        
        


    

