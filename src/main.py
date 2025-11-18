"""
Graph analysis module for Buenos Aires city networks.
Students must implement all functions marked with TODO.
"""

# -----------------------------
# Graph loading
# -----------------------------
from src.graphs.simple_graph import SimpleGraph
from src.algos import (
    componentes_conexos,
    orden_fallos,
    dijkstra,
    tarjan,
)
from src.output import (
    format_camino_minimo,
    format_componentes_conexos,
    format_orden_fallos,
    format_plantas_asignadas,
    format_puentes_y_articulaciones,
    format_ruta_recoleccion,
    format_simulacion_corte,
)


# ===============================================================
# LOADERS
# ===============================================================

def load_graph(path):
    """Load an unweighted simple graph."""
    graph = SimpleGraph(isDirected=False)

    with open(path, "r") as file:
        for line in file:
            if not line or line[0] == "#":
                continue

            line = line.strip()
            if not line:
                continue

            u, v = line.split(" ")
            graph.add_edge(u, v)

    return graph.get_adjacency_dict()


def load_weighted_graph(path):
    """Load weighted graph."""
    graph = SimpleGraph(isDirected=False, weighted=True)

    with open(path, "r") as file:
        for line in file:
            if not line or line[0] == "#":
                continue

            line = line.strip()
            if not line:
                continue

            u, v, w = line.split(" ")
            graph.add_edge(u, v, int(w))

    return graph.get_adjacency_dict()


# ===============================================================
# BFS helper for PLANTAS_ASIGNADAS
# ===============================================================

def distancia_bfs(grafo, origen):
    """Return BFS distances in an unweighted graph."""
    from collections import deque
    dist = {n: float("inf") for n in grafo}
    dist[origen] = 0
    q = deque([origen])

    while q:
        u = q.popleft()
        for v in grafo[u]:
            if dist[v] == float("inf"):
                dist[v] = dist[u] + 1
                q.append(v)

    return dist


# ===============================================================
# MAIN QUERY PROCESSOR
# ===============================================================

def process_queries(queries_file, output_file, electric_graph, road_graph, water_graph):

    print(">> Entrando a process_queries")

    graphs = {
        "ELECTRICA": electric_graph,
        "VIAL": road_graph,
        "HIDRICA": water_graph,
    }

    with open(queries_file, "r", encoding="utf-8") as qf, open(output_file, "w", encoding="utf-8") as out:
        for line in qf:
            line = line.strip()

            # ignorar comentarios y líneas vacías
            if not line or line.startswith("#"):
                continue

            parts = line.split()
            comando = parts[0].upper()

            # ===============================================================
            # COMPONENTES CONEXOS
            # ===============================================================
            if comando in ("CONEXOS", "COMPONENTES_CONEXOS"):
                tipo = parts[1].upper()
                g = graphs[tipo]
                comps = componentes_conexos(g)
                out.write(format_componentes_conexos(comps))
                out.write("\n")

            # ===============================================================
            # ORDEN DE FALLOS
            # ===============================================================
            elif comando == "ORDEN_FALLOS":
                tipo = parts[1].upper()
                g = graphs[tipo]
                fallos = orden_fallos(g)
                out.write(format_orden_fallos(fallos))
                out.write("\n")

            # ===============================================================
            # CAMINO MINIMO (Dijkstra sobre la red VIAL)
            # ===============================================================
            elif comando == "CAMINO_MINIMO":
                origen = parts[1]
                destino = parts[2]
                dist, camino = dijkstra(road_graph, origen, destino)
                out.write(format_camino_minimo(origen, destino, dist, camino))
                out.write("\n")

            # ===============================================================
            # CAMINO_MINIMO_SIMULAR_CORTE
            # ===============================================================
            elif comando == "CAMINO_MINIMO_SIMULAR_CORTE":
                # Formato: {A,B,C} origen destino
                corte_str = parts[1].strip("{}")
                bloqueados = set(corte_str.split(",")) if corte_str else set()

                origen = parts[2]
                destino = parts[3]

                dist, camino = dijkstra(road_graph, origen, destino, bloqueados=bloqueados)
                out.write(format_simulacion_corte(origen, destino, bloqueados, dist, camino))
                out.write("\n")

            # ===============================================================
            # CAMINO_RECOLECCION_BASURA
            # ===============================================================
            elif comando == "CAMINO_RECOLECCION_BASURA":
                g = road_graph

                # DFS ordenado lexicográficamente
                visit = set()
                camino = []

                def dfs(u):
                    visit.add(u)
                    camino.append(u)
                    vecinos = sorted([v for v, _ in g[u]])
                    for v in vecinos:
                        if v not in visit:
                            dfs(v)

                start = sorted(g.keys())[0]   # primer barrio alfabético
                dfs(start)

                out.write(format_ruta_recoleccion(camino))
                out.write("\n")

            # ===============================================================
            # PLANTAS_ASIGNADAS (multi-source BFS)
            # ===============================================================
            elif comando == "PLANTAS_ASIGNADAS":
                plantas = parts[1:]
                g = water_graph

                from collections import deque
                dist = {n: float("inf") for n in g}
                asign = {}
                q = deque()

                # inicializar BFS con múltiples plantas
                for p in plantas:
                    dist[p] = 0
                    asign[p] = p
                    q.append(p)

                # BFS expandiendo por capas
                while q:
                    u = q.popleft()
                    for v in g[u]:
                        if dist[v] > dist[u] + 1:
                            dist[v] = dist[u] + 1
                            asign[v] = asign[u]
                            q.append(v)
                        elif dist[v] == dist[u] + 1:
                            asign[v] = min(asign[v], asign[u])

                out.write(format_plantas_asignadas(plantas, asign))
                out.write("\n")

            # ===============================================================
            # PUENTES Y ARTICULACIONES
            # ===============================================================
            elif comando == "PUENTES_Y_ARTICULACIONES":
                g = water_graph

                # tarjan devuelve → (puentes, articulaciones)
                puentes, articulaciones = tarjan(g)

                # formatter espera → (articulaciones, puentes)
                out.write(format_puentes_y_articulaciones(articulaciones, puentes))
                out.write("\n")

            # ===============================================================
            # COMANDO DESCONOCIDO
            # ===============================================================
            else:
                out.write(f"ERROR: comando desconocido → {line}\n\n")

    return {"status": "OK", "message": "Consultas procesadas correctamente"}
