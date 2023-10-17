import networkx as nx
import random
import matplotlib.pyplot as plt
import tkinter as tk

from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

canvas2 = None

def gerar_labirinto(num_vertices, num_arestas):
    grafo = nx.gnm_random_graph(num_vertices, num_arestas)
    meta = "Meta"
    grafo.add_node(meta)
    mapping = {i: chr(65 + i) for i in range(num_vertices - 1)}
    mapping[num_vertices - 1] = meta
    grafo = nx.relabel_nodes(grafo, mapping)
    for (u, v) in grafo.edges():
        grafo.edges[u, v]['weight'] = random.randint(1, 10)
    return grafo, meta

def atualizar_labirinto():
    num_vertices = int(num_vertices_entry.get())
    num_arestas = random.randint(num_vertices, num_vertices * 2)
    global grafo, meta
    grafo, meta = gerar_labirinto(num_vertices, num_arestas)
    pos = nx.spring_layout(grafo, k=0.8)
    ax.clear()
    node_colors = ['skyblue' if node != meta else 'red' for node in grafo.nodes()]
    nx.draw_networkx(grafo, pos, with_labels=True, node_size=800, node_color=node_colors, ax=ax, width=2, edge_color='black', style='dashed')
    nx.draw_networkx_edge_labels(grafo, pos, edge_labels=nx.get_edge_attributes(grafo, 'weight'), ax=ax)
    canvas.draw()

def calcular_caminho():
    global canvas2

    node_start = node_start_entry.get().strip().upper()

    if node_start in grafo.nodes and meta in grafo.nodes:
        caminho_mais_curto = dijkstra(grafo, source=node_start, target=meta)
        resultado_label.config(text=f"Caminho mais curto: {caminho_mais_curto}")

        fig2 = plt.Figure(figsize=(8, 3))
        ax2 = fig2.add_subplot(111)
        ax2.clear()
        grafo_caminho = grafo.subgraph(caminho_mais_curto)
        pos = nx.spring_layout(grafo_caminho, k=0.5)
        node_colors = ['skyblue' if node != meta else 'red' for node in grafo_caminho.nodes()]
        nx.draw_networkx(grafo_caminho, pos, with_labels=True, node_size=800, node_color=node_colors, ax=ax2, width=2, edge_color='black', style='dashed')
        nx.draw_networkx_edge_labels(grafo_caminho, pos, edge_labels=nx.get_edge_attributes(grafo_caminho, 'weight'), ax=ax2)

        if canvas2:
            canvas2.get_tk_widget().destroy()

        canvas2 = FigureCanvasTkAgg(fig2, master=frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack()
    else:
        resultado_label.config(text=f"Nó especificado não encontrado no labirinto.")

def dijkstra(grafo, source, target):
    dist = {node: float('inf') for node in grafo.nodes()}
    dist[source] = 0
    visited = set()

    while visited != grafo.nodes():
        min_node = None
        for node in grafo.nodes():
            if node not in visited:
                if min_node is None:
                    min_node = node
                elif dist[node] < dist[min_node]:
                    min_node = node

        if min_node is None:
            break

        visited.add(min_node)
        current_weight = dist[min_node]

        for neighbor in grafo.neighbors(min_node):
            weight = current_weight + grafo[min_node][neighbor]['weight']
            if weight < dist[neighbor]:
                dist[neighbor] = weight

    if target not in dist:
        return []

    path = [target]
    while target != source:
        for neighbor in grafo.neighbors(target):
            if dist[target] == dist[neighbor] + grafo[target][neighbor]['weight']:
                target = neighbor
                path.insert(0, target)
                break

    return path

root = tk.Tk()
root.title("Labirinto com Grafos e Pesos")

frame = ttk.Frame(root)
frame.pack(padx=10, pady=10)

num_vertices_label = ttk.Label(frame, text="Quantidade de Vértices:")
num_vertices_label.pack()

num_vertices_entry = ttk.Entry(frame)
num_vertices_entry.insert(0, "8")
num_vertices_entry.pack()

atualizar_button = ttk.Button(frame, text="Atualizar Labirinto", command=atualizar_labirinto)
atualizar_button.pack()

fig = plt.Figure(figsize=(8, 6))
ax = fig.add_subplot(111)

grafo, meta = gerar_labirinto(8, 12)

pos = nx.spring_layout(grafo, k=0.8)

node_colors = ['skyblue' if node != meta else 'red' for node in grafo.nodes()]
nx.draw_networkx(grafo, pos, with_labels=True, node_size=800, node_color=node_colors, ax=ax, width=2, edge_color='black', style='dashed')

nx.draw_networkx_edge_labels(grafo, pos, edge_labels=nx.get_edge_attributes(grafo, 'weight'), ax=ax)

canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().pack()

node_start_label = ttk.Label(frame, text="Nó de partida:")
node_start_label.pack()

node_start_entry = ttk.Entry(frame)
node_start_entry.pack()

calcular_button = ttk.Button(frame, text="Calcular Caminho Mais Curto", command=calcular_caminho)
calcular_button.pack()

resultado_label = ttk.Label(frame, text="")
resultado_label.pack()

root.mainloop()
