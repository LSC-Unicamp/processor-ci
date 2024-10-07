import os
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
from core.ollama import get_filtered_files_list, get_top_module, generate_top_file
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


def get_top_module_file(modules: list[dict[str, str]], top_module: str) -> str:
    for module in modules:
        if module["module"] == top_module:
            return module["file"]

    return ""

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

    filtered_files = get_filtered_files_list(
        non_tb_files, tb_files, modules, module_graph, repo_name
    )
    top_module = get_top_module(
        non_tb_files, tb_files, modules, module_graph, repo_name
    )

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

    # copy_hardware_template(repo_name)
    top_module_file = get_top_module_file(modulename_list, top_module)
    generate_top_file(top_module_file, repo_name)

    remove_repo(repo_name)

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
