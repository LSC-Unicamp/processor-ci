import subprocess
import os
import glob
import json
import re
import shutil
import networkx as nx
import matplotlib.pyplot as plt

# Constante com o diretório de destino
DESTINATION_DIR = "./"


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


def remove_repo(repo_name):
    destination_path = os.path.join(DESTINATION_DIR, repo_name)

    shutil.rmtree(destination_path)


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


def find_module_instances(content, module_list):
    """Encontra instâncias de módulos em um arquivo Verilog, SystemVerilog ou VHDL."""
    instances = []

    # Padrão para instâncias em Verilog/SystemVerilog: modulo inst_name(...) ou modulo #(...) inst_name(...)
    verilog_instance_pattern = re.compile(
        r"(\w+)\s*(?:#\s*\(.*?\)\s*)?\w+\s*\(.*?\)\s*;", re.DOTALL
    )

    # Padrão para instâncias em VHDL: component module_name is
    vhdl_instance_pattern = re.compile(r"component\s+(\w+)\s+is", re.IGNORECASE)

    # Procurar instâncias em Verilog/SystemVerilog
    for match in verilog_instance_pattern.findall(content):
        if match in module_list:
            instances.append(match)

    # Procurar instâncias em VHDL
    for match in vhdl_instance_pattern.findall(content):
        if match in module_list:
            instances.append(match)

    return instances


def build_module_graph(files, modules):
    """Constrói um grafo de dependência entre os módulos."""
    module_graph = {}
    module_graph_inverse = {}

    module_names = [module[0] for module in modules]

    # Inicializar o grafo direto e inverso com cada módulo
    for module_name, _ in modules:
        module_graph[module_name] = []
        module_graph_inverse[module_name] = []

    for file_path in files:
        with open(
            file_path, "r", errors="ignore"
        ) as f:  # Ignorar erros de decodificação
            content = f.read()

            # Encontrar o nome do módulo atual (módulo onde as instâncias estão sendo feitas)
            current_module_match = re.search(r"module\s+(\w+)", content)
            if not current_module_match:
                continue  # Ignorar arquivos sem um módulo Verilog

            current_module_name = current_module_match.group(1)

            # Encontrar as instâncias dentro deste módulo
            module_instances = find_module_instances(content, module_names)

            # Atualizar o grafo direto (instanciado -> instanciador) e inverso (instanciador -> instanciado)
            for instance in module_instances:
                if instance in module_graph:
                    module_graph[instance].append(current_module_name)
                    module_graph_inverse[current_module_name].append(instance)

    return module_graph, module_graph_inverse


def plot_graph(module_graph, inverse=False):
    G = nx.DiGraph()

    for node, edges in module_graph.items():
        for edge in edges:
            if inverse:
                G.add_edge(edge, node)
            else:
                G.add_edge(node, edge)

    plt.figure(figsize=(10, 8))

    # Escolher o layout
    pos = nx.spring_layout(G)  # Tente também circular_layout, shell_layout, etc.

    # Desenhar o grafo
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=3000,
        node_color="lightblue",
        font_size=10,
        font_weight="bold",
        edge_color="gray",
        arrows=True,
    )

    plt.title(
        "Module Dependency Graph (Inverse)" if inverse else "Module Dependency Graph"
    )
    plt.show()


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

    # Construir os grafos direto e inverso
    module_graph, module_graph_inverse = build_module_graph(files, modules)

    # Montar o JSON de saída
    output_json = {
        "name": repo_name,
        "folder": repo_name,
        "sim_files": [os.path.relpath(tb_f, destination_path) for tb_f in tb_files],
        "design_files": [
            os.path.relpath(non_tb_f, destination_path) for non_tb_f in non_tb_files
        ],
        "include_dirs": include_dirs,
        "repository": url,
        "top_module": "",
        "extra_flags": [],
        # "modules": modulename_list,
        # "module_graph": module_graph,
        # "module_graph_inverse": module_graph_inverse
    }

    print(json.dumps(output_json, indent=4))

    # Plotar os grafos
    # plot_graph(module_graph, "Grafo Direto dos Módulos")
    # plot_graph(module_graph_inverse, "Grafo Inverso dos Módulos")

    remove_repo(repo_name)


def run():
    url = input("Insira a URL do repositório: ")
    main(url)


if __name__ == "__main__":
    run()
