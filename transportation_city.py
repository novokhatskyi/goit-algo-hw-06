import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

# Скачати граф дорожньої мережі для заданого міста/села
G = ox.graph_from_place("Krasna Luka, Ukraine", network_type='drive')

# Отримуємо координати вузлів
node_positions = {node: (data['x'], data['y']) for node, data in G.nodes(data=True)}

# Візуалізація графа (без підписів для початку)
fig, ax = ox.plot_graph(G, node_size=30, node_color='white', edge_color='yellow', bgcolor='black', show=False, close=False)

# Підписи до вузлів: координати (широта, довгота)
for node, (x, y) in node_positions.items():
    # Тут x — довгота, y — широта
    label = f"{G.nodes[node]['y']:.3f}, {G.nodes[node]['x']:.3f}"
    ax.text(x, y, label, fontsize=7, color='cyan', alpha=0.9)

# Підписи до ребер: відстань у метрах
edge_labels = {}
for u, v, data in G.edges(data=True):
    length = data.get('length', None)
    if length:
        # Відобразимо тільки короткі ребра для уникнення накладення підписів
        edge_labels[(u, v)] = f"{int(length)}м"

# Визначаємо позиції вузлів для NetworkX
pos = {node: (data['x'], data['y']) for node, data in G.nodes(data=True)}

# Додаємо підписи до ребер
nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels, font_size=6, font_color='orange', ax=ax, label_pos=0.5)

plt.title("Транспортна мережа Krasna Luka (координати вузлів і відстані ребер)")
plt.tight_layout()
plt.show()