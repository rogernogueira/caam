from pathlib import Path
from typing import Literal
from pydantic import BaseModel
from ollama import chat
import pymupdf

path = "dados/auxilio.pdf"
doc = pymupdf.open(path)
doc[0].get_pixmap(dpi=200).save("dados/auxilio.png")

path_img = Path('dados/auxilio.png')


# Verify the file exists
if not path_img.exists():
  raise FileNotFoundError(f'Image not found at: {path}')

# Set up chat as usual
response = chat(
  model='qwen2.5vl',
  messages=[
    {
      'role': 'user',
      'content': '''Analise a imagem e extraia os seguintes dados:{'Nome':'none da pessoa', 
            'Matricula':'matricula da pessoa',  
            'Cargo':'cargo da pessoa'}. 
            }  ''',
      'images': [path_img],
    },
  ],
  options={'temperature': 0},  # Set temperature to 0 for more deterministic output
)
# Convert received content to the schema
print(response.message.content)