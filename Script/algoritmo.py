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