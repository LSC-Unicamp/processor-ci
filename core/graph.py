"""
This module provides functions for analyzing Verilog, SystemVerilog, and VHDL code to
identify module instances and build dependency graphs. It uses regular expressions to
find instances of modules within files and constructs direct and inverse
dependency graphs. The graphs are then visualized using the NetworkX and Matplotlib libraries.

Functions:

1. `find_module_instances(content: str, module_list: list) -> list`
   Searches for instances of specified modules in the content of Verilog, SystemVerilog,
   or VHDL files.

   Args:
       content (str): The content of the file to search for module instances.
       module_list (list): A list of module names to check for instances.

   Returns:
       list: A list of module instances found in the content that match any of the modules
       in `module_list`.

2. `build_module_graph(files: list, modules: list[dict]) -> tuple[list, list]`
   Builds a dependency graph between modules by analyzing the instances found in the given files.

   Args:
       files (list): A list of file paths to search for module instances.
       modules (list): A list of dictionaries containing module names and their respective
       file paths.

   Returns:
       tuple: A tuple containing two dictionaries:
           - `module_graph`: A dictionary where each module name maps to a list of modules it
            instantiates.
           - `module_graph_inverse`: A dictionary where each module name maps to a list of modules
            that instantiate it.

3. `plot_graph(module_graph: dict, inverse: bool = False) -> None`
   Plots the module dependency graph using the NetworkX and Matplotlib libraries.

   Args:
       module_graph (dict): A dictionary representing the module dependency graph.
       inverse (bool, optional): If True, plots the inverse graph (instantiator -> instantiated).
       Defaults to False.

   Returns:
       None: The graph is displayed using Matplotlib.

This module is useful for analyzing and visualizing the relationships between modules in hardware
description language (HDL) code such as Verilog, SystemVerilog, and VHDL.
"""


import re
import networkx as nx
import matplotlib.pyplot as plt


def find_module_instances(content: str, module_list: list) -> list:
    """
    Finds instances of modules in a Verilog, SystemVerilog, or VHDL file.

    Args:
        content (str): The content of the file to search for module instances.
        module_list (list): A list of module names to check for instances.

    Returns:
        list: A list of module instances found in the content that match any of
        the modules in `module_list`.
    """
    instances = []

    # Pattern for Verilog/SystemVerilog instances: module inst_name(...) or
    # module #( ... ) inst_name(...)
    verilog_instance_pattern = re.compile(
        r'(\w+)\s*(?:#\s*\(.*?\)\s*)?\w+\s*\(.*?\)\s*;', re.DOTALL
    )

    # Pattern for VHDL instances: component module_name is
    vhdl_instance_pattern = re.compile(
        r'component\s+(\w+)\s+is', re.IGNORECASE
    )

    # Search for instances in Verilog/SystemVerilog
    for match in verilog_instance_pattern.findall(content):
        if match in module_list:
            instances.append(match)

    # Search for instances in VHDL
    for match in vhdl_instance_pattern.findall(content):
        if match in module_list:
            instances.append(match)

    return instances


def build_module_graph(files: list, modules: list[dict]) -> tuple[list, list]:
    """
    Builds a dependency graph between modules based on the files and module list.

    Args:
        files (list): A list of file paths to search for module instances.
        modules (list): A list of dictionaries containing module names and their
        respective file paths.

    Returns:
        tuple: A tuple containing two dictionaries:
            - module_graph: A dictionary where each module name maps to a list of
                modules it instantiates.
            - module_graph_inverse: A dictionary where each module name maps to a
                list of modules that instantiate it.
    """
    module_graph = {}
    module_graph_inverse = {}

    module_names = [module[0] for module in modules]

    # Initialize the direct and inverse graphs with each module
    for module_name, _ in modules:
        module_graph[module_name] = []
        module_graph_inverse[module_name] = []

    for file_path in files:
        with open(
            file_path, 'r', errors='ignore', encoding='utf-8'
        ) as f:  # Ignore decoding errors
            content = f.read()

            # Find the current module name (module where instances are being made)
            current_module_match = re.search(r'module\s+(\w+)', content)
            if not current_module_match:
                continue  # Skip files without a Verilog module

            current_module_name = current_module_match.group(1)

            # Find instances within this module
            module_instances = find_module_instances(content, module_names)

            # Update the direct (instantiated -> instantiator) and inverse
            # (instantiator -> instantiated) graphs
            for instance in module_instances:
                if instance in module_graph:
                    module_graph[instance].append(current_module_name)
                    module_graph_inverse[current_module_name].append(instance)

    return module_graph, module_graph_inverse


def plot_graph(module_graph: dict, inverse: bool = False) -> None:
    """
    Plots the module dependency graph using NetworkX and Matplotlib.

    Args:
        module_graph (dict): A dictionary representing the module dependency graph.
        inverse (bool, optional): If True, plots the inverse graph
        (instantiator -> instantiated). Defaults to False.

    Returns:
        None: The graph is displayed using Matplotlib.
    """
    graph = nx.DiGraph()

    for node, edges in module_graph.items():
        for edge in edges:
            if inverse:
                graph.add_edge(edge, node)
            else:
                graph.add_edge(node, edge)

    plt.figure(figsize=(10, 8))

    # Choose the layout
    pos = nx.spring_layout(
        graph
    )  # You can also try circular_layout, shell_layout, etc.

    # Draw the graph
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_size=3000,
        node_color='lightblue',
        font_size=10,
        font_weight='bold',
        edge_color='gray',
        arrows=True,
    )

    plt.title(
        'Module Dependency Graph (Inverse)'
        if inverse
        else 'Module Dependency Graph'
    )
    plt.show()
