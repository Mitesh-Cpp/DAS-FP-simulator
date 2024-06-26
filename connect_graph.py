import random
from peer import peer

def connect_graph(peers):
    n = len(peers)
    network_graph = [[False] * n for _ in range(n)]  # Initialize an empty network graph

    def show_graph(peers, network_graph):
        for i, row in enumerate(network_graph):
            print(f"Node {peers[i].id}: Connected to {', '.join(map(str, peers[i].connected_nodes))}")

    def is_connected(graph, start, visited):
        stack = [start]
        visited[start] = True

        while stack:
            current_node = stack.pop()
            for neighbor, has_edge in enumerate(graph[current_node]):
                if has_edge and not visited[neighbor]:
                    stack.append(neighbor)
                    visited[neighbor] = True

        return all(visited)

    def connect_peers(peers, network_graph):
        for i in range(n):
            peers[i].connected_nodes = []
        non_light_honest_peers = [i for i, peer in enumerate(peers) if not peer.isLight and peer.isHonest]
        # print(non_light_honest_peers)
        for i in range(n):
            rid = random.choice(non_light_honest_peers)
            while len(peers[rid].connected_nodes) == 10:
                rid = random.choice(non_light_honest_peers)
            peers[i].connected_nodes.append(rid)
            peers[rid].connected_nodes.append(i)
            
        
        for i in range(n):
            if len(peers[i].connected_nodes) == 10:
                continue
            deg = 6 + random.randint(0, 4) - len(peers[i].connected_nodes)
            available_nodes = set(range(n))

            while deg > 0 and available_nodes:
                node_id = random.choice(list(available_nodes))
                if not network_graph[i][node_id] and len(peers[node_id].connected_nodes) < 10 and node_id != i:
                    network_graph[i][node_id] = network_graph[node_id][i] = True
                    peers[i].connected_nodes.append(peers[node_id].id)
                    peers[node_id].connected_nodes.append(peers[i].id)
                    deg -= 1
                available_nodes.remove(node_id)

    connect_peers(peers, network_graph)

    # Check if the degree of each node is at least 3
    min_degree = 11
    for i in range(n):
        min_degree = min(min_degree, len(peers[i].connected_nodes))
    while min_degree < 6 or not is_connected(network_graph, 0, [False] * n):
        network_graph = [[False] * n for _ in range(n)]
        # print(min_degree)
        connect_peers(peers, network_graph)
    # show_graph(peers, network_graph)