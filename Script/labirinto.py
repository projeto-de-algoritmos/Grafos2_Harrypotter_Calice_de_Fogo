import networkx as nx
import random
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Função para gerar um grafo de labirinto com pesos aleatórios
def gerar_labirinto(num_vertices, num_arestas):
    grafo = nx.gnm_random_graph(num_vertices, num_arestas)
    meta = "Meta"
    grafo.add_node(meta)
    mapping = {i: chr(65 + i) for i in range(num_vertices - 1)}  # Mapeamento de números para letras
    mapping[num_vertices - 1] = meta
    grafo = nx.relabel_nodes(grafo, mapping)
    for (u, v) in grafo.edges():
        grafo.edges[u, v]['weight'] = random.randint(1, 10)  # Definindo pesos aleatórios de 1 a 10
    return grafo, meta

# Função para calcular o caminho mais curto a partir de um vértice escolhido
def calcular_caminho():
    node_start = node_start_entry.get().strip().upper()

    if node_start in grafo.nodes and meta in grafo.nodes:
        caminho_mais_curto = nx.shortest_path(grafo, source=node_start, target=meta, weight='weight')
        resultado_label.config(text=f"Caminho mais curto: {caminho_mais_curto}")
    else:
        resultado_label.config(text=f"Nó especificado não encontrado no labirinto.")

# Função para atualizar o labirinto com base na quantidade de vértices
def atualizar_labirinto():
    num_vertices = int(num_vertices_entry.get())
    num_arestas = random.randint(num_vertices, num_vertices * 2)  # Aproximadamente o dobro de vértices para arestas
    global grafo, meta
    grafo, meta = gerar_labirinto(num_vertices, num_arestas)
    pos = nx.spring_layout(grafo, k=0.8)
    ax.clear()
    node_colors = ['skyblue' if node != meta else 'red' for node in grafo.nodes()]
    nx.draw_networkx(grafo, pos, with_labels=True, node_size=800, node_color=node_colors, ax=ax, width=2, edge_color='black', style='dashed')
    nx.draw_networkx_edge_labels(grafo, pos, edge_labels=nx.get_edge_attributes(grafo, 'weight'), ax=ax)
    canvas.draw()

# Interface Gráfica
root = tk.Tk()
root.title("Labirinto com Grafos e Pesos")

frame = ttk.Frame(root)
frame.pack(padx=10, pady=10)

num_vertices_label = ttk.Label(frame, text="Quantidade de Vértices:")
num_vertices_label.pack()

num_vertices_entry = ttk.Entry(frame)
num_vertices_entry.insert(0, "8")  # Valor inicial de 8 vértices
num_vertices_entry.pack()

atualizar_button = ttk.Button(frame, text="Atualizar Labirinto", command=atualizar_labirinto)
atualizar_button.pack()

fig = plt.Figure(figsize=(8, 6))
ax = fig.add_subplot(111)

grafo, meta = gerar_labirinto(8, 12)  # Valor inicial de 8 vértices e 12 arestas

pos = nx.spring_layout(grafo, k=0.8)  # Definindo o valor de k para separar os nós

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
