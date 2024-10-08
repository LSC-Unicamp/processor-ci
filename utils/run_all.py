import subprocess

# Caminho para o arquivo que contém a lista de URLs
file_path = 'arquivos.txt'

# Abrir o arquivo e ler as URLs
with open(file_path, 'r') as file:
    urls = file.readlines()

# Remover qualquer espaço ou quebra de linha ao final de cada URL
urls = [url.strip() for url in urls]

# Comando base
command_base = ["proxychains", "python", "config_generator.py", "-u", "", "-c", "-a"]

# Timeout de 3 minutos (180 segundos)
timeout_seconds = 180

# Para cada URL na lista, executar o comando com timeout
for url in urls:
    # Montar o comando com a URL
    command_base[4] = url  # Substituir a URL no comando
    print(f"Executando: {' '.join(command_base)}")

    try:
        # Executar o comando com timeout
        subprocess.run(command_base, timeout=timeout_seconds, check=True)
    except subprocess.TimeoutExpired:
        print(f"Comando para {url} atingiu o tempo limite de {timeout_seconds} segundos.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando para {url}: {e}")
