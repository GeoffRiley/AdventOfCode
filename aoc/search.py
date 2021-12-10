from collections import deque
from heapq import heappush, heappop
from typing import (TypeVar, Iterable, Sequence, Generic, List, Callable, Set,
                    Deque, Dict, Any, Optional, Union, Protocol, )

_T = TypeVar("_T")
_C = TypeVar("_C", bound="Comparable")
_N = TypeVar("_N", bound="Node")


def linear_contains(iterable: Iterable[_T], key: _T) -> bool:
    for item in iterable:
        if item == key:
            return True
    return False


class Comparable(Protocol):
    def __eq__(self, other: Any) -> bool:
        ...

    def __lt__(self, other: Any) -> bool:
        ...

    def __gt__(self: _C, other: _C) -> bool:
        return (not self < other) and self != other

    def __le__(self: _C, other: _C) -> bool:
        return self < other or self == other

    def __ge__(self: _C, other: _C) -> bool:
        return not self < other


def binary_contains(sequence: Sequence[Comparable], key: Comparable) -> bool:
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


class Stack(Generic[_T]):
    def __init__(self) -> None:
        self._container: List[_T] = []

    @property
    def empty(self) -> bool:
        return not self._container

    def push(self, item: _T) -> None:
        self._container.append(item)

    def pop(self) -> _T:
        return self._container.pop()

    def clear(self) -> None:
        self._container.clear()

    def __repr__(self) -> str:
        return repr(self._container)


class Node(Generic[_T]):
    def __init__(
            self, state: _T, parent: Optional[_N], cost: float = 0.0, heuristic: float = 0.0
    ) -> None:
        self.state: _T = state
        self.parent: Optional[_N] = parent
        self.cost: float = cost
        self.heuristic: float = heuristic

    def __lt__(self, other: _N) -> bool:
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


def node_to_path(node: Node[_T]) -> List[_T]:
    path: List[_T] = [node.state]
    while node.parent is not None:
        node = node.parent
        path.append(node.state)
    path.reverse()
    return path


class Queue(Generic[_T]):
    def __init__(self) -> None:
        self._container: Deque[_T] = deque()

    @property
    def empty(self) -> bool:
        return not self._container

    def push(self, item: _T) -> None:
        self._container.append(item)

    def pop(self) -> _T:
        return self._container.popleft()

    def clear(self) -> None:
        self._container.clear()

    def __repr__(self) -> str:
        return repr(self._container)


def dfs(
        initial: _T,
        goal_test: Callable[[_T], bool],
        successors: Callable[[_T], List[_T]]
) -> Optional[Node[_T]]:
    """ Depth first search """
    frontier: Stack[Node[_T]] = Stack()
    return _frontier_search(frontier, initial, goal_test, successors)


def bfs(
        initial: _T,
        goal_test: Callable[[_T], bool],
        successors: Callable[[_T], List[_T]]
) -> Optional[Node[_T]]:
    """ Breadth first search """
    frontier: Queue[Node[_T]] = Queue()
    return _frontier_search(frontier, initial, goal_test, successors)


def _frontier_search(
        frontier: Union[Stack[Node[_T]], Queue[Node[_T]]],
        initial: _T,
        goal_test: Callable[[_T], bool],
        successors: Callable[[_T], List[_T]]
) -> Optional[Node[_T]]:
    """ Main body for dfs and bfs

    The type of `frontier` dictates how the algorithm progresses.
    """
    frontier.push(Node(initial, None))
    explored: Set[_T] = {initial}
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
    def __init__(self) -> None:
        self._container: List[_T] = []

    @property
    def empty(self) -> bool:
        return not self._container  # not is true for empty container

    def push(self, item: _T) -> None:
        heappush(self._container, item)  # in by priority

    def pop(self) -> _T:
        return heappop(self._container)  # out by priority

    def __repr__(self) -> str:
        return repr(self._container)


def astar(
        initial: _T,
        goal_test: Callable[[_T], bool],
        successors: Callable[[_T], List[_T]],
        heuristic: Callable[[_T], float],
) -> Optional[Node[_T]]:
    """ A* search """
    frontier: PriorityQueue[Node[_T]] = PriorityQueue()
    frontier.push(Node(initial, None, 0.0, heuristic(initial)))
    explored: Dict[_T, float] = {initial: 0.0}
    while not frontier.empty:
        current_node: Node[_T] = frontier.pop()
        current_state: _T = current_node.state
        if goal_test(current_state):
            return current_node
        for child in successors(current_state):
            new_cost: float = current_node.cost + 1
            if child not in explored or explored[child] > new_cost:
                explored[child] = new_cost
                frontier.push(Node(child, current_node, new_cost, heuristic(child)))
    return None
