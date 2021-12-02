from dataclasses import dataclass


@dataclass
class Edge:
    """ Representation of a single edge

    Attributes:
        u: int
            the "from" vertex
        v: int
            the "to" vertex

    Methods:
        __str__
        reversed
    """
    u: int
    v: int

    def __str__(self) -> str:
        return f"{self.u} -> {self.v}"

    def reversed(self) -> 'Edge':
        return Edge(self.v, self.u)
