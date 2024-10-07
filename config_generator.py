import os
import re
import time
import json
import shutil
import argparse
from core.config import load_config, get_processor_data, save_config
from core.file_manager import (
    clone_repo,
    remove_repo,
    find_files_with_extension,
    extract_modules,
    is_testbench_file,
    find_include_dirs,
)
from core.graph import build_module_graph
from core.ollama import send_prompt
from core.jenkins import generate_jenkinsfile


BASE_DIR = "jenkins_pipeline/"
FPGAs = [
    "colorlight_i9",
    "digilent_nexys4_ddr",
    # "gowin_tangnano_20k",
    # "xilinx_vc709",
    # "digilent_arty_a7_100t"
]
DESTINATION_DIR = "./temp"
MAIN_SCRIPT_PATH = "/eda/processor-ci/main.py"

def parse_filtered_files(text: str) -> list:
    # Expressão regular para capturar a lista dentro de colchetes
    match = re.search(r'filtered_files:\s*\[\s*(.*?)\s*\]', text, re.DOTALL)
    
    if match:
        # Extrai o conteúdo dos colchetes
        file_list_str = match.group(1)
        
        # Remove espaços em excesso, quebras de linha, e divide a string por vírgulas
        file_list = [file.strip().strip("'") for file in file_list_str.split(',')]
        
        return file_list
    
    return []
    
def remove_top_module(text: str) -> str:
    # Expressão regular para encontrar a linha com o formato top_module: <resposta>
    match = re.search(r'top_module:\s*(\S+)', text)
    
    if match:
        # Extrai o módulo encontrado
        top_module = match.group(1)
        return top_module
    
    return ""

def get_filtered_files_list(files, sim_files, modules, tree, repo_name):
    prompt = f"""
    Processors are generally divided into one or more modules; for example, I can have a module for the ALU, one for the register bank, etc. 
    The files below are the hardware description language files for a processor and its peripherals. 
    Additionally, we have a list of modules present in the processor (approximately, some modules might be missing) and which files they are in, 
    along with their dependency tree. The provided data has two categories: sim_files and files. 
    The sim_files are testbench and verification files (usually containing terms like tests, tb, testbench, among others in the name), 
    while the files are the remaining files, including unnecessary ones such as SoC, peripherals (memory, GPIO, UART, etc.). 
    Based on this, keep only the files that you deem relevant to a processor and return them in a Python list. 
    Remember to ignore memory files such as ram.v or ram.vhdl, peripheral files, board and FPGA files, debug files, among others. 
    Keep only the processor-related files. Return the list of files in the requested template.

    filtered_files: [<result>]

    project_name: {repo_name},
    sim_files: [{sim_files}],
    files: [{files}],
    modules: [{modules}]
    tree: [{tree}]
    """

    ok, response = send_prompt(prompt)

    if not ok:
        raise NameError("Erro ao consultar modelo")

    #print (response)

    return parse_filtered_files(response)


def get_top_module(files, sim_files, modules, tree, repo_name):
    prompt = f"""
    Processors are generally divided into one or more modules; for example, I can have a module for the ALU, one for the register bank, etc. 
    The files below are the hardware description language files for a processor and its peripherals. 
    Additionally, we have a list of modules present in the processor (approximately, some modules might be missing), and which files they are in, along with their dependency tree. 
    The provided data has two categories: sim_files and files. The sim_files are testbench and verification files (usually containing terms like tests, tb, testbench, among others in the name), 
    while the files are the remaining files, including unnecessary ones such as SoC and peripherals (memory, GPIO, UART, etc.). Based on this, find the processor's top module—remember, the processor's, not the SoC's.
    Return the top module in the following template: top_module: <result>.

    project_name: {repo_name},
    sim_files: [{sim_files}],
    files: [{files}],
    modules: [{modules}]
    tree: [{tree}]
    """

    ok, response = send_prompt(prompt)

    if not ok:
        raise NameError("Erro ao consultar modelo")

    #print(response)

    return remove_top_module(response)


def copy_hardware_template(repo_name: str) -> None:
    # Caminho do diretório de origem
    orig = "rtl/template.v"

    # Caminho do diretório de destino
    dest = f"rtl/{repo_name}.v"

    if os.path.exists(dest):
        print("Arquivo já existe")
        return

    # Copiar o diretório
    shutil.copy(orig, dest)


def generate_processor_config(
    url: str, add_config: bool, plot_graph: bool, config_file_path: str
) -> None:
    repo_name = url.split("/")[-1].replace(".git", "")

    destination_path = clone_repo(url, repo_name)

    if not destination_path:
        print("Não foi possível clonar o repositório.")
        return

    extensions = ["v", "sv", "vhdl", "vhd"]
    files, extension = find_files_with_extension(destination_path, extensions)

    modules = extract_modules(files)

    modulename_list = []
    for module_name, file_path in modules:
        modulename_list.append(
            {
                "module": module_name,
                "file": os.path.relpath(file_path, destination_path),
            }
        )

    tb_files = []
    non_tb_files = []

    for f in files:
        if is_testbench_file(f, repo_name):
            tb_files.append(f)
        else:
            non_tb_files.append(f)

    tb_files = [os.path.relpath(tb_f, destination_path) for tb_f in tb_files]
    non_tb_files = [
        os.path.relpath(non_tb_f, destination_path) for non_tb_f in non_tb_files
    ]

    include_dirs = find_include_dirs(destination_path)

    # Construir os grafos direto e inverso
    module_graph, module_graph_inverse = build_module_graph(files, modules)

    filtered_files = get_filtered_files_list(non_tb_files, tb_files, modules, module_graph, repo_name)
    top_module = get_top_module(non_tb_files, tb_files, modules, module_graph, repo_name)

    remove_repo(repo_name)

    language_version = "2005"

    if extension == ".vhdl":
        language_version = "08"
    elif extension == ".vhd":
        language_version = "08"
    elif extension == ".sv":
        language_version = "2012"

    output_json = {
        "name": repo_name,
        "folder": repo_name,
        "sim_files": tb_files,
        "files": filtered_files,
        "include_dirs": include_dirs,
        "repository": url,
        "top_module": top_module,
        "extra_flags": [],
        "language_version": language_version,
    }

    print("Result: ")
    print(json.dumps(output_json, indent=4))

    output_json["modules"] = modulename_list
    output_json["module_graph"] = module_graph
    output_json["module_graph_inverse"] = module_graph_inverse
    output_json["non_tb_files"] = non_tb_files

    log_file = open(f"logs/{repo_name}_{time.time()}.json", "w")

    log_file.write(json.dumps(output_json, indent=4))

    log_file.close()

    copy_hardware_template(repo_name)

    if add_config:
        config = load_config(config_file_path)

        config["cores"][repo_name] = output_json

        save_config(config_file_path, config)

    if plot_graph:
        # Plotar os grafos
        plot_graph(module_graph, "Grafo Direto dos Módulos")
        plot_graph(module_graph_inverse, "Grafo Inverso dos Módulos")


def generate_all_pipelines(config_file_path: str) -> None:
    config = load_config(config_file_path)

    for key in config["cores"].keys():
        processor_data = get_processor_data(config, key)
        generate_jenkinsfile(
            processor_data,
            FPGAs,
            MAIN_SCRIPT_PATH,
            processor_data["language_version"],
            processor_data["extra_flags"],
        )
        os.rename("Jenkinsfile", f'{BASE_DIR}{processor_data["name"]}.Jenkinsfile')

    print("Jenkinsfiles generated successfully.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Script para gerar as configurações de um processador"
    )

    parser = argparse.ArgumentParser(
        description="Script to generate processor configurations"
    )

    parser.add_argument(
        "-j",
        "--generate-all-jenkinsfiles",
        action="store_true",
        help="Generates a Jenkinsfiles for the processors",
    )
    parser.add_argument(
        "-c",
        "--generate-config",
        action="store_true",
        help="Generates a processor configuration",
    )
    parser.add_argument(
        "-g",
        "--plot-graph",
        action="store_true",
        help="Plots the graph of the generated configuration",
    )
    parser.add_argument(
        "-a",
        "--add-config",
        action="store_true",
        help="Adds the generated configuration to the config file",
    )
    parser.add_argument(
        "-p",
        "--path-config",
        type=str,
        default="config.json",
        help="Path to the config file",
    )
    parser.add_argument(
        "-u",
        "--processor-url",
        type=str,
        help="URL of the processor repository",
    )

    args = parser.parse_args()

    if args.generate_config:
        if not args.processor_url:
            raise ValueError("Argumento processor-url não encontrado")

        generate_processor_config(
            args.processor_url, args.add_config, args.plot_graph, args.path_config
        )

    if args.generate_all_jenkinsfiles:
        generate_all_pipelines(args.path_config)

    if not args.generate_config and not args.generate_all_jenkinsfiles:
        print("Nenhum comando fornecido, utilize --help para listar as opcões")


if __name__ == "__main__":
    main()
