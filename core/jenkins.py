def generate_jenkinsfile(
    config: dict,
    fpgas: list,
    main_script_path: str,
    lang_version: str,
    extra_flags: list = None,
) -> None:

    jenkinsfile = """
pipeline {{
    agent any
    stages {{
        stage('Git Clone') {{
            steps {{
                sh 'rm -rf {folder}'
                sh 'git clone --recursive {repository} {folder}'
            }}
        }}

        {pre_script}

        stage('Simulation') {{
            steps {{
                dir("{folder}") {{
                    {simulation_command}
                }}
            }}
        }}
        
        stage('FPGA Build Pipeline') {{
            parallel {{
                {fpga_parallel_stages}
            }}
        }}
    }}
    post {{
        always {{
            dir("{folder}") {{
                sh 'rm -rf *'
            }}
        }}
    }}
}}
"""

    # Prepare file lists
    files = " ".join(config.get("files", []))
    sim_files = " ".join(config.get("sim_files", []))
    include_dirs = " ".join(f"-I {inc}" for inc in config.get("include_dirs", []))

    # Define extra flags if provided
    extra_flags_str = " ".join(extra_flags) if extra_flags else ""

    # Determine simulation command based on file types
    is_vhdl = any(
        file.endswith(".vhdl") or file.endswith(".vhd")
        for file in config.get("files", [])
    )
    is_verilog = any(file.endswith(".v") or file.endswith(".sv") for file in config.get("files", []))

    if is_vhdl and not is_verilog:
        # VHDL simulation command
        simulation_command = f'sh "ghdl -a --std={lang_version} {extra_flags_str} {include_dirs} {files} {sim_files}"'
    elif is_verilog and not is_vhdl:
        # Verilog simulation command
        simulation_command = f'sh "iverilog -o simulation.out -g{lang_version} {extra_flags_str} -s {config["top_module"]} {include_dirs} {files} {sim_files}"'
    else:
        raise ValueError("Os arquivos precisam ser exclusivamente VHDL ou Verilog.")

    # Prepare FPGA stages for each FPGA in parallel
    fpga_parallel_stages = "\n                ".join(
        [
            f"""
                stage('{fpga}') {{
                    options {{
                        lock(resource: '{fpga}')
                    }}
                    stages {{
                        stage('Síntese e PnR') {{
                            steps {{
                                dir("{config['folder']}") {{
                                    echo 'Iniciando síntese para FPGA {fpga}.'
                                    sh 'python3 {main_script_path} -c /eda/processor-ci/config.json -p {config["folder"]} -b {fpga}'
                                }}
                            }}
                        }}
                        stage('Flash {fpga}') {{
                            steps {{
                                dir("{config['folder']}") {{
                                    echo 'FPGA {fpga} bloqueada para flash.'
                                    sh 'python3 {main_script_path} -c /eda/processor-ci/config.json -p {config["folder"]} -b {fpga} -l'
                                }}
                            }}
                        }}
                        stage('Teste {fpga}') {{
                            steps {{
                                echo 'Testando FPGA {fpga}.'
                                dir("{config['folder']}") {{
                                    // Insira aqui os comandos de teste necessários
                                }}
                            }}
                        }}
                    }}
                }}"""
            for fpga in fpgas
        ]
    )

    pre_script = ""

    if "pre_script" in config.keys():
        pre_script = f"""
        stage('Verilog Convert') {{
            steps {{
                dir("{config['folder']}") {{
                    sh '{config['pre_script']}'
                }}
            }}
        }}
        """

    # Generate Jenkinsfile content
    jenkinsfile = jenkinsfile.format(
        repository=config["repository"],
        folder=config["folder"],
        pre_script=pre_script,
        top_module=config["top_module"],
        include_dirs=include_dirs,
        files=files,
        sim_files=sim_files,
        simulation_command=simulation_command,
        fpga_parallel_stages=fpga_parallel_stages,
    )

    # Save the Jenkinsfile
    with open("Jenkinsfile", "w") as f:
        f.write(jenkinsfile)

    print("Jenkinsfile generated successfully.")
