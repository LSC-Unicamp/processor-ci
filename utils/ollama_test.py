import os
import subprocess
import sys
import shutil
import json
import ollama  # Ollama Python SDK
from ollama import Client


# Step 1: Clone the GitHub Repository
def clone_repository(repo_url, local_dir):
    if os.path.exists(local_dir):
        print(f'Directory {local_dir} already exists. Deleting and recloning.')
        shutil.rmtree(local_dir)  # Remove the directory if it already exists
    try:
        subprocess.run(['git', 'clone', repo_url, local_dir], check=True)
        print(f'Cloned repository into {local_dir}')
    except subprocess.CalledProcessError as e:
        print(f'Failed to clone the repository: {e}')
        sys.exit(1)


# Step 2: Use Ollama to find the top-level CPU module and its dependencies
def find_cpu_top_and_dependencies(repo_dir):
    # Gather all Verilog files in the repository
    verilog_files = [
        os.path.join(dp, f)
        for dp, dn, filenames in os.walk(repo_dir)
        for f in filenames
        if f.endswith('.v')
    ]

    # Create the prompt for Ollama
    prompt = f'The repository contains the following Verilog files: {verilog_files}. Identify the top-level CPU module (typically named top, core, cpu_top, cpu_csr, or main) (give me just one top module) and list all the necessary Verilog files required for compilation.\n'

    prompt_2 = 'Also organize the files like the following template:\n\
                    Top-Level Module:\n\
                        top_module goes here\n\
                    Modules required for compilation:\n'

    prompt_3 = 'Also show the path from after the /ollama-tests/ directory to the file'
    prompt = prompt + prompt_2 + prompt_3

    # Request Ollama to analyze the Verilog files
    response = client.generate(model='qwen2.5:32b', prompt=prompt)

    # Check if response contains expected content
    if response and 'response' in response:
        print(
            'Ollama Response:', response['response']
        )  # Debugging print to ensure you see the response

        try:
            # Variables to hold the top module and core modules
            top_level_module = ''
            cpu_core_modules = []

            # Split the response into lines
            lines = response['response'].split('\n')

            # Initialize flags to detect sections
            top_module_section = False
            cpu_core_section = False

            # Iterate over lines to extract data
            for line in lines:
                line = line.strip()  # Clean up extra spaces

                if 'Top-Level Module:' in line:
                    top_module_section = True
                    cpu_core_section = False  # Reset any other section
                    continue  # Move to the next line after the header

                if 'Modules required for compilation:' in line:
                    cpu_core_section = True
                    top_module_section = False  # Reset top module section
                    continue  # Move to the next line after the header

                # Capture the top-level module
                if top_module_section and line.startswith('-'):
                    top_level_module = line.split('- ')[1].strip()

                # Capture the CPU core modules
                if cpu_core_section and line.startswith('-'):
                    cpu_core_modules.append(line.split('- ')[1].strip())

            # Check if we successfully extracted the top module and core modules
            if top_level_module and cpu_core_modules:
                return top_level_module, cpu_core_modules
            else:
                print(
                    'Failed to find the top-level module or CPU core modules.'
                )
                sys.exit(1)

        except Exception as e:
            print(f'Error parsing Ollama response: {e}')
            sys.exit(1)
    else:
        print('No valid response from Ollama.')
        sys.exit(1)


def find_cpu_top_and_dependencies(repo_dir):
    # Gather all Verilog files in the repository
    verilog_files = [
        os.path.join(dp, f)
        for dp, dn, filenames in os.walk(repo_dir)
        for f in filenames
        if f.endswith('.v')
    ]

    # Create the prompt for Ollama
    prompt = f'The repository contains the following Verilog files: {verilog_files}. Identify the top-level CPU module (typically named top, core, cpu_top, cpu_csr, or main) (give me just one top module) and list all the necessary Verilog files required for compilation.\n'
    prompt += 'Also organize the files like the following template:\n'
    prompt += 'Top-Level Module:\n    top_module goes here\nModules required for compilation:\n'
    prompt += 'Also show the path from after the /ollama-tests/ directory to the file'

    # Request Ollama to analyze the Verilog files
    response = client.generate(model='qwen2.5:32b', prompt=prompt)

    # Check if response contains expected content
    if response and 'response' in response:
        print(
            'Ollama Response:', response['response']
        )  # Debugging print to ensure you see the response

        try:
            # Variables to hold the top module and core modules
            top_level_module = ''
            core_modules = []
            additional_modules = []
            testbench_modules = []

            # Split the response into lines
            lines = response['response'].split('\n')

            # Initialize flags to detect sections
            top_module_section = False
            core_module_section = False

            # Iterate over lines to extract data
            for line in lines:
                line = line.strip()  # Clean up extra spaces

                # Identify sections based on the headings in the response
                if 'Top-Level Module:' in line:
                    top_module_section = True
                    core_module_section = False  # Reset other sections
                    continue  # Move to the next line after the header

                if 'Modules required for compilation:' in line:
                    core_module_section = True
                    top_module_section = False  # Reset other sections
                    continue

                # Capture the top-level module
                if top_module_section and line:
                    top_level_module = line.strip()

                # Capture the core modules
                if core_module_section and line:
                    core_modules.append(line.strip())

            # Check if we successfully extracted the top module and core modules
            if top_level_module and core_modules:
                return top_level_module, core_modules
            else:
                print('Failed to find the top-level module or core modules.')
                sys.exit(1)

        except Exception as e:
            print(f'Error parsing Ollama response: {e}')
            sys.exit(1)
    else:
        print('No valid response from Ollama.')
        sys.exit(1)


# Step 3: Return a list of necessary .v files and directories for compilation
def get_necessary_verilog_files_and_dirs(repo_dir):
    cpu_top_file, dependencies = find_cpu_top_and_dependencies(repo_dir)

    # Combine the CPU top file and its dependencies into a single list
    necessary_files = [cpu_top_file] + dependencies

    # Get unique directories for the necessary Verilog files
    necessary_dirs = {os.path.dirname(file) for file in necessary_files}

    print('Necessary .v files for CPU compilation:')
    for file in necessary_files:
        print(file)

    print('\nNecessary directories to include with -I flag:')
    for directory in necessary_dirs:
        print(directory)

    return (
        necessary_files,
        necessary_dirs,
        cpu_top_file,
    )  # Return necessary files, directories, and top module


# Step 4: Ask Ollama which Verilog standard is required
def determine_verilog_standard(verilog_files):
    files_str = ', '.join(verilog_files)

    prompt = f'Based on the following Verilog files: {files_str}, determine which Verilog standard (2001, 2005, 2005-sv, 2008) is required for proper compilation.'

    response = client.generate(model='qwen2.5:32b', prompt=prompt)

    if response and 'response' in response:
        print("Ollama's recommendation for Verilog standard:")
        print(response['response'])
        return response['response'].strip().lower()
    else:
        print('Failed to determine the required Verilog standard.')
        sys.exit(1)


# Step 5: Check for extra flags needed for Icarus Verilog compilation using Ollama
def check_extra_flags(verilog_files):
    files_str = ', '.join(verilog_files)

    # Use Ollama to suggest any extra flags
    prompt = f'The following Verilog files: {files_str} are part of a CPU design. Can you suggest any extra Icarus Verilog flags that might be needed during compilation?'

    response = client.generate(model='qwen2.5:32b', prompt=prompt)
    print(response['response'])

    if response and 'response' in response:
        print("Ollama's suggestion for extra Icarus Verilog flags:")
        print(response['response'])
        return response['response'].strip().split()
    else:
        print('Failed to determine extra Icarus Verilog flags.')
        sys.exit(1)


# Step 6: Write JSON file based on the specified template
def write_json_output(
    repo_url,
    top_module,
    necessary_files,
    language_version,
    include_dirs,
    extra_flags,
):
    output_data = ' \
        "template": { \
            "repository":, \
            "name": "template", \
            "folder": "template", \
            "files": [], \
            "language_version": , \
            "top_module": , \
            "sim_files": [],\
            "include_dirs": [],\
            "extra_flags": [],\
            "enable": false \
        }'

    prompt = f'Based on the following template: {output_data} write a json file with the following parameters: {repo_url}, {necessary_files}, {language_version}, {top_module}, {include_dirs}, {extra_flags}'

    response = client.generate(model='qwen2.5:32b', prompt=prompt)
    print(response)

    # Write the JSON to a file
    json_file_path = 'output.json'
    with open(json_file_path, 'w') as json_file:
        json.dump(response, json_file, indent=4)
        print(f'JSON output written to {json_file_path}')


# Example usage
if __name__ == '__main__':
    client = Client(host='http://enqii.lsc.ic.unicamp.br:11434')
    # Provide the GitHub URL for the CPU design
    repo_url = input('Enter the GitHub repo URL for the Verilog CPU design: ')
    local_dir = './Documentos/ollama-testes/'

    # Clone the repository
    clone_repository(repo_url, local_dir)

    # Get the list of necessary Verilog files and directories for the CPU
    (
        necessary_verilog_files,
        necessary_verilog_dirs,
        top_module,
    ) = get_necessary_verilog_files_and_dirs(local_dir)

    # Determine which Verilog standard is required
    verilog_standard = determine_verilog_standard(necessary_verilog_files)

    # Check for extra flags needed using Ollama
    extra_flags = check_extra_flags(necessary_verilog_files)

    # Write the JSON output
    write_json_output(
        repo_url,
        top_module,
        necessary_verilog_files,
        verilog_standard,
        necessary_verilog_dirs,
        extra_flags,
    )
