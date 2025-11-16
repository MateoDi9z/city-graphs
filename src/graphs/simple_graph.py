from .graph import Graph


class SimpleGraph(Graph):
    vertices = list()
    adjacency_matrix = list()
    directed = False
    weighted = False

    def __init__(self, isDirected=False, weighted=False):
        self.vertices = list()  # Empty vertex list
        self.adjacency_matrix = list()  # Empty adjacency matrix
        self.directed = isDirected  # True if the graph is directed, False otherwise
        self.weighted = weighted

    def add_vertex(self, v):
        if v in self.vertices:
            return

        value = 0 if self.weighted else False
        self.vertices.append(v)

        if len(self.adjacency_matrix) == 0:
            self.adjacency_matrix.append([value])

        for i in range(len(self.adjacency_matrix)):
            self.adjacency_matrix[i].append(value)

        self.adjacency_matrix.append([value] * len(self.vertices))

    def add_edge(self, u, v, w=1):
        if u not in self.vertices:
            self.add_vertex(u)

        if v not in self.vertices:
            self.add_vertex(v)

        value = w if self.weighted else True
        self.adjacency_matrix[self.vertices.index(u)][self.vertices.index(v)] = value

        if not self.directed:
            self.adjacency_matrix[self.vertices.index(v)][self.vertices.index(u)] = (
                value
            )

    def get_adjacency_dict(self) -> dict:
        adjacency_dict = dict()

        for i in range(len(self.vertices)):
            neighbors = []
            for j in range(len(self.adjacency_matrix[i])):
                if self.adjacency_matrix[i][j]:
                    if self.weighted:
                        neighbors.append(
                            (self.vertices[j], self.adjacency_matrix[i][j])
                        )
                    else:
                        neighbors.append(self.vertices[j])

            if not neighbors:
                continue

            adjacency_dict[self.vertices[i]] = neighbors
        return adjacency_dict

    def __repr__(self) -> str:
        if len(self.vertices) == 0:
            return "Grafo vacío"

        result = "\n    |"

        for z in self.vertices:
            result += f" {z[0:3]} |"
        result += "\n"

        for i in range(len(self.adjacency_matrix)):
            t = " | "
            for j in range(len(self.adjacency_matrix[i])):
                x = self.adjacency_matrix[i][j]
                t += str(" X " if x else " . ") + " | "
            result += self.vertices[i][0:3] + t + "\n"
        return result
