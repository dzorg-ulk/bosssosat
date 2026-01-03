from main import *


def bfs(self, start_vertex):
    if start_vertex not in self.adjacency_list:
        return []

    queue = Queue()
    visited = set()

    queue.enqueue(start_vertex)
    visited.add(start_vertex)
    result = []

    while not queue.is_empty():
        vertex = queue.dequeue()
        result.append(vertex)

        if vertex in self.adjacency_list:
            for neighbor, _ in self.adjacency_list[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.enqueue(neighbor)

    return result


def dfs(vertex):
    if vertex == end_vertex:
        return True
    visited.add(vertex)
    for neighbor, _ in self.adjacency_list[vertex]:
        if neighbor not in visited:
            if dfs(neighbor):
                return True
        return False
    return dfs(start_vertex)


def __str__(self):
    result = []
    for vertex in self.adjacency_list:
        neighbors = [f"{neighbor}({weight})" for neighbor, weight in self.adjacency_list[vertex]]
        result.append(f"{vertex}: {', '.join(neighbors)}")
    return "\n".join(result)


if __name__ == "__main__":
    graph = Graph(directed=False)

    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_vertex("C")
    graph.add_vertex("D")
    graph.add_vertex("E")

    graph.add_edge("A", "B", 1)
    graph.add_edge("A", "C", 2)
    graph.add_edge("B", "D", 3)
    graph.add_edge("C", "E", 4)
    graph.add_edge("D", "E", 5)

    print("Структура графа:")
    print(graph)
    print()

    print("Все вершины:", graph.get_vertices())
    print("Все ребра:", graph.get_edges())
    print()

    print("Обход в глубину (DFS) из A:", graph.depth_first_search("A"))
    print("Обход в ширину (BFS) из A:", graph.breadth_first_search("A"))
    print()

    print("Есть ли путь из A в E?", graph.has_path("A", "E"))
    print("Есть ли путь из A в F?", graph.has_path("A", "F"))
    print()

    # Демонстрация с ориентированным графом
    print("ОРИЕНТИРОВАННЫЙ ГРАФ")
    directed_graph = Graph(directed=True)
    directed_graph.add_edge("X", "Y", 1)
    directed_graph.add_edge("Y", "Z", 2)

    print("Структура ориентированного графа:")
    print(directed_graph)
    print("Обход в глубину из X:", directed_graph.depth_first_search("X"))