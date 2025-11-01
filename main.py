class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, value):
        if value not in self.nodes:
            self.nodes[value] = []

    def add_edge(self, from_node, to_node):
        if from_node in self.nodes and to_node in self.nodes:
            self.nodes[from_node].append(to_node)


graph = Graph()
for node in ["A", "B", "C", "D"]:
    graph.add_node(node)

graph.add_edge("A", "B")
graph.add_edge("A", "C")
graph.add_edge("B", "D")
graph.add_edge("C", "D")
