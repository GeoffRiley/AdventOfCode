import itertools
from collections import deque
from functools import lru_cache
from heapq import heappush, heappop
from typing import (
    TypeVar,
    Iterable,
    Sequence,
    Generic,
    List,
    Callable,
    Set,
    Deque,
    Dict,
    Any,
    Optional,
    Union,
    Protocol,
)

_T = TypeVar("_T")
_C = TypeVar("_C", bound="Comparable")
_N = TypeVar("_N", bound="Node")


def linear_contains(iterable: Iterable[_T], key: _T) -> bool:
    """Return True if key is in iterable"""
    return key in iterable


class Comparable(Protocol):
    """Protocol for comparable objects"""

    def __eq__(self, other: Any) -> bool:
        """Return True if self == other"""
        ...

    def __lt__(self, other: Any) -> bool:
        """Return True if self < other"""
        ...

    def __gt__(self: _C, other: _C) -> bool:
        """Return True if self > other"""
        return other < self

    def __le__(self: _C, other: _C) -> bool:
        """Return True if self <= other"""
        return self < other or self == other

    def __ge__(self: _C, other: _C) -> bool:
        """Return True if self >= other"""
        return not self < other


def binary_contains(
        sequence: Sequence[Comparable],
        key: Comparable,
        check_sorted: bool = False
) -> bool:
    """
    Return True if key is in sequence using binary search.

    The input sequence must be sorted in ascending order.

    If check_sorted is True, a ValueError is raised if the sequence is not sorted.
    """
    if check_sorted and any(sequence[i] > sequence[i + 1] for i in range(len(sequence) - 1)):
        raise ValueError("Input sequence must be sorted in ascending order for binary search.")

    low: int = 0
    high: int = len(sequence) - 1
    while low <= high:
        mid: int = (low + high) // 2
        if sequence[mid] < key:
            low = mid + 1
        elif sequence[mid] > key:
            high = mid - 1
        else:
            return True
    return False


class StackEmptyError(Exception):
    """Raised when attempting to pop from an empty stack."""
    pass

class Stack(Generic[_T]):
    """LIFO stack"""

    def __init__(self) -> None:
        """Create a new stack"""
        self._container: List[_T] = []

    @property
    def empty(self) -> bool:
        """Return True if the stack is empty"""
        return not self._container

    def push(self, item: _T) -> None:
        """Add an item to the top of the stack"""
        self._container.append(item)

    def pop(self) -> _T:
        """
        Remove and return the top item from the stack.

        Raises:
            StackEmptyError: If the stack is empty.
        """
        if self.empty:
            raise StackEmptyError("Cannot pop from an empty stack.")
        return self._container.pop()

    def clear(self) -> None:
        """Remove all items from the stack"""
        self._container.clear()

    def __repr__(self) -> str:
        """Return a string representation of the stack"""
        return repr(self._container)


class Node(Generic[_T]):
    """A node in a search tree"""

    def __init__(
        self, state: _T, parent: Optional[_N], cost: float = 0.0, heuristic: float = 0.0
    ) -> None:
        """Create a search tree node"""
        self.state: _T = state
        self.parent: Optional[_N] = parent
        self.cost: float = cost
        self.heuristic: float = heuristic

    def __lt__(self, other: _N) -> bool:
        """Return True if self < other"""
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


def node_to_path(node: Node[_T]) -> List[_T]:
    """Return the sequence of states to go from the root to this node"""
    path: List[_T] = [node.state]
    while node.parent is not None:
        node = node.parent
        path.append(node.state)
    path.reverse()
    return path


class Queue(Generic[_T]):
    """FIFO queue"""

    def __init__(self) -> None:
        """Create a new queue"""
        self._container: Deque[_T] = deque()

    @property
    def empty(self) -> bool:
        """Return True if the queue is empty"""
        return not self._container

    def push(self, item: _T) -> None:
        """Add an item to the end of the queue"""
        self._container.append(item)

    def pop(self) -> _T:
        """Remove and return the first item from the queue"""
        return self._container.popleft()

    def clear(self) -> None:
        """Remove all items from the queue"""
        self._container.clear()

    def __repr__(self) -> str:
        """Return a string representation of the queue"""
        return repr(self._container)


def dfs(
    initial: _T, goal_test: Callable[[_T], bool], successors: Callable[[_T], List[_T]]
) -> Optional[Node[_T]]:
    """Depth first search"""
    frontier: Stack[Node[_T]] = Stack()
    return _frontier_search(frontier, initial, goal_test, successors)


def bfs(
    initial: _T, goal_test: Callable[[_T], bool], successors: Callable[[_T], List[_T]]
) -> Optional[Node[_T]]:
    """Breadth first search"""
    frontier: Queue[Node[_T]] = Queue()
    return _frontier_search(frontier, initial, goal_test, successors)


def _frontier_search(
    frontier: Union[Stack[Node[_T]], Queue[Node[_T]]],
    initial: _T,
    goal_test: Callable[[_T], bool],
    successors: Callable[[_T], List[_T]],
) -> Optional[Node[_T]]:
    """Main body for dfs and bfs

    The type of `frontier` dictates how the algorithm progresses.
    """
    # frontier: Stack[Node[_T]] = Stack()   # for dfs
    # frontier: Queue[Node[_T]] = Queue()   # for bfs
    frontier.push(Node(initial, None))
    explored: Set[_T] = {initial}

    # keep going while there is more to explore
    # and the goal has not been reached
    while not frontier.empty:
        current_node: Node[_T] = frontier.pop()
        current_state: _T = current_node.state
        if goal_test(current_state):
            return current_node
        for child in successors(current_state):
            if child in explored:
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))
    return None


class PriorityQueue(Generic[_T]):
    """Priority queue"""

    def __init__(self) -> None:
        """Create a new priority queue"""
        self._container: List[_T] = []

    @property
    def empty(self) -> bool:
        """Return True if the queue is empty"""
        return not self._container  # not is true for empty container

    def push(self, item: _T) -> None:
        """Add an item to the queue"""
        heappush(self._container, item)  # in by priority

    def pop(self) -> _T:
        """Remove and return the first item from the queue"""
        return heappop(self._container)  # out by priority

    def __repr__(self) -> str:
        """Return a string representation of the queue"""
        return repr(self._container)


def astar(
    initial: _T,
    goal_test: Callable[[_T], bool],
    successors: Callable[[_T], List[_T]],
    heuristic: Callable[[_T], float],
        cost: Callable[[_T, _T], float] = None,
) -> Optional[Node[_T]]:
    """A* search"""
    # 1. Create a priority queue
    # 2. Add the initial node to the queue
    # 3. Create a set to store the explored nodes
    # 4. Loop until the queue is empty
    #     a. Pop the node with the lowest cost
    #     b. If the node is the goal, return it
    #     c. For each child of the node
    #         i. Calculate the cost to the child
    #         ii. If the child is not explored or the new cost is lower
    #             1. Add the child to the explored set
    #             2. Add the child to the queue

    frontier: PriorityQueue[Node[_T]] = PriorityQueue()
    frontier.push(Node(initial, None, 0.0, heuristic(initial)))
    explored: Dict[_T, float] = {initial: 0.0}
    if cost is None:
        cost = lambda a, b: 1

    # keep going while there is more to explore
    # and the goal has not been reached
    while not frontier.empty:
        current_node: Node[_T] = frontier.pop()
        current_state: _T = current_node.state
        if goal_test(current_state):
            return current_node
        for child in successors(current_state):
            step_cost = cost(current_state, child)
            new_cost: float = current_node.cost + step_cost
            if child not in explored or explored[child] > new_cost:
                explored[child] = new_cost
                frontier.push(Node(child, current_node, new_cost, heuristic(child)))
    return None


def all_paths(
        start: _T,
        goal: _T,
        successors: Callable[[_T], List[_T]],
) -> List[List[_T]]:
    """
    Find all paths from start to goal in a graph.

    Args:
        start: The starting node.
        goal: The goal node.
        successors: Function that returns a list of successors for a node.

    Returns:
        A list of paths, where each path is a list of nodes from start to goal.
    """

    @lru_cache(maxsize=None)
    def _all_paths(
            current: _T,
            goal: _T,
            path: tuple,
            visited: frozenset,
    ) -> List[List[_T]]:
        if current == goal:
            return [list(path + (current,))]
        paths = []
        for neighbor in successors(current):
            if neighbor not in visited:
                new_paths = _all_paths(
                    neighbor,
                    goal,
                    path + (current,),
                    visited | frozenset([current]),
                )
                paths.extend(new_paths)
        return paths

    return _all_paths(start, goal, tuple(), frozenset())


# Implement Karp's algorithm
def karp(edges: dict[str, list[tuple[str, float]]]) -> list[str]:
    """
    Find the minimum mean cycle in a directed graph using Karp's algorithm.

    Args:
        edges: dict mapping node to list of (neighbor, weight) tuples

    Returns:
        The minimum mean cycle as a list of nodes, or an empty list if no cycle exists.
    """
    nodes = list(edges.keys())
    n = len(nodes)
    node_idx = {node: i for i, node in enumerate(nodes)}

    # dp[k][v] = min cost to reach v in exactly k steps
    dp = [[float('inf')] * n for _ in range(n + 1)]
    parent = [[-1] * n for _ in range(n + 1)]

    # Initialize: cost to reach each node in 0 steps is 0
    for v in range(n):
        dp[0][v] = 0

    # Dynamic programming: for each k steps, update costs
    for k, v in itertools.product(range(1, n + 1), range(n)):
        for u, w in edges.get(nodes[v], []):
            u_idx = node_idx[u]
            if dp[k - 1][u_idx] + w < dp[k][v]:
                dp[k][v] = dp[k - 1][u_idx] + w
                parent[k][v] = u_idx

    # Find minimum mean cycle
    min_mean = float('inf')
    end_node = -1
    start_k = -1

    for v in range(n):
        max_mean = -float('inf')
        for k in range(n):
            if dp[n][v] < float('inf') and dp[k][v] < float('inf') and n != k:
                mean = (dp[n][v] - dp[k][v]) / (n - k)
                if mean < min_mean:
                    min_mean = mean
                    end_node = v
                    start_k = k

    # Reconstruct the cycle
    if end_node == -1:
        return []

    # Backtrack to get the cycle
    cycle = []
    visited = set()
    k = n
    v = end_node
    for _ in range(n):
        v = parent[k][v]
        k -= 1
        if v in visited or v == -1:
            break
        visited.add(v)
        cycle.append(nodes[v])
    cycle.reverse()
    return cycle
