from textwrap import dedent
from agno.agent import Agent, RunResponse
from agno.models.ollama import Ollama
from agno.tools.googlesearch import GoogleSearchTools
from agno.tools.arxiv import ArxivTools
from agno.tools.python import PythonTools

# servico = 'ISSQN'  # Serviço a ser pesquisado

# agent = Agent(
#         model=Ollama(id='qwen2.5'),
#         instructions=dedent(f'''
#                     Buque na internet os  informaçoes sobre o {servico} do municipio aprensentado no contexto e 
#                             e analise se a união é substituto tributario para {servico}:
#                   '''),     
#               response_model=None,  
#               name="Contador",
#               description="E contador que analiza questões sobre ISSQN.",
#         tools=[GoogleSearchTools()],
#         debug_mode=True,

#               )

# response = agent.print_response("Municipio do Rio do Janeiro", debug=True)

# agent2 = Agent(
#         model=Ollama(id='qwen2.5'),
#         instructions=dedent(f'''
#                    Quero artigos que trabalham com embeddings para o saúde,faça uma lista com resumos dos artigos em português.
#                   '''),     
#               response_model=None,  
#               name="Pesquisador",
#               #description="E contador que analiza questões sobre ISSQN.",
#         tools=[ArxivTools()],
#         debug_mode=True,

#               )

# response = agent2.print_response()
import subprocess                                                                                                                                                               
def run_powershell_command(command):                                                                                                                                            
    result = subprocess.run(['powershell', '-Command', command], capture_output=True, text=True)                                                                                
    if result.returncode == 0:
        return result.stdout.strip()
    else:                                                      
        return f"Erro ao executar: {result.stderr.strip()}"    

model_name = 'qwen3:0.6b'  # modelo que será usado para executar o comando

run_powershell_command(f"ollama run {model_name}")

agent3 = Agent(
        model=Ollama(id=model_name),
              response_model=None,  
              name="Programador",
              #description="E contador que analiza questões sobre ISSQN.",
        #tools=[PythonTools()],
        debug_mode=True,
              )

#response = agent3.print_response("faça um funçao em python  que execute uma chama do powershell que rode o seguinte comando 'ollama run qwen2.5'")
response = agent3.print_response("qual o seu nome?'")