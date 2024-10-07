import os
import json


def load_config(config_path: str) -> dict:
    """
    Carrega o arquivo de configuração JSON e retorna seu conteúdo.

    :param config_path: Caminho para o arquivo de configuração JSON.
    :return: Conteúdo do JSON como dicionário.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"O arquivo de configuração {config_path} não foi encontrado."
        )

    with open(config_path, "r") as file:
        config_data = json.load(file)

    return config_data


def save_config(config_path: str, config_data: dict) -> None:
    """
    Salva o dicionário de configuração no arquivo JSON especificado.

    :param config_path: Caminho para o arquivo de configuração JSON.
    :param config_data: Dicionário de dados de configuração a ser salvo.
    """
    with open(config_path, "w") as file:
        json.dump(config_data, file, indent=4)


def get_processor_data(config: dict, processor_name: str) -> dict:
    """
    Busca os dados do processador pelo nome no arquivo de configuração.

    :param config: Dicionário de configuração carregado.
    :param processor_name: Nome do processador que deseja buscar.
    :return: Dicionário com os dados do processador, ou None se não encontrado.
    """
    cores = config.get("cores", {})

    processor_data = cores.get(processor_name)
    if not processor_data:
        raise ValueError(
            f"Processador '{processor_name}' não encontrado na configuração."
        )

    return processor_data
