from collections import deque
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
        return (not self < other) and self != other

    def __le__(self: _C, other: _C) -> bool:
        """Return True if self <= other"""
        return self < other or self == other

    def __ge__(self: _C, other: _C) -> bool:
        """Return True if self >= other"""
        return not self < other


def binary_contains(sequence: Sequence[Comparable], key: Comparable) -> bool:
    """Return True if key is in sequence"""
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
        """Remove and return the top item from the stack"""
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

    # keep going while there is more to explore
    # and the goal has not been reached
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
