import os
import zipfile
import shutil

# Caminho para a pasta 'jars'
jars_folder = 'jars'
# Nome da pasta de destino
project_folder = 'project'

# Exclui todos os arquivos e subpastas na pasta 'project' se ela existir
if os.path.exists(project_folder):
    shutil.rmtree(project_folder)

# Cria a pasta de destino novamente
os.makedirs(project_folder)

# Itera sobre todos os arquivos na pasta 'jars'
for jar_file in os.listdir(jars_folder):
    if jar_file.endswith('.jar'):
        jar_path = os.path.join(jars_folder, jar_file)
        jar_name = os.path.splitext(jar_file)[0]
        jar_extract_folder = os.path.join(project_folder, jar_name)
        
        # Cria uma pasta para o conteúdo do .jar
        if not os.path.exists(jar_extract_folder):
            os.makedirs(jar_extract_folder)
        
        # Extrai o conteúdo do .jar para a pasta criada
        with zipfile.ZipFile(jar_path, 'r') as jar:
            jar.extractall(jar_extract_folder)

print("Todos os arquivos .jar foram extraídos com sucesso.")
