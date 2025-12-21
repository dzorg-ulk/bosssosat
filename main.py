from typing import List, Dict, Set, Optional
from collections import deque
import time


class AdjacencyList:
    def __init__(self):
        self.nodes = {}
        self.root_id = None

    def add_node(self, node_id, data, parent_id=None):
        if node_id in self.nodes:
            print(f"Ошибка: узел {node_id} уже существует")
            return

        node = {
            'id': node_id,
            'data': data,
            'parent_id': parent_id,
            'children': []
        }
        self.nodes[node_id] = node

        if parent_id is None:
            self.root_id = node_id
        elif parent_id in self.nodes:
            self.nodes[parent_id]['children'].append(node)

    def get_children(self, node_id):
        node = self.nodes.get(node_id, {})
        return node.get('children', [])

    def get_parent(self, node_id):
        node = self.nodes.get(node_id)
        if node and node['parent_id']:
            return self.nodes.get(node['parent_id'])
        return None

    def get_descendants(self, node_id):
        descendants = []

        def collect(current_id):
            node = self.nodes.get(current_id)
            if not node:
                return
            for child in node['children']:
                descendants.append(child)
                collect(child['id'])

        collect(node_id)
        return descendants

    def get_ancestors(self, node_id):
        ancestors = []
        current = self.nodes.get(node_id)

        while current and current['parent_id']:
            parent = self.nodes.get(current['parent_id'])
            if parent:
                ancestors.append(parent)
                current = parent
            else:
                break

        return list(reversed(ancestors))

    def print_structure(self):
        if not self.root_id:
            print("Структура пуста")
            return

        def print_node(node_id, level=0):
            node = self.nodes[node_id]
            indent = "  " * level
            print(f"{indent}├─ {node['id']}: {node['data']}")
            for child in node['children']:
                print_node(child['id'], level + 1)

        print("Adjacency List структура:")
        print_node(self.root_id)


class ClosureTable:
    def __init__(self):
        self.nodes = {}
        self.closure = set()  # (ancestor_id, descendant_id, depth)

    def add_node(self, node_id, data, parent_id=None):
        if node_id in self.nodes:
            print(f"Ошибка: узел {node_id} уже существует")
            return

        self.nodes[node_id] = {'id': node_id, 'data': data}
        self.closure.add((node_id, node_id, 0))

        if parent_id and parent_id in self.nodes:
            # Прямой родитель
            self.closure.add((parent_id, node_id, 1))

            # Все предки родителя
            for a, d, depth in list(self.closure):
                if d == parent_id:
                    self.closure.add((a, node_id, depth + 1))

    def get_children(self, node_id):
        children = []
        for a, d, depth in self.closure:
            if a == node_id and depth == 1:
                children.append(self.nodes[d])
        return children

    def get_parent(self, node_id):
        for a, d, depth in self.closure:
            if d == node_id and depth == 1:
                return self.nodes.get(a)
        return None

    def get_descendants(self, node_id):
        descendants = []
        for a, d, depth in self.closure:
            if a == node_id and d != node_id:
                descendants.append((self.nodes[d], depth))
        return sorted(descendants, key=lambda x: x[1])

    def get_ancestors(self, node_id):
        ancestors = []
        for a, d, depth in self.closure:
            if d == node_id and a != node_id:
                ancestors.append((self.nodes[a], depth))
        return sorted(ancestors, key=lambda x: x[1], reverse=True)

    def print_structure(self):
        if not self.nodes:
            print("Структура пуста")
            return

        # Находим корни
        roots = []
        for node_id in self.nodes:
            has_parent = any(d == node_id and depth == 1 for a, d, depth in self.closure)
            if not has_parent:
                roots.append(node_id)

        print("Closure Table структура:")
        for root_id in roots:
            queue = deque([(root_id, 0)])
            visited = set()

            while queue:
                node_id, level = queue.popleft()
                if node_id in visited:
                    continue
                visited.add(node_id)

                node = self.nodes[node_id]
                indent = "  " * level
                print(f"{indent}├─ {node['id']}: {node['data']}")

                children = self.get_children(node_id)
                for child in children:
                    queue.append((child['id'], level + 1))

    def print_closure(self):
        print("\nТаблица связей (ancestor → descendant, depth):")
        for a, d, depth in sorted(self.closure, key=lambda x: (x[0], x[2], x[1])):
            print(f"  {a} → {d} (глубина: {depth})")


def create_example():
    adj = AdjacencyList()

    # Создаем иерархию компании
    adj.add_node(1, "Генеральный директор")
    adj.add_node(2, "Технический директор", 1)
    adj.add_node(3, "Финансовый директор", 1)
    adj.add_node(4, "Руководитель разработки", 2)
    adj.add_node(5, "Руководитель QA", 2)
    adj.add_node(6, "Тимлид Backend", 4)
    adj.add_node(7, "Тимлид Frontend", 4)
    adj.add_node(8, "Старший Backend разработчик", 6)

    return adj


def convert_adj_to_closure(adj):
    closure = ClosureTable()

    def add_recursive(node_id):
        node = adj.nodes[node_id]
        parent_id = node['parent_id']
        closure.add_node(node['id'], node['data'], parent_id)
        for child in node['children']:
            add_recursive(child['id'])

    add_recursive(adj.root_id)
    return closure


def main():
    print("СРАВНЕНИЕ ADJACENCY LIST И CLOSURE TABLE")

    adj_list = create_example()

    print("\n1. Adjacency List:")
    adj_list.print_structure()

    print("\n2. Конвертируем в Closure Table:")
    closure_table = convert_adj_to_closure(adj_list)
    closure_table.print_structure()
    closure_table.print_closure()

    print("ПРОВЕРКА ОПЕРАЦИЙ")

    test_id = 4  # Руководитель разработки

    print(f"\nДля узла {test_id}:")
    print("Дети:", [c['data'] for c in adj_list.get_children(test_id)])
    print("Потомки:", [d['data'] for d in adj_list.get_descendants(test_id)])
    print("Предки:", [a['data'] for a in adj_list.get_ancestors(test_id)])

    print("\nClosure Table для узла 4:")
    print("Дети:", [c['data'] for c in closure_table.get_children(test_id)])
    desc_data = [f"{d['data']} (глубина {depth})" for d, depth in closure_table.get_descendants(test_id)]
    print("Потомки:", desc_data)

    print("СКОРОСТЬ (микросекунды)")

    import timeit

    def test_adj_descendants():
        return len(adj_list.get_descendants(test_id))

    def test_closure_descendants():
        return len(closure_table.get_descendants(test_id))

    adj_time = timeit.timeit(test_adj_descendants, number=1000) * 1000
    clo_time = timeit.timeit(test_closure_descendants, number=1000) * 1000

    print(f"Adjacency List потомки: {adj_time:.1f} мкс")
    print(f"Closure Table потомки:  {clo_time:.1f} мкс")


if __name__ == "__main__":
    main()
