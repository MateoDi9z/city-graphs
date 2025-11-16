from collections import deque

# -----------------------------
# Algoritmos
# -----------------------------


def componentes_conexos(g: dict):
    vistos = set()
    comps = []

    for start in sorted(g.keys()):
        if start in vistos:
            continue

        q = deque([start])
        vistos.add(start)
        comp = []

        while q:
            u = q.popleft()
            comp.append(u)
            for v in g[u]:
                if v not in vistos:
                    vistos.add(v)
                    q.append(v)

        comps.append(sorted(comp))
    return comps


def orden_fallos(g: dict):
    grados = []

    for u in sorted(g.keys()):
        grados.append((u, len(g[u])))

    grados.sort(key=lambda x: (x[1], x[0]))
    return grados


def dijkstra(gw: dict, origen: str, destino: str, bloqueados: set | None = None):
    """
    Dijkstra
    gw: diccionario de adyacencia ponderado no dirigido: {u: [(v, peso), ...]}
    origen, destino: nodos
    bloqueados: conjunto de nodos a ignorar
    Retorna: (distancia, camino)
    """

    if bloqueados is None:
        bloqueados = set()

    # Validaciones iniciales
    if (
        origen not in gw
        or destino not in gw
        or origen in bloqueados
        or destino in bloqueados
    ):
        return float("inf"), []

    # Distancia inicial infinito
    dist = {n: float("inf") for n in gw.keys()}
    prev = {}
    visitados = set()
    dist[origen] = 0.0

    while True:
        # Seleccionar el nodo no visitado con menor distancia
        u = None
        mejor = float("inf")
        for n in dist.keys():
            if n in visitados or n in bloqueados:
                continue
            if dist[n] < mejor:
                mejor = dist[n]
                u = n

        if u is None:
            # No queda nodo alcanzable
            break
        if u == destino:
            # Ya tenemos la distancia mínima al destino
            break

        visitados.add(u)

        for v, w in gw[u]:
            if v in visitados or v in bloqueados:
                continue
            nd = dist[u] + float(w)
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u

    if dist[destino] == float("inf"):
        return float("inf"), []

    # Reconstruir camino
    camino = []
    cur = destino

    while cur != origen:
        camino.append(cur)
        cur = prev[cur]

    camino.append(origen)
    camino.reverse()
    return float(dist[destino]), camino
