import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

# 1. Скачати граф дорожньої мережі для заданого населеного пункту
G = ox.graph_from_place("Skybyn, Ukraine", network_type='drive')

# 2. Візуалізувати граф (вузли та ребра)
fig, ax = ox.plot_graph(G, node_size=30, node_color='white', edge_color='yellow', bgcolor='black')

# 3. Аналіз основних характеристик
num_nodes = G.number_of_nodes()
num_edges = G.number_of_edges()
degrees = dict(G.degree())
average_degree = sum(degrees.values()) / len(degrees)

print(f"Кількість вершин (вузлів): {num_nodes}")
print(f"Кількість ребер: {num_edges}")
print(f"Середній ступінь вершини: {average_degree:.2f}")

# 4. Додатково: розподіл ступенів вершин
plt.figure(figsize=(7, 4))
plt.hist(list(degrees.values()), bins=range(1, max(degrees.values())+2), edgecolor='black', color='skyblue')
plt.title('Розподіл ступеня вершин')
plt.xlabel('Ступінь вершини')
plt.ylabel('Кількість вершин')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
