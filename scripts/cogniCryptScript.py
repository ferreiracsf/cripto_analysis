import os
import subprocess
import time

# Caminho base do repositório
caminho_base = os.path.dirname(os.path.abspath(__file__))
# Caminho da pasta 'api'
caminho_pasta = os.path.join(caminho_base, 'jars')
# Caminho do scanner Java
caminho_scanner = os.path.join(caminho_base, 'HeadlessJavaScanner-4.0.0-jar-with-dependencies.jar')
# Caminho dos algoritmos de validação
rulesDir = os.path.join(caminho_base, 'JCA')
# Caminho para salvar os relatórios
reportPath = os.path.join(caminho_base, 'reports')
# Tipo de formato dos relatórios
reportFormat = 'TXT'
# Lista para armazenar os nomes dos arquivos .jar
arquivos_jar = []
tempos_execucao = []
# Versão para ser compilada
version = '11.0.24-amzn'

# Altera a versão do Java pelo sdkman e executa os comandos subsequentes no mesmo shell
try:
    # Comando para alterar a versão do Java e executar o scanner Java
    command = f"""
    bash -c '
    source $HOME/.sdkman/bin/sdkman-init.sh && 
    sdk use java {version} && 
    for arquivo in {caminho_pasta}/*.jar; do
        identificador=$(basename "$arquivo" .jar)
        caminho_relatorio="{reportPath}/$identificador"
        mkdir -p "$caminho_relatorio"
        java -jar "{caminho_scanner}" --rulesDir "{rulesDir}" --appPath "$arquivo" --reportPath "$caminho_relatorio" --reportFormat "{reportFormat}" --identifier "$identificador"
    done
    '
    """
    # Executa o comando no shell
    subprocess.run(command, shell=True, check=True)
except subprocess.CalledProcessError as e:
    print("Erro ao executar o comando:")
    print(e.stderr)

# Exibe os nomes dos arquivos .jar processados e seus tempos de execução
for nome_arquivo in os.listdir(caminho_pasta):
    if nome_arquivo.endswith('.jar'):
        arquivos_jar.append(nome_arquivo)

for arquivo in arquivos_jar:
    identificador = os.path.splitext(arquivo)[0]
    caminho_relatorio = os.path.join(reportPath, identificador)
    if os.path.exists(caminho_relatorio):
        print(f'Processado: {arquivo}')
