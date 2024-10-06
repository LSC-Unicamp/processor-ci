import argparse
from core.config import get_processor_data, load_config
from core.fpga import make_build_file, flash, build


def main(
    config_path: str,
    processor_name: str,
    board_name: str,
    toolchain_path: str,
    load: bool = False,
) -> None:
    # Carrega o arquivo de configuração
    config = load_config(config_path)

    # Busca os dados do processador pelo nome
    processor_data = get_processor_data(config, processor_name)

    # Exibe os argumentos recebidos e os dados do processador

    build_file_path = make_build_file(processor_data, board_name, toolchain_path)

    if load:
        flash(board_name, toolchain_path)
    else:
        build(build_file_path, board_name, toolchain_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script para configurar o design com base no processador e placa."
    )

    # Definição dos argumentos obrigatórios
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        required=True,
        help="Caminho do arquivo de configuração do script.",
    )
    parser.add_argument(
        "-p",
        "--processor",
        type=str,
        required=True,
        help="Nome do processador a ser utilizado.",
    )
    parser.add_argument(
        "-b",
        "--board",
        type=str,
        required=True,
        help="Nome da placa a ser utilizada.",
    )

    # Parâmetro opcional para o caminho das toolchains
    parser.add_argument(
        "-t",
        "--toolchain",
        type=str,
        default="/eda",
        required=False,
        help="Caminho para as toolchains (padrão: /eda).",
    )

    # Parâmetro opcional para carregar o bitstream
    parser.add_argument(
        "-l",
        "--load",
        action="store_true",
        help="Carregar o bitstream na FPGA.",
    )

    # Parse dos argumentos
    args = parser.parse_args()

    # Chama a função principal com os argumentos
    main(
        args.config,
        args.processor,
        args.board,
        args.toolchain,
        args.load,
    )
