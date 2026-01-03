class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None

    def is_empty(self):
        return len(self.items) == 0

    def __len__(self):
        return len(self.items)


class Graph:
    def __init__(self, directed=False):
        self.adjacency_list = {}
        self.directed = directed

    def add_vertex(self, vertex):
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []

    def add_edge(self, vertex1, vertex2, weight=1):
        if vertex1 not in self.adjacency_list:
            self.add_vertex(vertex1)
        if vertex2 not in self.adjacency_list:
            self.add_vertex(vertex2)

        if not any(neighbor == vertex2 for neighbor, _ in self.adjacency_list[vertex1]):
            self.adjacency_list[vertex1].append((vertex2, weight))

        if not self.directed and not any(neighbor == vertex1 for neighbor, _ in self.adjacency_list[vertex2]):
            self.adjacency_list[vertex2].append((vertex1, weight))

    def get_vertices(self):
        return list(self.adjacency_list.keys())

    def get_edges(self):
        edges = []
        for vertex in self.adjacency_list:
            for neighbor, weight in self.adjacency_list[vertex]:
                if not self.directed:
                    if not any(v == neighbor and n == vertex and w == weight for v, n, w in edges):
                        edges.append((vertex, neighbor, weight))
                else:
                    edges.append((vertex, neighbor, weight))
        return edges

    def breadth_first_search(self, start_vertex):
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

            for neighbor, _ in self.adjacency_list.get(vertex, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.enqueue(neighbor)

        return result

    def depth_first_search(self, start_vertex):
        if start_vertex not in self.adjacency_list:
            return []

        visited = set()
        result = []

        def dfs_recursive(vertex):
            visited.add(vertex)
            result.append(vertex)
            for neighbor, _ in self.adjacency_list.get(vertex, []):
                if neighbor not in visited:
                    dfs_recursive(neighbor)

        dfs_recursive(start_vertex)
        return result

    def has_path(self, start_vertex, end_vertex):
        if start_vertex not in self.adjacency_list or end_vertex not in self.adjacency_list:
            return False

        visited = set()

        def dfs(vertex):
            if vertex == end_vertex:
                return True
            visited.add(vertex)
            for neighbor, _ in self.adjacency_list.get(vertex, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
            return False

        return dfs(start_vertex)

    def __str__(self):
        if not self.adjacency_list:
            return "Граф пуст"

        result = []
        for vertex in sorted(self.adjacency_list.keys()):
            neighbors = [f"{neighbor}({weight})" for neighbor, weight in self.adjacency_list[vertex]]
            result.append(f"{vertex}: {', '.join(neighbors)}" if neighbors else f"{vertex}: нет соседей")
        return "\n".join(result)