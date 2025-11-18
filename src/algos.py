from collections import deque


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

    if (
        origen not in gw
        or destino not in gw
        or origen in bloqueados
        or destino in bloqueados
    ):
        return float("inf"), []

    dist = {n: float("inf") for n in gw.keys()}
    prev = {}
    visitados = set()
    dist[origen] = 0.0

    while True:
        u = None
        mejor = float("inf")
        for n in dist.keys():
            if n in visitados or n in bloqueados:
                continue
            if dist[n] < mejor:
                mejor = dist[n]
                u = n

        if u is None:
            break
        if u == destino:
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

    camino = []
    cur = destino

    while cur != origen:
        camino.append(cur)
        cur = prev[cur]

    camino.append(origen)
    camino.reverse()
    return float(dist[destino]), camino


def tarjan(g: dict):
    """
    Detecta puentes y puntos de articulación en un grafo no dirigido.
    Retorna: (lista_puentes, lista_articulaciones)
    """

    tiempo = 0
    visitado = set()
    disc = {}   
    bajo = {}  
    padre = {} 
    puentes = []
    articulaciones = set()

    def dfs(u):
        nonlocal tiempo
        visitado.add(u)
        tiempo += 1
        disc[u] = bajo[u] = tiempo
        hijos = 0 

        for v in g[u]:
            if v not in visitado:
                padre[v] = u
                hijos += 1
                dfs(v)
                bajo[u] = min(bajo[u], bajo[v])
                if bajo[v] > disc[u]:
                    puentes.append((u, v))

                if padre.get(u) is not None and bajo[v] >= disc[u]:
                    articulaciones.add(u)

            elif v != padre.get(u):
                bajo[u] = min(bajo[u], disc[v])

        if padre.get(u) is None and hijos > 1:
            articulaciones.add(u)

    for nodo in g.keys():
        if nodo not in visitado:
            dfs(nodo)

    puentes = sorted(puentes)
    articulaciones = sorted(list(articulaciones))

    return puentes, articulaciones
