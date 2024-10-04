import json

def generate_jenkinsfile(config, fpgas, main_script_path, lang_version):
    jenkinsfile = """
pipeline {{
    agent any
    stages {{
        stage('Git Clone and Cleanup') {{
            steps {{
                sh 'rm -rf {folder}'
                sh 'git clone --recursive {repository} {folder}'
            }}
        }}
        
        stage('Simulation') {{
            steps {{
                dir("{folder}") {{
                    {simulation_command}
                }}
            }}
        }}
        
        stage('FPGA Synthesis') {{
            parallel {{
                {fpga_parallel_stages}
            }}
        }}

        stage('Run Tests') {{
            parallel {{
                {fpga_test_stages}
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
    
    # Determine simulation command based on file types
    is_vhdl = any(file.endswith('.vhdl') or file.endswith('.vhd') for file in config.get("files", []))
    is_verilog = any(file.endswith('.v') for file in config.get("files", []))

    if is_vhdl and not is_verilog:
        # VHDL simulation command
        simulation_command = f'sh "ghdl -a --std={lang_version} {include_dirs} {files} {sim_files}"'
    elif is_verilog and not is_vhdl:
        # Verilog simulation command
        simulation_command = f'sh "iverilog -o simulation.out -g{lang_version} -s {config["top_module"]} {include_dirs} {files} {sim_files} && vvp simulation.out"'
    else:
        raise ValueError("Os arquivos precisam ser exclusivamente VHDL ou Verilog.")

    # Prepare FPGA synthesis steps for each FPGA in parallel
    fpga_parallel_stages = "\n                ".join(
        [
            f'''stage('{fpga}') {{
                    steps {{
                        lock(resource: '{fpga}') {{
                            echo 'FPGA {fpga} bloqueada para síntese.'
                            dir("{config['folder']}") {{
                                sh 'python3 {main_script_path} -c /eda/processor-ci/config.json -p {config["folder"]} -b {fpga}'
                            }}
                        }}
                    }}
                }}''' 
            for fpga in fpgas
        ]
    )

    # Prepare test stages for each FPGA in parallel
    fpga_test_stages = "\n                ".join(
        [
            f'''stage('{fpga} Tests') {{
                    steps {{
                        echo 'Executando testes para FPGA {fpga}.'
                        unlock(resource: '{fpga}')
                    }}
                }}'''
            for fpga in fpgas
        ]
    )

    # Generate Jenkinsfile content
    jenkinsfile = jenkinsfile.format(
        repository=config['repository'],
        folder=config['folder'],
        top_module=config['top_module'],
        include_dirs=include_dirs,
        files=files,
        sim_files=sim_files,
        simulation_command=simulation_command,
        fpga_parallel_stages=fpga_parallel_stages,
        fpga_test_stages=fpga_test_stages
    )
    
    # Save the Jenkinsfile
    with open('Jenkinsfile', 'w') as f:
        f.write(jenkinsfile)
    
    print("Jenkinsfile generated successfully.")

if __name__ == "__main__":
    # Example input data
    config = {
            "repository":"https://github.com/klessydra/T03x.git",
            "name":"T03x",
            "folder":"T03x",
            "files":[
                "klessydra-t0-3th/PKG_RiscV_Klessydra_thread_parameters.vhd",
                "klessydra-t0-3th/PKG_RiscV_Klessydra.vhd",
                "klessydra-t0-3th/RTL-CSR_Unit.vhd",
                "klessydra-t0-3th/RTL-Debug_Unit.vhd",
                "klessydra-t0-3th/RTL-Processing_Pipeline.vhd",
                "klessydra-t0-3th/RTL-Program_Counter_unit.vhd",
                "klessydra-t0-3th/STR-Klessydra_top.vhd"
            ],
            "linguage_version":"2008",
            "top_module":"",
            "sim_files":[

            ]
        }

    # List of FPGAs
    fpgas = [
        "colorlight_i9",
        "digilent_nexys4_ddr",
        #"gowin_tangnano_20k",
        #"xilinx_vc709",
        #"digilent_arty_a7_100t"
    ]

    # Path to the main.py script
    main_script_path = "/eda/processor-ci/main.py"  # Update this with the actual path to main.py

    # Version of the HDL language to use
    lang_version = "2008"  # Exemplo de versão, pode ser ajustado conforme necessário

    # Call function to generate Jenkinsfile
    generate_jenkinsfile(config, fpgas, main_script_path, lang_version)
