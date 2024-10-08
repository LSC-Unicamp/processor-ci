import os
import re
import time
from ollama import Client

SERVER_URL = "http://enqii.lsc.ic.unicamp.br:11434"

client = Client(host=SERVER_URL)


def send_prompt(prompt: str, model: str = "qwen2.5:32b") -> tuple[bool, str]: # "qwen2.5:32b"

    response = client.generate(prompt=prompt, model=model)

    if not response or not "response" in response:
        return 0, ""

    return 1, response["response"]


def parse_filtered_files(text: str) -> list:
    # Expressão regular para capturar a lista dentro de colchetes
    match = re.search(r"filtered_files:\s*\[\s*(.*?)\s*\]", text, re.DOTALL)

    if match:
        # Extrai o conteúdo dos colchetes
        file_list_str = match.group(1)

        # Remove espaços em excesso, quebras de linha, e divide a string por vírgulas
        file_list = [file.strip().strip("'") for file in file_list_str.split(",")]

        return file_list

    return []


def remove_top_module(text: str) -> str:
    # Expressão regular para encontrar a linha com o formato top_module: <resposta>
    match = re.search(r"top_module:\s*(\S+)", text)

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
    Remember to ignore memory files such as ram.v or ram.vhdl, peripheral files, caches files, pll files, bus files, board and FPGA files, debug files, among others. 
    Keep only the processor-related files. Return files in template: filtered_files: [<result>].

    TIP: generally directories with names like rtl, core, src, project_name, etc., usually have the processor files. Files with the project name are often processor files.
    All processors have at least one useful file

    Return only the list of files in the requested template, excluding any additional files and comments.

    project_name: {repo_name},
    sim_files: [{sim_files}],
    files: [{files}],
    modules: [{modules}]
    tree: [{tree}]
    """

    ok, response = send_prompt(prompt)

    if not ok:
        raise NameError("Erro ao consultar modelo")

    print (response)

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

    # print(response)

    return remove_top_module(response)


def generate_top_file(top_module_file: str, processor_name: str) -> None:
    template_file = open("rtl/template.v", "r")
    top_module_file = open(f"temp/{processor_name}/{top_module_file}", "r")
    example_file = open("rtl/Risco-5.v", "r")

    template = template_file.read()
    top_module_content = top_module_file.read()
    example = example_file.read()

    template_file.close()
    top_module_file.close()
    example_file.close()

    prompt = f"""
    In the context of processor verification, we use a hardware infrastructure to verify the processor. 
    Both the processor and the infrastructure are hardware described in hardware description language (HDL), in our case Verilog. 
    The processor connects to this infrastructure through a Verilog module that instantiates the infrastructure and the processor, 
    making the necessary connections and adaptations. Below is an example of such a connection. Based on this example, 
    the provided template, and the processor's top module, make the necessary connections and adaptations. 
    Pay attention to details such as whether the processor has two memories or only one, if it always has the read signal enabled and only sends the write signal, 
    among others. After this process, return the complete Verilog file based on the template.
    
    example file: 
    {example}

    template file: 
    {template}

    processor top file:
    {top_module_content}

    """

    ok, response = send_prompt(prompt)

    if not ok:
        raise NameError("Erro ao consultar modelo")

    if os.path.exists(f"rtl/{processor_name}.v"):
        processor_name = f"{processor_name}_{time.time()}"

    final_file = open(f"rtl/{processor_name}.v", "w")
    final_file.write(response)
    final_file.close()
