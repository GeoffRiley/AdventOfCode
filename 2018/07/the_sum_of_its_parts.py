import networkx as nx


def generate_graph(lines):
    graph = nx.DiGraph()
    for line in lines:
        words = line.split()
        graph.add_edge(words[1], words[7])
    return graph


def the_sum_of_its_parts_part_1(inp):
    graph = generate_graph(inp)
    return ''.join(nx.lexicographical_topological_sort(graph))


def the_sum_of_its_parts_part_2(inp):
    graph = generate_graph(inp)
    task_times = []
    tasks = []
    time = 0
    while task_times or graph:
        available_tasks = [t for t in graph if t not in tasks and graph.in_degree(t) == 0]
        if available_tasks and len(task_times) < 5:
            task = min(available_tasks)
            task_times.append(ord(task) - 4)
            tasks.append(task)
        else:
            min_time = min(task_times)
            completed = [tasks[i] for i, v in enumerate(task_times) if v == min_time]
            task_times = [v - min_time for v in task_times if v > min_time]
            tasks = [t for t in tasks if t not in completed]
            time += min_time
            graph.remove_nodes_from(completed)
    return time


if __name__ == '__main__':
    with open('input.txt') as sequence_file:
        sequence_list = sequence_file.read().splitlines(keepends=False)
        print(f'Day 7, part 1: {the_sum_of_its_parts_part_1(sequence_list)}')
        print(f'Day 7, part 2: {the_sum_of_its_parts_part_2(sequence_list)}')
        # Day 7, part 1: EPWCFXKISTZVJHDGNABLQYMORU
        # Day 7, part 2: 952
