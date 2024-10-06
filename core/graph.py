import re
import networkx as nx
import matplotlib.pyplot as plt


def find_module_instances(content: str, module_list: list) -> list:
    """Encontra instâncias de módulos em um arquivo Verilog, SystemVerilog ou VHDL."""
    instances = []

    # Padrão para instâncias em Verilog/SystemVerilog: modulo inst_name(...) ou modulo #(...) inst_name(...)
    verilog_instance_pattern = re.compile(
        r"(\w+)\s*(?:#\s*\(.*?\)\s*)?\w+\s*\(.*?\)\s*;", re.DOTALL
    )

    # Padrão para instâncias em VHDL: component module_name is
    vhdl_instance_pattern = re.compile(r"component\s+(\w+)\s+is", re.IGNORECASE)

    # Procurar instâncias em Verilog/SystemVerilog
    for match in verilog_instance_pattern.findall(content):
        if match in module_list:
            instances.append(match)

    # Procurar instâncias em VHDL
    for match in vhdl_instance_pattern.findall(content):
        if match in module_list:
            instances.append(match)

    return instances


def build_module_graph(files: list, modules: list[dict]) -> tuple[list, list]:
    """Constrói um grafo de dependência entre os módulos."""
    module_graph = {}
    module_graph_inverse = {}

    module_names = [module[0] for module in modules]

    # Inicializar o grafo direto e inverso com cada módulo
    for module_name, _ in modules:
        module_graph[module_name] = []
        module_graph_inverse[module_name] = []

    for file_path in files:
        with open(
            file_path, "r", errors="ignore"
        ) as f:  # Ignorar erros de decodificação
            content = f.read()

            # Encontrar o nome do módulo atual (módulo onde as instâncias estão sendo feitas)
            current_module_match = re.search(r"module\s+(\w+)", content)
            if not current_module_match:
                continue  # Ignorar arquivos sem um módulo Verilog

            current_module_name = current_module_match.group(1)

            # Encontrar as instâncias dentro deste módulo
            module_instances = find_module_instances(content, module_names)

            # Atualizar o grafo direto (instanciado -> instanciador) e inverso (instanciador -> instanciado)
            for instance in module_instances:
                if instance in module_graph:
                    module_graph[instance].append(current_module_name)
                    module_graph_inverse[current_module_name].append(instance)

    return module_graph, module_graph_inverse


def plot_graph(module_graph: dict, inverse: bool = False) -> None:
    G = nx.DiGraph()

    for node, edges in module_graph.items():
        for edge in edges:
            if inverse:
                G.add_edge(edge, node)
            else:
                G.add_edge(node, edge)

    plt.figure(figsize=(10, 8))

    # Escolher o layout
    pos = nx.spring_layout(G)  # Tente também circular_layout, shell_layout, etc.

    # Desenhar o grafo
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=3000,
        node_color="lightblue",
        font_size=10,
        font_weight="bold",
        edge_color="gray",
        arrows=True,
    )

    plt.title(
        "Module Dependency Graph (Inverse)" if inverse else "Module Dependency Graph"
    )
    plt.show()
