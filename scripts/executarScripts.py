import subprocess
import time
import tracemalloc
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Lista de scripts que você deseja executar
scripts = [
    "cogniCryptScript.py", 
    "cryptoGuardScript.py", 
    "findSecBugsScript.py",
    "extrairArquivosJarScript.py",
    "horusecScript.py"
    ]

# Cria a pasta ./reports se não existir
os.makedirs('./reports', exist_ok=True)

# Caminho do arquivo de relatório unificado
report_path = os.path.join('./reports', 'analise_report.txt')

# Listas para armazenar dados para o gráfico
script_names = []
execution_times = []
memory_usages = []
peak_memory_usages = []

# Abre o arquivo de relatório unificado para escrita
with open(report_path, 'w') as report_file:
    for script in scripts:
        try:
            # Inicia a medição de tempo e memória
            start_time = time.time()
            tracemalloc.start()

            # Executa o script
            result = subprocess.run(['python3.8', script], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Para a medição de tempo e memória
            end_time = time.time()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            # Calcula o tempo de execução
            execution_time = end_time - start_time

            # Armazena os dados para o gráfico
            script_names.append(script)
            execution_times.append(execution_time)
            memory_usages.append(current / 10**6)
            peak_memory_usages.append(peak / 10**6)

            # Cria a mensagem de relatório
            report_message = (
                f"Saída de {script}:\n"
                f"{result.stdout}\n"
                f"Tempo de execução de {script}: {execution_time:.2f} segundos\n"
                f"Consumo de memória de {script}: {current / 10**6:.2f} MB (atual), {peak / 10**6:.2f} MB (pico)\n"
                "----------------------------------------\n"
            )

            # Escreve a mensagem de relatório no arquivo
            report_file.write(report_message)

            # Exibe a mensagem de relatório no console
            print(report_message)

        except subprocess.CalledProcessError as e:
            # Cria a mensagem de relatório de erro
            error_message = (
                f"Erro ao executar {script}:\n"
                f"{e.stderr}\n"
                "----------------------------------------\n"
            )

            # Escreve a mensagem de relatório de erro no arquivo
            report_file.write(error_message)

            # Exibe a mensagem de relatório de erro no console
            print(error_message)

# Cria subplots para unificar os gráficos
fig = make_subplots(rows=2, cols=1, subplot_titles=('Tempo de Execução dos Scripts', 'Consumo de Memória dos Scripts'))

# Adiciona o gráfico de tempo de execução
fig.add_trace(go.Bar(name='Tempo de Execução (s)', x=script_names, y=execution_times), row=1, col=1)

# Adiciona o gráfico de consumo de memória
fig.add_trace(go.Bar(name='Memória Atual (MB)', x=script_names, y=memory_usages), row=2, col=1)
fig.add_trace(go.Bar(name='Memória de Pico (MB)', x=script_names, y=peak_memory_usages), row=2, col=1)

# Atualiza o layout do gráfico
fig.update_layout(title='Análise de Desempenho dos Scripts', xaxis_title='Scripts', yaxis_title='Tempo (s)', barmode='group')
fig.update_yaxes(title_text='Memória (MB)', row=2, col=1)

# Salva o gráfico unificado em um arquivo HTML
fig.write_html('./reports/graficos_report.html')
