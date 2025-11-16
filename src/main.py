"""
Graph analysis module for Buenos Aires city networks.
Students must implement all functions marked with TODO.
"""

# -----------------------------
# Graph loading
# -----------------------------
from src.graphs.simple_graph import SimpleGraph
from src.output import (
    format_camino_minimo,
    format_componentes_conexos,
    format_orden_fallos,
    format_plantas_asignadas,
    format_puentes_y_articulaciones,
    format_ruta_recoleccion,
    format_simulacion_corte,
)


def load_graph(path):
    """
    Load a simple graph from a file.

    Args:
        path: File path

    Returns:
        Adjacency dictionary {node: [neighbors]}
    """

    graph = SimpleGraph(isDirected=False)

    with open(path, "r") as file:
        for line in file:
            if not line or line[0] == "#":
                continue

            clean_line = line.strip()
            if not clean_line:
                continue

            from_node, to_node = tuple(clean_line.split(" "))
            graph.add_edge(from_node, to_node)

    return graph.get_adjacency_dict()


def load_weighted_graph(path):
    """
    Load a weighted graph from a file.

    Args:
        path: File path

    Returns:
        Adjacency dictionary {node: [(neighbor, weight), ...]}
    """

    graph = SimpleGraph(isDirected=False, weighted=True)

    with open(path, "r") as file:
        for line in file:
            if not line or line[0] == "#":
                continue

            clean_line = line.strip()
            if not clean_line:
                continue

            from_node, to_node, weight = tuple(clean_line.split(" "))
            graph.add_edge(from_node, to_node, int(weight))

    return graph.get_adjacency_dict()


def process_queries(queries_file, output_file, electric_graph, road_graph, water_graph):
    """
    Process queries from file and generate output.

    Args:
        queries_file: Path to queries file
        output_file: Path to output file
        electric_graph: Electric network graph
        road_graph: Road network graph
        water_graph: Water network graph
    """
    # TODO: Implement
    return dict()
