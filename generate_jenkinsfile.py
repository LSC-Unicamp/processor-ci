import json

def generate_jenkinsfile(config, fpgas, main_script_path, lang_version, extra_flags=None):
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
    is_vhdl = any(file.endswith('.vhdl') or file.endswith('.vhd') for file in config.get("files", []))
    is_verilog = any(file.endswith('.v') for file in config.get("files", []))

    if is_vhdl and not is_verilog:
        # VHDL simulation command
        simulation_command = f'sh "ghdl -a --std={lang_version} {extra_flags_str} {include_dirs} {files} {sim_files}"'
    elif is_verilog and not is_vhdl:
        # Verilog simulation command
        simulation_command = f'sh "iverilog -o simulation.out -g{lang_version} {extra_flags_str} -s {config["top_module"]} {include_dirs} {files} {sim_files} && vvp simulation.out"'
    else:
        raise ValueError("Os arquivos precisam ser exclusivamente VHDL ou Verilog.")

    # Prepare FPGA stages for each FPGA in parallel
    fpga_parallel_stages = "\n                ".join(
        [
            f'''
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
        fpga_parallel_stages=fpga_parallel_stages
    )
    
    # Save the Jenkinsfile
    with open('Jenkinsfile', 'w') as f:
        f.write(jenkinsfile)
    
    print("Jenkinsfile generated successfully.")

if __name__ == "__main__":
    # Example input data
    config = {
        "repository": "https://github.com/liangkangnan/tinyriscv.git",
        "folder": "tinyriscv",
        "files": [
            "rtl/core/clint.v",
            "rtl/core/csr_reg.v",
            "rtl/core/ctrl.v",
            "rtl/core/defines.v",
            "rtl/core/div.v",
            "rtl/core/ex.v",
            "rtl/core/id_ex.v",
            "rtl/core/id.v",
            "rtl/core/if_id.v",
            "rtl/core/pc_reg.v",
            "rtl/core/regs.v",
            "rtl/core/rib.v",
            "rtl/core/tinyriscv.v"
        ],
        "top_module": "tinyriscv_soc_tb",
        "sim_files": [
            "tb/tinyriscv_soc_tb.v",
            "rtl/debug/jtag_dm.v",
            "rtl/debug/jtag_driver.v",
            "rtl/debug/jtag_top.v",
            "rtl/debug/uart_debug.v",
            "rtl/perips/gpio.v",
            "rtl/perips/ram.v",
            "rtl/perips/rom.v",
            "rtl/perips/spi.v",
            "rtl/perips/timer.v",
            "rtl/perips/uart.v",
            "rtl/soc/tinyriscv_soc_top.v",
            "rtl/utils/full_handshake_rx.v",
            "rtl/utils/full_handshake_tx.v",
            "rtl/utils/gen_buf.v",
            "rtl/utils/gen_dff.v"
        ],
        "include_dirs": [
            "rtl/core"
        ]
    }

    # List of FPGAs
    fpgas = [
        "colorlight_i9",
        "digilent_nexys4_ddr",
        "gowin_tangnano_20k",
        "xilinx_vc709",
        "digilent_arty_a7_100t"
    ]

    # Path to the main.py script
    main_script_path = "/eda/processor-ci/main.py"  # Update this with the actual path to main.py

    # Version of the HDL language to use
    lang_version = "2005"  # Exemplo de versão, pode ser ajustado conforme necessário

    # Extra flags for IVerilog or GHDL
    extra_flags = ["-Wall"]  # Example flags, can be empty or updated with more flags

    # Call function to generate Jenkinsfile
    generate_jenkinsfile(config, fpgas, main_script_path, lang_version, extra_flags)
