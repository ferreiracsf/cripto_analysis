import os
import subprocess
import time

# Caminho base do repositório
caminho_base = os.path.dirname(os.path.abspath(__file__))
# Caminho da pasta 'jars'
caminho_pasta = os.path.join(caminho_base, 'jars')
# Caminho do scanner Java
caminho_scanner = os.path.join(caminho_base, './findsecbugs/findsecbugs.sh')
# Caminho para salvar os relatórios
reportPath = os.path.join(caminho_base, 'reports')
# Versão para ser compilada
version = '17.0.12-amzn'

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
        {caminho_scanner} -progress -html -output "$caminho_relatorio/$identificador.html" "$arquivo"
    done
    '
    """
    # Executa o comando no shell
    subprocess.run(command, shell=True, check=True)
except subprocess.CalledProcessError as e:
    print("Erro ao executar o comando:")
    print(e.stderr)
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")
