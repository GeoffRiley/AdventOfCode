import pytest
from aoc.search import (
    linear_contains,
    binary_contains,
    Stack,
    Queue,
    PriorityQueue,
    Node,
    node_to_path,
    dfs,
    bfs,
    astar,
)


# Linear Contains Tests
@pytest.mark.parametrize(
    "iterable, key, expected",
    [
        ([1, 2, 3], 2, True),
        ([], 1, False),
        ([1, 2, 3], 4, False),
        (["a", "b", "c"], "b", True),
    ],
    ids=["mid_list", "empty_list", "not_found", "string_list"],
)
def test_linear_contains(iterable, key, expected):
    # Act
    result = linear_contains(iterable, key)

    # Assert
    assert result == expected


# Binary Contains Tests
@pytest.mark.parametrize(
    "sequence, key, expected",
    [
        ([1, 2, 3, 4, 5], 3, True),
        ([1, 2, 3, 4, 5], 6, False),
        ([], 1, False),
        ([1], 1, True),
    ],
    ids=["mid_list", "not_found", "empty_list", "single_element"],
)
def test_binary_contains(sequence, key, expected):
    # Act
    result = binary_contains(sequence, key)

    # Assert
    assert result == expected


# Stack Tests
def test_stack_operations():
    # Arrange
    stack = Stack()

    # Assert
    assert stack.empty is True

    # Act
    stack.push(1)
    stack.push(2)

    # Assert
    assert stack.empty is False
    assert stack.pop() == 2
    assert stack.pop() == 1
    assert stack.empty is True


# Queue Tests
def test_queue_operations():
    # Arrange
    queue = Queue()

    # Assert
    assert queue.empty is True

    # Act
    queue.push(1)
    queue.push(2)

    # Assert
    assert queue.empty is False
    assert queue.pop() == 1
    assert queue.pop() == 2
    assert queue.empty is True


# Node Tests
def test_node_creation():
    # Arrange
    parent = Node(1, None)
    node = Node(2, parent, 1.0, 2.0)

    # Assert
    assert node.state == 2
    assert node.parent == parent
    assert node.cost == 1.0
    assert node.heuristic == 2.0


# Node to Path Tests
def test_node_to_path():
    # Arrange
    node3 = Node(3, None)
    node2 = Node(2, node3)
    node1 = Node(1, node2)

    # Act
    path = node_to_path(node1)

    # Assert
    assert path == [3, 2, 1]


# Search Algorithm Tests
def test_dfs():
    # Arrange
    def goal_test(state):
        return state == 5

    def successors(state):
        return [state + 1]

    # Act
    result = dfs(1, goal_test, successors)

    # Assert
    assert result is not None
    assert result.state == 5


def test_bfs():
    # Arrange
    def goal_test(state):
        return state == 5

    def successors(state):
        return [state + 1]

    # Act
    result = bfs(1, goal_test, successors)

    # Assert
    assert result is not None
    assert result.state == 5


def test_astar():
    # Arrange
    def goal_test(state):
        return state == 5

    def successors(state):
        return [state + 1]

    def heuristic(state):
        return 5 - state

    # Act
    result = astar(1, goal_test, successors, heuristic)

    # Assert
    assert result is not None
    assert result.state == 5


# Priority Queue Tests
def test_priority_queue():
    # Arrange
    pq = PriorityQueue()

    # Assert
    assert pq.empty is True

    # Act
    pq.push(3)
    pq.push(1)
    pq.push(2)

    # Assert
    assert pq.empty is False
    assert pq.pop() == 1
    assert pq.pop() == 2
    assert pq.pop() == 3
    assert pq.empty is True
