import os
import subprocess


CURRENT_DIR = os.getcwd()


def get_macros(board: str) -> str:
    if board == "colorlight_i9":
        return "-DID=0x6a6a6a6a -DCLOCK_FREQ=25000000 -DMEMORY_SIZE=4096"

    if board == "digilent_nexys4_ddr":
        return '-tclargs "ID=0x6a6a6a6a" "CLOCK_FREQ=50000000" "MEMORY_SIZE=4096"'

    if board == "digilent_arty_a7_100t":
        return '-tclargs "ID=0x6a6a6a6a" "CLOCK_FREQ=50000000" "MEMORY_SIZE=4096"'

    if board == "xilinx_vc709":
        return '-tclargs "ID=0x6a6a6a6a" "CLOCK_FREQ=100000000" "MEMORY_SIZE=4096"'

    return '-tclargs "ID=0x6a6a6a6a" "CLOCK_FREQ=50000000" "MEMORY_SIZE=4096"'


def get_prefix(board: str, vhdl: bool) -> str:
    if board == "gowin_tangnano_20k":
        return "add_file"

    if vhdl:
        if board == "colorlight_i9":
            return "yosys ghdl -a"
        return "read_vhdl"

    if board == "colorlight_i9":
        return "yosys read_verilog"

    return "read_verilog"


def make_build_file(config: dict, board: str, toolchain_path: str) -> str:

    if toolchain_path[-1] == "/":
        toolchain_path = toolchain_path[:-1]

    base_config_path = f"{toolchain_path}/processor-ci/build_scripts/{board}.tcl"

    if not os.path.exists(base_config_path):
        raise FileNotFoundError(
            f"O arquivo de configuração {base_config_path} não foi encontrado."
        )

    base_config = None

    with open(base_config_path, "r") as file:
        base_config = file.read()

    if not base_config:
        raise ValueError(
            f"Não foi possível ler o arquivo de configação {base_config_path}."
        )

    final_config_path = CURRENT_DIR + f"/build_{board}.tcl"

    with open(final_config_path, "w") as file:
        prefix = get_prefix(board, False)
        file.write(
            prefix + f' {toolchain_path}/processor-ci/rtl/{config["folder"]}.v\n'
        )

        for i in config["files"]:
            prefix = get_prefix(board, i.endswith(".vhd"))
            file.write(prefix + f" {CURRENT_DIR}/" + i + "\n")

        file.write(base_config)

    print(f"Arquivo de configuração final gerado em {final_config_path}")

    return final_config_path


def build(build_script_path: str, board: str, toolchain_path: str) -> None:
    if toolchain_path[-1] == "/":
        toolchain_path = toolchain_path[:-1]

    makefile_path = f"{toolchain_path}/processor-ci/makefiles/{board}.mk"

    macros = get_macros(board)

    # Define a variável BUILD_SCRIPT antes do comando make
    process = subprocess.Popen(
        [
            "make",
            "-f",
            makefile_path,
            f"BUILD_SCRIPT={build_script_path}",
            f"MACROS={macros}",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Captura a saída e os erros
    stdout, stderr = process.communicate()

    # Verifica o status da execução
    if process.returncode == 0:
        print("Makefile executado com sucesso.")
        print("Saída do Makefile:")
        print(stdout)
    else:
        print("Erro ao executar o Makefile.")
        print(stderr)
        raise subprocess.CalledProcessError(process.returncode, "make")


def flash(board: str, toolchain_path: str) -> None:
    if toolchain_path[-1] == "/":
        toolchain_path = toolchain_path[:-1]

    makefile_path = f"{toolchain_path}/processor-ci/makefiles/{board}.mk"

    process = subprocess.Popen(
        ["make", "-f", makefile_path, "load"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Captura a saída e os erros

    stdout, stderr = process.communicate()

    # Verifica o status da execução
    if process.returncode == 0:
        print("Makefile executado com sucesso.")
        print("Saída do Makefile:")
        print(stdout)
    else:
        print("Erro ao executar o Makefile.")
        print(stderr)
        raise subprocess.CalledProcessError(process.returncode, "make")
