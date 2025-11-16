from abc import ABC, abstractmethod


class Graph(ABC):
    @abstractmethod
    def add_edge(self, u, v, w=1) -> None:
        """
        Adds an edge between vertices (create if not exist) u and v.

        Args:
            u: The source vertex.
            v: The destination vertex.
        """
        pass

    @abstractmethod
    def add_vertex(self, v) -> None:
        """
        Adds a vertex to the graph.

        Args:
            v: The vertex to add.
        """
        pass

    @abstractmethod
    def get_adjacency_dict(self) -> dict:
        """
        Returns a dictionary representing the adjacency list of the graph.

        Returns:
            A dictionary with vertices as keys and neighbors as values. {node: [neighbors]}
        """
        pass

    # @abstractmethod
    # def remove_vertex(self, v):
    #    """
    #    Removes a vertex from the graph.

    #    Args:
    #        v: The vertex to remove.
    #    """
    #    pass

    # @abstractmethod
    # def remove_edge(self, u, v):
    #     pass

    # @abstractmethod
    # def has_edge(self, u, v):
    #     pass

    # @abstractmethod
    # def add_vertex(self, v):
    #     pass

    # @abstractmethod
    # def remove_vertex(self, v):
    #     pass

    # @abstractmethod
    # def order(self):
    #     pass

    # def get_vertexes(self):
    #     pass

    # @abstractmethod
    # def get_adjacency_list(self, v):
    #     pass
