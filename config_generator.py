import os
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


def get_filtered_files_list(files, sim_files, modules, tree):
    prompt = f"""
    Processors are generally divided into one or more modules; for example, I can have a module for the ALU, one for the register bank, etc. 
    The files below are the hardware description language files for a processor and its peripherals. 
    Additionally, we have the list of modules present in the processor (approximately, some modules might be missing) and which files they are in, as well as their dependency tree. 
    The provided data has two categories: sim_files and files. The sim_files are testbench and verification files (usually containing terms like tests, tb, testbench, 
    among others in the name), while the files are the remaining files, including unnecessary ones such as SoC and peripherals (memory, GPIO, UART, etc.). 
    Based on this, keep only the files you deem relevant to a processor and return them in a Python list. Ignore memory and soc files such as ram.v, ram.vhdl, soc.v, etc. Remember, returns only files list.

    sim_files: [{sim_files}],
    files: [{files}],
    modules: [{modules}]
    tree: [{tree}]
    """

    ok, response = send_prompt(prompt)

    if not ok:
        raise NameError("Erro ao consultar modelo")

    print(response)


def get_top_module(files, sim_files, modules, tree):
    prompt = f"""
    Processors are generally divided into one or more modules; for example, I can have a module for the ALU, one for the register bank, etc. 
    The files below are the hardware description language files for a processor and its peripherals. 
    Additionally, we have a list of modules present in the processor (approximately, some modules might be missing), and which files they are in, along with their dependency tree. 
    The provided data has two categories: sim_files and files. The sim_files are testbench and verification files (usually containing terms like tests, tb, testbench, among others in the name), 
    while the files are the remaining files, including unnecessary ones such as SoC and peripherals (memory, GPIO, UART, etc.). Based on this, find the processor's top module—remember, the processor's, not the SoC's.
    Here is the response in the requested template:

    top_module: <resultado>

    sim_files: [{sim_files}],
    files: [{files}],
    modules: [{modules}]
    tree: [{tree}]
    """

    ok, response = send_prompt(prompt)

    if not ok:
        raise NameError("Erro ao consultar modelo")

    print(response)


def copy_hardware_template(repo_name: str) -> None:
    # Caminho do diretório de origem
    orig = "rtl/template.v"

    # Caminho do diretório de destino
    dest = f"rtl/{repo_name}.v"

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

    # get_top_module(non_tb_files, tb_files, modules, module_graph)

    remove_repo(repo_name)

    output_json = {
        "name": repo_name,
        "folder": repo_name,
        "sim_files": tb_files,
        "files": non_tb_files,
        "include_dirs": include_dirs,
        "repository": url,
        "top_module": "",
        "extra_flags": [],
        "language_version": "2005",
    }

    print("Result: ")
    print(json.dumps(output_json, indent=4))

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
