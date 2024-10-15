# horusec start -p ./project/Examples -D -o=json -O=./output.json 
# horusec start -p ./project/{nome_do_projeto} -D -o=json -O=.reports/{nome_do_projeto}/{nome_do_projeto}_horusec.json 
import os
import subprocess

# Caminho para a pasta de projetos
project_path = './project'
# Caminho para a pasta de relatórios
report_path = './reports'

# Verifica se a pasta de relatórios existe, se não, cria
if not os.path.exists(report_path):
    os.makedirs(report_path)

# Lista todos os projetos na pasta de projetos
projects = [d for d in os.listdir(project_path) if os.path.isdir(os.path.join(project_path, d))]

# Executa o comando horusec para cada projeto
for project in projects:
    project_dir = os.path.join(project_path, project)
    report_dir = os.path.join(report_path, project)
    
    # Verifica se a pasta de relatório do projeto existe, se não, cria
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    
    output_file = os.path.join(report_dir, f"{project}_horusec.json")
    command = f"horusec start -p {project_dir} -D -o=json -O={output_file}"
    
    # Executa o comando
    subprocess.run(command, shell=True, check=True)
