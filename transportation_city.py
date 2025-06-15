from rich import print
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from bfs_dfs import bfs_iterative, dfs_iterative, dijkstra, print_table

# 1. Скачати граф дорожньої мережі для заданого населеного пункту
G = ox.graph_from_place("Skybyn, Ukraine", network_type='drive')

# 2. Візуалізувати граф (вузли та ребра)
fig, ax = ox.plot_graph(G, node_size=40, node_color='white', edge_color='yellow', bgcolor='black', show=False, close=False)

# Додаємо імена вузлів (ідентифікатори)
for node, data in G.nodes(data=True):
    ax.text(data['x'], data['y'], str(node), fontsize=6, color='white', alpha=0.7)

# Додаємо підписи до ребер
for u, v, data in G.edges(data=True):
    if 'length' in data:
        # Координати для підпису (середина ребра)
        x1, y1 = G.nodes[u]['x'], G.nodes[u]['y']
        x2, y2 = G.nodes[v]['x'], G.nodes[v]['y']
        xm, ym = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(xm, ym, f"{data['length']:.0f}", fontsize=6, color='red', alpha=0.7)

# 3. Аналіз основних характеристик
num_nodes = G.number_of_nodes()
num_edges = G.number_of_edges()
degrees = dict(G.degree())
average_degree = sum(degrees.values()) / len(degrees)

print(f"Кількість вершин (вузлів): {num_nodes}")
print(f"Кількість ребер: {num_edges}")
print(f"Середній ступінь вершини: {average_degree:.2f}")

# 4. Довжина ребер
for u, v, data in list(G.edges(data=True))[:10]:  # Можна взяти більше для прикладу
    if 'length' in data:
        print(f"{u} -> {v}, length = {data['length']:.1f} м, name = {data.get('name', 'N/A')}")
    else:
        print(f"{u} -> {v}, length = N/A")

# 5. Координати вузлів
print("\nКоординати перших 10 вузлів:")
for node, data in list(G.nodes(data=True))[:10]:
    print(f"Node: {node}, lat: {data['y']}, lon: {data['x']}")

# 6. DFS
source = 2390301685
dfs_order = dfs_iterative(G, source)
print("[bold green]DFS порядок обходу:[/bold green]")
# dfs_tree = nx.dfs_tree(G, source=source)
# print("[bold green]Кількість ребер у дереві DFS:[/bold green]", len(list(dfs_tree.edges())))

# 7. BFS
bfs_order = bfs_iterative(G, source)
print("\n[bold green]BFS порядок обходу:[/bold green]", bfs_order)
# bfs_tree = nx.bfs_tree(G, source=source)
# print("[bold yellow]Кількість ребер у дереві BFS:[/bold yellow]", len(list(bfs_tree.edges())))

# Не заледно від вибору вершини кількість ребер завжди однакова, навіть якщо вибрати інше місто. 
# Справа в тому що граф звязаний і починаю з одного і того ж source/
# Доречі я спеціально виводжу кількість ребер а не іх перелік. 
# Бо взаледності від міста іх жуєе багато. Можу сказати що перелік відрізняється

# Алгоритм Дейкстри (вручну) Робюлю копію графа, бос алгоритм спиймає мій граф як словник, а він таким не являєтсья.
def build_simple_graph(nx_graph):
    simple_graph = {}
    for u, v, data in nx_graph.edges(data=True):
        length = data.get("length", 1)
        if u not in simple_graph:
            simple_graph[u] = {}
        if v not in simple_graph:
            simple_graph[v] = {}
        # Додаємо ребро з вагою (мінімальну вагу, якщо MultiGraph)
        simple_graph[u][v] = min(length, simple_graph[u].get(v, float('inf')))
    return simple_graph

graph_dict = build_simple_graph(G)
distance = dijkstra(graph_dict, source)
print_table(distance, visited=distance.keys())  # або visited=[], якщо хочеш тільки відстані

# shortest_paths = nx.single_source_dijkstra_path(G, source=source, cutoff=None, weight="length")
# shortest_path_lengths = nx.single_source_dijkstra_path_length(G, source=source, weight="length")

# print(shortest_paths)
# print("Вершина\t\tДовжина шляху, м")
# for node, dist in shortest_path_lengths.items():
#     print(f"{node}\t{dist:.1f}")


# 8. Додатково: розподіл ступенів вершин
plt.figure(figsize=(7, 4))
plt.hist(list(degrees.values()), bins=range(1, max(degrees.values())+2), edgecolor='black', color='skyblue')
plt.title('Розподіл ступеня вершин')
plt.xlabel('Ступінь вершини')
plt.ylabel('Кількість вершин')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()