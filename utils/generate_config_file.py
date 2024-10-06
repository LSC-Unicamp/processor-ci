import subprocess
import os
import glob
import json
import re

# Constante com o diretório de destino
DESTINATION_DIR = "/home/julio/eda/teste_search_script"


def clone_repo(url, repo_name):
    """Clona um repositório do GitHub para um diretório especificado."""
    destination_path = os.path.join(DESTINATION_DIR, repo_name)

    try:
        # Clonar o repositório
        subprocess.run(["git", "clone", url, destination_path], check=True)
        return destination_path
    except subprocess.CalledProcessError as e:
        print(f"Erro ao clonar o repositório: {e}")
        return None


def find_files_with_extension(directory, extensions):
    """Encontra arquivos com extensões específicas em um diretório."""
    files = []
    for extension in extensions:
        files.extend(glob.glob(f"{directory}/**/*.{extension}", recursive=True))
    return files


def is_testbench_file(file_path, repo_name):
    """Verifica se o arquivo parece ser um testbench baseado no nome ou na localização."""
    relative_path = os.path.relpath(file_path, os.path.join(DESTINATION_DIR, repo_name))

    file_name = os.path.basename(relative_path)
    directory_parts = os.path.dirname(relative_path).split(os.sep)

    # Verificando se o nome do arquivo contém palavras-chave
    if re.search(r"(tb|testbench|test)", file_name, re.IGNORECASE):
        return True

    # Verificando se alguma parte do caminho contém palavras-chave
    for part in directory_parts:
        if re.search(
            r"(tests?|testbenches|testbenchs?|simulations?|tb|sim)", part, re.IGNORECASE
        ):
            return True

    return False


def find_include_dirs(directory):
    """Encontra todos os diretórios que contêm arquivos de inclusão."""
    include_files = glob.glob(f"{directory}/**/*.(svh|vh)", recursive=True)
    include_dirs = list(set([os.path.dirname(file) for file in include_files]))
    return include_dirs


def extract_modules(files):
    """Extrai módulos e entidades de arquivos Verilog, SystemVerilog e VHDL."""
    modules = []

    module_pattern_verilog = re.compile(r"module\s+(\w+)\s*")
    entity_pattern_vhdl = re.compile(r"entity\s+(\w+)\s+is", re.IGNORECASE)

    for file_path in files:
        with open(
            file_path, "r", errors="ignore"
        ) as f:  # Ignorar erros de decodificação
            content = f.read()

            # Encontrar módulos Verilog/SystemVerilog
            verilog_matches = module_pattern_verilog.findall(content)
            modules.extend(
                [
                    (module_name, os.path.relpath(file_path))
                    for module_name in verilog_matches
                ]
            )

            # Encontrar entidades VHDL
            vhdl_matches = entity_pattern_vhdl.findall(content)
            modules.extend(
                [
                    (entity_name, os.path.relpath(file_path))
                    for entity_name in vhdl_matches
                ]
            )

    return modules


def main(url):
    # Obter o nome do repositório a partir da URL
    repo_name = url.split("/")[-1].replace(".git", "")

    destination_path = clone_repo(url, repo_name)

    if not destination_path:
        print("Não foi possível clonar o repositório.")
        return

    extensions = ["v", "sv", "vhdl", "vhd"]
    files = find_files_with_extension(destination_path, extensions)

    modules = extract_modules(files)

    modulename_list = []
    for module_name, file_path in modules:
        modulename_list.append(
            {
                "module": module_name,
                "file": os.path.relpath(file_path, destination_path),
            }
        )

    # Separar arquivos em testbench e não-testbench
    tb_files = [f for f in files if is_testbench_file(f, repo_name)]
    non_tb_files = [f for f in files if not is_testbench_file(f, repo_name)]

    include_dirs = find_include_dirs(destination_path)

    # Montar o JSON de saída
    output_json = {
        "name": repo_name,
        "folder": repo_name,
        "sim_files": [os.path.relpath(tb_f, destination_path) for tb_f in tb_files],
        "design_files": [
            os.path.relpath(non_tb_f, destination_path) for non_tb_f in non_tb_files
        ],
        "include_dirs": include_dirs,
        "modules": modulename_list,
    }

    print(json.dumps(output_json, indent=4))


def run():
    url = input("Insira a URL do repositório: ")
    main(url)


if __name__ == "__main__":
    run()
