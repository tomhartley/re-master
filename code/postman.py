import networkx as nx

def odd_graph(graph):
    """
    Given a graph G, construct a graph containing only the vertices with odd degree from G. The resulting graph is
    fully connected, with each weight being the shortest path between the nodes in G.
    Complexity: O(V'*(E + V log(V)) )
    """
    result = nx.Graph()
    odd_nodes = [n for n in graph.nodes() if graph.degree(n) % 2 == 1]
    for u in odd_nodes:
        # We calculate the shortest paths twice here, but the overall performance hit is low
        paths = nx.shortest_path(graph, source=u, weight='weight')
        lengths = nx.shortest_path_length(graph, source=u, weight='weight')
        for v in odd_nodes:
            if u <= v:
                # We only add each edge once
                continue
            # The edge weights are negative for the purpose of max_weight_matching (we want the minimum weight)
            result.add_edge(u, v, weight=-lengths[v], path=paths[v])

    return result

def build_eulerian_graph(graph, odd, matching):
    """
    Build an Eulerian graph from a matching. The result is a MultiGraph.
    """

    # Copy the original graph to a multigraph (so we can add more edges between the same nodes)
    eulerian_graph = nx.MultiGraph(graph)

    # For each matched pair of odd vertices, connect them with the shortest path between them
    for u, v in matching.items():
        if v <= u:
            # Each matching occurs twice in the matchings: (u => v) and (v => u). We only count those where v > u
            continue
        edge = odd[u][v]
        path = edge['path']  # The shortest path between the two nodes, calculated in odd_graph()

        # Add each segment in this path to the graph again
        for p, q in pairs(path):
            eulerian_graph.add_edge(p, q, weight=graph[p][q]['weight'])

    return eulerian_graph

def pairs(lst, circular=False):
    """
    Loop through all pairs of successive items in a list.
    >>> list(pairs([1, 2, 3, 4]))
    [(1, 2), (2, 3), (3, 4)]
    >>> list(pairs([1, 2, 3, 4], circular=True))
    [(1, 2), (2, 3), (3, 4), (4, 1)]
    """
    i = iter(lst)
    first = prev = item = i.next()
    for item in i:
        yield prev, item
        prev = item
    if circular:
        yield item, first


def single_chinese_postman_path(graph):
    """
    Given a graph, return a list of node id's forming the shortest chinese postman path.
    If we assume V' (number of nodes with odd degree) is at least some constant fraction of V (total number of nodes),
    say 10%, the overall complexity is O(V^3).
    """

    # Build a fully-connected graph containing only the odd edges.  Complexity: O(V'*(E + V log(V)) )
    odd = odd_graph(graph)

    # Find the best matching of pairs of odd nodes. Complexity: O(V'^3)
    matching = nx.max_weight_matching(odd, True)

    # Complexity of the remainder is less approximately O(E)
    eulerian_graph = build_eulerian_graph(graph, odd, matching)
    nodes = nx.eulerian_circuit(eulerian_graph)

    return eulerian_graph, nodes

