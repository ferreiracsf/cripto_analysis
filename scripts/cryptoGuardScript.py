import subprocess
import os
import shutil
import re

# Caminho base do repositório
caminho_base = os.path.dirname(os.path.abspath(__file__))

# Versão para ser utilizada
version = '8.0.422-amzn'

# Altera a versão do Java pelo sdkman e executa os JARs
jar_file = "cryptoguard.jar"
input_option = ["-in", "jar", "-s"]
jars_folder = "./jars"
reports_folder = "./reports"

# Verifica se o arquivo JAR principal existe
if not os.path.isfile(jar_file):
    print(f"Erro: O arquivo JAR não existe: {jar_file}")
    exit(1)

# Verifica se a pasta de JARs de entrada existe
if not os.path.isdir(jars_folder):
    print(f"Erro: A pasta de entrada não existe: {jars_folder}")
    exit(1)

# Monta o comando base para alterar a versão do Java
base_command = f"source $HOME/.sdkman/bin/sdkman-init.sh && sdk use java {version} && java -version"

# Percorre todos os arquivos na pasta 'jars'
for nome_arquivo in os.listdir(jars_folder):
    # Verifica se o arquivo tem a extensão .jar
    if nome_arquivo.endswith('.jar'):
        input_jar = os.path.join(jars_folder, nome_arquivo)
        
        # Monta o comando completo para cada arquivo .jar
        command = f"bash -c '{base_command} && java -jar {jar_file} {' '.join(input_option)} {input_jar}'"
        
        # Executa o comando
        try:
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(f"Saída do comando para {nome_arquivo}:")
            print(result.stdout)
            print("Versão do Java:")
            print(result.stderr)
            
            # Extrai o nome do JAR sem a extensão
            nome_jar = os.path.splitext(nome_arquivo)[0]
            
            # Cria a pasta de relatório se não existir
            report_path = os.path.join(reports_folder, nome_jar)
            os.makedirs(report_path, exist_ok=True)
            
            # Procura pelo arquivo gerado na raiz do projeto
            pattern = re.compile(rf"_CryptoGuard-\d+\.\d+\.\d+_{nome_jar}_[\w-]+\.json")
            for file in os.listdir(caminho_base):
                if pattern.match(file):
                    source_file = os.path.join(caminho_base, file)
                    destination_file = os.path.join(report_path, file)
                    shutil.move(source_file, destination_file)
                    print(f"Arquivo {file} movido para {report_path}")
                    break
            else:
                print(f"Nenhum arquivo correspondente encontrado para {nome_jar}")
                
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar o comando para {nome_arquivo}:")
            print(e.stderr)
